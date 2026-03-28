from app.services.flow_engine import FlowEngine
from app.domain.conversation import ConversationState

engine = FlowEngine(client_id="demo")
state = ConversationState(session_id="test", flow_state="main_menu")

conversation = [
    "turno",
    "precio",
    "hola no entiendo nada",
    "volver",
]

print(f"[INICIO] estado: {state.flow_state}\n")

for msg in conversation:
    result = engine.next_step(state, msg)
    state.flow_state = result.flow_state
    print(f"Usuario : {msg}")
    print(f"Estado  : {result.flow_state}")
    print(f"Bot     : {result.reply_text}")
    print()
