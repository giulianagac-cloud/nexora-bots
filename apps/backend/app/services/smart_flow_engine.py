"""
SmartFlowEngine — misma interfaz pública que FlowEngine.

Reemplaza el matching por keywords con clasificación TF-IDF via NLPEngine.
Aplica context boosting: si el usuario ya está en un estado asociado a un
intent, ese intent recibe un bonus de score para mantener el contexto salvo
que el usuario cambie claramente de tema.
"""
from __future__ import annotations

import json
import unicodedata
from pathlib import Path

from app.services.entity_extractor import EntityExtractor
from app.services.flow_engine import FlowResult
from app.services.nlp_engine import NLPEngine

BASE_DIR = Path(__file__).resolve().parents[2]  # apps/backend/


def _load_json(client_id: str, filename: str) -> dict:
    path = BASE_DIR / "clients" / client_id / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class SmartFlowEngine:
    def __init__(self, client_id: str = "demo") -> None:
        self.client_id = client_id

        flows_data = _load_json(client_id, "flows.json")
        self._fallback_message: str = flows_data["fallback_message"]
        self._flows: dict[str, dict] = {
            flow["state"]: flow for flow in flows_data["flows"]
        }

        messages_data = _load_json(client_id, "messages.json")
        msgs = messages_data["messages"]
        self._back_to_main_text: str = msgs["back_to_main_menu"]
        self._fallback_module_text: str = msgs["fallback_module_menu"]
        self._back_keywords: list[str] = msgs["back_keywords"]

        intents_data = _load_json(client_id, "intents.json")
        self._context_boost: float = intents_data.get("context_boost", 0.0)
        self._nlp = NLPEngine(intents_data)
        self._entity_extractor = EntityExtractor()

        # Mapa inverso state → intent para el boosting de contexto.
        self._state_to_intent: dict[str, str] = {}
        for intent_def in intents_data.get("intents", []):
            intent_name = intent_def["intent"]
            next_state = intent_def.get("next_state")
            if next_state:
                self._state_to_intent[next_state] = intent_name

    def _normalize(self, text: str) -> str:
        nfd = unicodedata.normalize("NFD", text.lower().strip())
        return "".join(c for c in nfd if not unicodedata.combining(c))

    def _options_for_state(self, state_name: str) -> list[dict]:
        flow = self._flows.get(state_name, {})
        result = []
        for opt in flow.get("options", []):
            if opt.get("label") and opt.get("keywords"):
                result.append({"label": opt["label"], "keyword": opt["keywords"][0]})
        return result

    def _classify_with_context(self, user_input: str, current_state: str) -> tuple[str | None, float]:
        """
        Clasifica el input aplicando context boost al intent del estado actual.
        Si el usuario está en turnos_menu y escribe algo ambiguo, el intent
        'turnos' recibe un bonus antes de comparar con otros intents.
        """
        intent_scores = self._nlp.scores(user_input)

        # Aplicar boost al intent correspondiente al estado actual.
        context_intent = self._state_to_intent.get(current_state)
        if context_intent and self._context_boost > 0:
            intent_scores[context_intent] = (
                intent_scores.get(context_intent, 0.0) + self._context_boost
            )

        if not intent_scores:
            return None, 0.0

        best_intent = max(intent_scores, key=lambda k: intent_scores[k])
        best_score = intent_scores[best_intent]

        # El threshold se aplica sobre el score sin boost para no bajar el
        # umbral de confianza real — sólo usamos el boost para desempatar.
        raw_scores = self._nlp.scores(user_input)
        raw_best = raw_scores.get(best_intent, 0.0)
        threshold = self._nlp._threshold

        if raw_best < threshold and best_intent != context_intent:
            return None, raw_best

        # Si ganó por boost pero el score crudo es muy bajo, aplicar fallback.
        if best_intent == context_intent and raw_best < threshold * 0.4:
            return None, raw_best

        return best_intent, best_score

    def next_step(self, state, user_input: str) -> FlowResult:
        # --- Paso 0: init trigger -------------------------------------------
        if user_input == "__init__":
            main_flow = self._flows.get("main_menu", {})
            return FlowResult(
                flow_state="main_menu",
                reply_text=main_flow.get("message", self._fallback_message),
                options=self._options_for_state("main_menu"),
            )

        normalized = self._normalize(user_input)

        # --- Paso 1: back keywords ------------------------------------------
        if state.flow_state != "main_menu" and any(
            kw in normalized for kw in self._back_keywords
        ):
            main_flow = self._flows.get("main_menu", {})
            return FlowResult(
                flow_state="main_menu",
                reply_text=self._back_to_main_text + "\n\n" + main_flow.get("message", ""),
                options=self._options_for_state("main_menu"),
            )

        # --- Paso 2: extracción de entidades (paralelo a NLP) ---------------
        entities = self._entity_extractor.extract(user_input)

        # --- Paso 3: clasificación NLP con context boosting -----------------
        intent, score = self._classify_with_context(user_input, state.flow_state)

        if intent is not None:
            next_state = self._nlp.state_for_intent(intent) or state.flow_state
            next_flow = self._flows.get(next_state, {})
            return FlowResult(
                flow_state=next_state,
                reply_text=next_flow.get("message", self._fallback_message),
                options=self._options_for_state(next_state),
                entities=entities,
            )

        # --- Paso 4: fallback -----------------------------------------------
        fallback_text = (
            self._fallback_message
            if state.flow_state == "main_menu"
            else self._fallback_module_text
        )
        return FlowResult(
            flow_state=state.flow_state,
            reply_text=fallback_text,
            options=self._options_for_state(state.flow_state),
            entities=entities,
        )
