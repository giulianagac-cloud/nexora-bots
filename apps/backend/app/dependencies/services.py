import json
from pathlib import Path

from app.core.config import get_settings
from app.infrastructure.session.memory import InMemorySessionStore
from app.services.chat_service import ChatService
from app.services.conversation_orchestrator import ConversationOrchestrator
from app.services.flow_engine import FlowEngine
from app.services.smart_flow_engine import SmartFlowEngine

BASE_DIR = Path(__file__).resolve().parents[2]  # apps/backend/


def _get_bot_type(client_id: str) -> str:
    path = BASE_DIR / "clients" / client_id / "config.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("bot_type", "starter")


def _build_engine(client_id: str):
    bot_type = _get_bot_type(client_id)
    if bot_type == "smart":
        return SmartFlowEngine(client_id=client_id)
    return FlowEngine(client_id=client_id)


session_store = InMemorySessionStore()
flow_engine = _build_engine(get_settings().client_id)
orchestrator = ConversationOrchestrator(flow_engine=flow_engine, session_store=session_store)


async def get_chat_service() -> ChatService:
    return ChatService(orchestrator=orchestrator)
