from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Client-generated or persisted session id.")
    message: str = Field(..., min_length=1, description="User message sent to the assistant.")


class ChatMessage(BaseModel):
    id: str
    role: Literal["assistant", "user", "system"]
    content: str


class ChatOption(BaseModel):
    label: str
    keyword: str


class ChatResponse(BaseModel):
    session_id: str
    reply: ChatMessage
    flow_state: str
    options: list[ChatOption] = Field(default_factory=list)

