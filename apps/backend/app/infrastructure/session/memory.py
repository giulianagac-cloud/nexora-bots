from app.domain.conversation import ConversationState
from app.infrastructure.session.base import SessionStore


class InMemorySessionStore(SessionStore):
    def __init__(self) -> None:
        self._sessions: dict[str, ConversationState] = {}

    async def get(self, session_id: str) -> ConversationState | None:
        return self._sessions.get(session_id)

    async def save(self, state: ConversationState) -> None:
        self._sessions[state.session_id] = state

