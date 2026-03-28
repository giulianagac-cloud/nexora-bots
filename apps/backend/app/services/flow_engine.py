import json
import unicodedata
from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# FlowResult — mismo contrato que antes: estado resultante + texto de respuesta.
# El orchestrator y los tests esperan exactamente estos dos campos.
# ---------------------------------------------------------------------------
@dataclass
class FlowResult:
    flow_state: str
    reply_text: str


# ---------------------------------------------------------------------------
# Helpers de carga de JSON
#
# BASE_DIR apunta a la raíz del paquete backend (apps/backend/).
# Desde ahí construimos la ruta a clients/{client_id}/*.json.
# Usamos Path(__file__) para que la ruta funcione independientemente
# de desde dónde se ejecute el proceso.
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]  # apps/backend/


def _load_json(client_id: str, filename: str) -> dict:
    path = BASE_DIR / "clients" / client_id / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# FlowEngine
#
# Se inicializa con un client_id (default "demo") y en ese momento carga
# los tres archivos JSON del cliente.  Todo lo que antes estaba hardcodeado
# en Python (estados, keywords, mensajes) ahora viene de esos archivos.
# ---------------------------------------------------------------------------
class FlowEngine:
    def __init__(self, client_id: str = "demo") -> None:
        self.client_id = client_id

        # flows.json: lista de estados con sus mensajes y opciones de transición
        flows_data = _load_json(client_id, "flows.json")
        self._fallback_message: str = flows_data["fallback_message"]

        # Indexamos los flows por nombre de estado para O(1) en next_step.
        # Estructura: { "main_menu": { "message": ..., "options": [...] }, ... }
        self._flows: dict[str, dict] = {
            flow["state"]: flow for flow in flows_data["flows"]
        }

        # messages.json: mensajes transversales (bienvenida, volver, fallbacks)
        messages_data = _load_json(client_id, "messages.json")
        msgs = messages_data["messages"]
        self._back_to_main_text: str = msgs["back_to_main_menu"]
        self._fallback_module_text: str = msgs["fallback_module_menu"]
        # back_keywords: palabras que siempre devuelven al menú principal
        self._back_keywords: list[str] = msgs["back_keywords"]

    # -----------------------------------------------------------------------
    # _normalize — igual que antes: minúsculas + sin acentos.
    # -----------------------------------------------------------------------
    def _normalize(self, text: str) -> str:
        normalized = unicodedata.normalize("NFD", text.lower().strip())
        return "".join(c for c in normalized if not unicodedata.combining(c))

    # -----------------------------------------------------------------------
    # next_step — el único método público que usa el orchestrator.
    #
    # Lógica en tres pasos:
    #   1. ¿El input es una back_keyword? → volver a main_menu
    #   2. ¿El flow actual tiene una opción cuyas keywords matcheen? → transición
    #   3. Sin match → fallback (distinto si estamos en main_menu o en submódulo)
    # -----------------------------------------------------------------------
    def next_step(self, state, user_input: str) -> FlowResult:
        normalized = self._normalize(user_input)

        # --- Paso 1: back keywords -------------------------------------------
        # Si el usuario escribe "volver", "menu" o "inicio" desde cualquier
        # estado que no sea main_menu, lo devolvemos al menú principal.
        if state.flow_state != "main_menu" and any(
            kw in normalized for kw in self._back_keywords
        ):
            main_flow = self._flows.get("main_menu", {})
            return FlowResult(
                flow_state="main_menu",
                reply_text=self._back_to_main_text + "\n\n" + main_flow.get("message", ""),
            )

        # --- Paso 2: buscar match en el flow actual --------------------------
        # Obtenemos el nodo del flow correspondiente al estado actual.
        current_flow = self._flows.get(state.flow_state)

        if current_flow:
            for option in current_flow.get("options", []):
                # Una opción matchea si cualquiera de sus keywords aparece
                # en el input normalizado del usuario.
                if any(kw in normalized for kw in option["keywords"]):
                    next_state = option["next_state"]
                    next_flow = self._flows.get(next_state, {})
                    return FlowResult(
                        flow_state=next_state,
                        reply_text=next_flow.get("message", self._fallback_message),
                    )

        # --- Paso 3: fallback ------------------------------------------------
        # En main_menu usamos el fallback general del flows.json.
        # En cualquier otro estado usamos el fallback de módulo de messages.json.
        fallback_text = (
            self._fallback_message
            if state.flow_state == "main_menu"
            else self._fallback_module_text
        )
        return FlowResult(
            flow_state=state.flow_state,
            reply_text=fallback_text,
        )
