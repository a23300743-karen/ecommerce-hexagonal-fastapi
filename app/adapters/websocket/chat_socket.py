import json
from dataclasses import asdict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.application.services.support_chat_service import SupportChatService
from app.infrastructure.faq.faq_memory_repository import FAQMemoryRepository
from app.infrastructure.repositories.mysql_support_chat_repository import MySQLSupportChatRepository
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.infrastructure.security.jwt_service import JWTService
from app.realtime.connection_manager import ConnectionManager

router = APIRouter(tags=["Realtime Chat"])
manager = ConnectionManager()
support_chat_service = SupportChatService(MySQLSupportChatRepository(), FAQMemoryRepository())


@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    user = _authenticate(websocket.query_params.get("token"))
    if user is None:
        await websocket.close(code=1008)
        return

    if user.role == "ADMIN":
        await manager.connect_admin(websocket)
    else:
        await manager.connect_customer(user.id, websocket)
        conversation = support_chat_service.get_or_create_conversation(user.id)
        history = support_chat_service.list_messages(conversation.id)
        await websocket.send_json({
            "type": "history",
            "conversation_id": conversation.id,
            "messages": [_serialize(item) for item in history]
        })

    try:
        while True:
            payload = json.loads(await websocket.receive_text())
            if user.role == "ADMIN":
                await _handle_admin_message(websocket, payload)
            else:
                await _handle_customer_message(user.id, websocket, payload)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except (ValueError, json.JSONDecodeError) as error:
        await websocket.send_json({"type": "error", "response": str(error)})
        manager.disconnect(websocket)


async def _handle_customer_message(user_id, websocket, payload):
    conversation, customer_message, automatic_message = support_chat_service.receive_customer_message(
        user_id, payload.get("content", "")
    )
    await websocket.send_json({"type": "saved", "message": _serialize(customer_message)})
    await manager.notify_admins({"type": "conversation_updated", "conversation_id": conversation.id})
    if automatic_message:
        await websocket.send_json({"type": "message", "message": _serialize(automatic_message)})


async def _handle_admin_message(websocket, payload):
    conversation_id = int(payload.get("conversation_id", 0))
    message = support_chat_service.send_admin_message(conversation_id, payload.get("content", ""))
    conversation = support_chat_service.get_conversation(conversation_id)
    serialized = _serialize(message)
    await websocket.send_json({"type": "message", "message": serialized})
    await manager.send_to_customer(conversation.user_id, {"type": "message", "message": serialized})
    await manager.notify_admins({"type": "conversation_updated", "conversation_id": conversation_id})


def _authenticate(token):
    if not token:
        return None
    try:
        payload = JWTService().decode_access_token(token)
        user = MySQLUserRepository().get_by_id(int(payload.get("sub")))
        return user if user and user.status == "ACTIVE" else None
    except Exception:
        return None


def _serialize(value):
    data = asdict(value)
    data["created_at"] = value.created_at.isoformat()
    return data
