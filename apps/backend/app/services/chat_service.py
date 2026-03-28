from app.schemas.chat import ChatRequest, ChatResponse
from app.services.conversation_orchestrator import ConversationOrchestrator


class ChatService:
    def __init__(self, orchestrator: ConversationOrchestrator) -> None:
        self.orchestrator = orchestrator

    async def handle_message(self, payload: ChatRequest) -> ChatResponse:
        return await self.orchestrator.handle_message(payload)

