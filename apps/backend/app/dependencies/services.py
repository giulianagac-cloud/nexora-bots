from app.infrastructure.session.memory import InMemorySessionStore
from app.services.chat_service import ChatService
from app.services.conversation_orchestrator import ConversationOrchestrator
from app.services.flow_engine import FlowEngine

session_store = InMemorySessionStore()
flow_engine = FlowEngine()
orchestrator = ConversationOrchestrator(flow_engine=flow_engine, session_store=session_store)


async def get_chat_service() -> ChatService:
    return ChatService(orchestrator=orchestrator)
