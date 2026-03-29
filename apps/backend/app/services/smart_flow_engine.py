"""
SmartFlowEngine — misma interfaz pública que FlowEngine.

Reemplaza el matching por keywords con clasificación TF-IDF via NLPEngine.
El ConversationOrchestrator no necesita saber cuál motor está activo.
"""
from __future__ import annotations

import json
import unicodedata
from dataclasses import dataclass
from pathlib import Path

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
        self._nlp = NLPEngine(intents_data)

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

        # --- Paso 2: clasificación NLP --------------------------------------
        intent, score = self._nlp.classify(user_input)

        if intent is not None:
            next_state = self._nlp.state_for_intent(intent) or state.flow_state
            next_flow = self._flows.get(next_state, {})
            return FlowResult(
                flow_state=next_state,
                reply_text=next_flow.get("message", self._fallback_message),
                options=self._options_for_state(next_state),
            )

        # --- Paso 3: fallback -----------------------------------------------
        fallback_text = (
            self._fallback_message
            if state.flow_state == "main_menu"
            else self._fallback_module_text
        )
        return FlowResult(
            flow_state=state.flow_state,
            reply_text=fallback_text,
            options=self._options_for_state(state.flow_state),
        )
