from uuid import uuid4

from app.core.logging import get_logger
from app.domain.conversation import ConversationMessage, ConversationState
from app.infrastructure.session.base import SessionStore
from app.schemas.chat import ChatMessage, ChatOption, ChatRequest, ChatResponse
from app.services.flow_engine import FlowEngine

logger = get_logger(__name__)


class ConversationOrchestrator:
    def __init__(self, flow_engine: FlowEngine, session_store: SessionStore) -> None:
        self.flow_engine = flow_engine
        self.session_store = session_store

    async def handle_message(self, payload: ChatRequest) -> ChatResponse:
        state = await self.session_store.get(payload.session_id)
        if state is None:
            state = ConversationState(session_id=payload.session_id)

        is_init = payload.message == "__init__"

        if not is_init:
            user_message = ConversationMessage(
                id=str(uuid4()),
                role="user",
                content=payload.message,
            )
            state.messages.append(user_message)

        flow_result = self.flow_engine.next_step(state=state, user_input=payload.message)
        assistant_message = ConversationMessage(
            id=str(uuid4()),
            role="assistant",
            content=flow_result.reply_text,
        )
        state.messages.append(assistant_message)
        state.flow_state = flow_result.flow_state

        await self.session_store.save(state)
        logger.info(
            "chat_message_processed",
            extra={
                "session_id": payload.session_id,
                "flow_state": state.flow_state,
                "message_count": len(state.messages),
            },
        )

        return ChatResponse(
            session_id=payload.session_id,
            flow_state=state.flow_state,
            reply=ChatMessage.model_validate(assistant_message.model_dump()),
            options=[ChatOption(**opt) for opt in flow_result.options],
        )

