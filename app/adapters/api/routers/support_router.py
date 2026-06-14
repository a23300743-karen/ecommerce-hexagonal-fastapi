from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException

from app.adapters.api.dependencies.auth_dependencies import require_admin
from app.application.services.support_chat_service import SupportChatService

router = APIRouter(prefix="/support", tags=["Support"])


def get_support_router(service: SupportChatService):

    @router.get("/conversations")
    def list_conversations(current_user=Depends(require_admin)):
        return [asdict(item) for item in service.list_conversations()]

    @router.get("/conversations/{conversation_id}/messages")
    def list_messages(conversation_id: int, current_user=Depends(require_admin)):
        try:
            return [asdict(item) for item in service.list_messages(conversation_id)]
        except ValueError as error:
            raise HTTPException(status_code=404, detail=str(error))

    return router
