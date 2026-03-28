from abc import ABC, abstractmethod

from app.domain.conversation import ConversationState


class SessionStore(ABC):
    @abstractmethod
    async def get(self, session_id: str) -> ConversationState | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, state: ConversationState) -> None:
        raise NotImplementedError

