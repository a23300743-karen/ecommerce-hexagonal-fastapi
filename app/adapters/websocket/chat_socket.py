import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.application.services.chat_service import ChatService
from app.infrastructure.faq.faq_memory_repository import FAQMemoryRepository
from app.realtime.connection_manager import ConnectionManager

router = APIRouter(
    tags=["Realtime Chat"]
)

faq_provider = FAQMemoryRepository()
chat_service = ChatService(faq_provider)
manager = ConnectionManager()


@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    await manager.connect(websocket)

    await manager.send_personal_message(
        {
            "type": "system",
            "response": "Conexion establecida con el chat de soporte."
        },
        websocket
    )

    try:
        while True:
            payload = await _receive_payload(websocket)

            result = chat_service.process_message(
                user=payload["user"],
                content=payload["content"]
            )

            await manager.send_personal_message(result, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except ValueError as error:
        await manager.send_personal_message(
            {
                "type": "error",
                "response": str(error)
            },
            websocket
        )
        manager.disconnect(websocket)


async def _receive_payload(websocket: WebSocket):
    text = await websocket.receive_text()

    try:
        payload = _parse_json_payload(text)
        return {
            "user": payload.get("user", "client"),
            "content": payload.get("content", "")
        }

    except ValueError:
        return {
            "user": "client",
            "content": text
        }


def _parse_json_payload(text: str):
    if not text.strip().startswith("{"):
        raise ValueError("No JSON payload")

    return json.loads(text)
