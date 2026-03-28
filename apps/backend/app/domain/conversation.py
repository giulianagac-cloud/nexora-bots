from typing import Literal

from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    id: str
    role: Literal["user", "assistant", "system"]
    content: str


# flow_state examples:
# - main_menu
# - administracion_personal_menu
# - justificar_licencias_menu
# - leave_guidance
# - payroll_support
class ConversationState(BaseModel):
    session_id: str
    flow_state: str = "main_menu"
    messages: list[ConversationMessage] = Field(default_factory=list)
