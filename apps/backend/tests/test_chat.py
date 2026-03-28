import asyncio

import httpx
import pytest

from app.core.messages import (
    ADMINISTRACION_PERSONAL_MENU,
    AVISO_ENFERMEDAD_MENU,
    FALLBACK_MODULE_MENU,
    JUSTIFICAR_LICENCIA_MEDICA_MENU,
    VACANTES_RESPUESTA,
    VOLVER_MENU_PRINCIPAL,
)
from app.main import app
import app.services.flow_engine as flow_engine_module


def _post_chat(session_id: str, message: str):
    async def _request():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            return await client.post(
                "/chat", json={"session_id": session_id, "message": message}
            )

    return asyncio.run(_request())


def test_chat_returns_guided_leave_response() -> None:
    response = _post_chat("session-1", "I need vacation information")

    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"] == "session-1"
    assert payload["flow_state"] == "leave_guidance"
    assert "circuito de licencias" in payload["reply"]["content"]


def test_chat_routes_to_administracion_personal_menu() -> None:
    response = _post_chat("api-test", "administracion")

    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"] == "api-test"
    assert payload["flow_state"] == "administracion_personal_menu"
    assert payload["reply"]["content"] == ADMINISTRACION_PERSONAL_MENU


def test_chat_routes_conversational_flow_to_justificar_vacaciones() -> None:
    response = _post_chat("api-flow-test", "administracion")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "administracion_personal_menu"

    response = _post_chat("api-flow-test", "justificar")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "justificar_licencias_menu"

    response = _post_chat("api-flow-test", "vacaciones")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "justificar_vacaciones"


def test_chat_routes_conversational_flow_to_justificar_mudanza() -> None:
    response = _post_chat("api-mudanza-flow-test", "administracion")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "administracion_personal_menu"

    response = _post_chat("api-mudanza-flow-test", "justificar")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "justificar_licencias_menu"

    response = _post_chat("api-mudanza-flow-test", "mudanza")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "justificar_mudanza"


def test_chat_routes_conversational_flow_to_justificar_examen() -> None:
    response = _post_chat("api-examen-flow-test", "administracion")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "administracion_personal_menu"

    response = _post_chat("api-examen-flow-test", "justificar")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "justificar_licencias_menu"

    response = _post_chat("api-examen-flow-test", "examen")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "justificar_examen"


def test_chat_routes_conversational_flow_to_justificar_examen_with_natural_alias() -> None:
    response = _post_chat("api-examen-alias-flow-test", "administracion")

    assert response.status_code == 200

    response = _post_chat("api-examen-alias-flow-test", "justificar")

    assert response.status_code == 200

    response = _post_chat("api-examen-alias-flow-test", "rindo mañana un final")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "justificar_examen"


def test_chat_routes_back_to_main_menu_with_volver() -> None:
    response = _post_chat("api-volver-test", "administracion")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "administracion_personal_menu"

    response = _post_chat("api-volver-test", "volver")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "main_menu"
    assert payload["reply"]["content"] == VOLVER_MENU_PRINCIPAL


def test_chat_routes_conversational_flow_to_busquedas_internas() -> None:
    response = _post_chat("api-busquedas-test", "busquedas")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "busquedas_internas_menu"

    response = _post_chat("api-busquedas-test", "vacantes")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "busquedas_internas_menu"
    assert payload["reply"]["content"] == VACANTES_RESPUESTA


def test_chat_returns_module_fallback_within_soporte() -> None:
    response = _post_chat("api-soporte-fallback-test", "soporte")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "soporte_menu"

    response = _post_chat("api-soporte-fallback-test", "asdf")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "soporte_menu"
    assert payload["reply"]["content"] == FALLBACK_MODULE_MENU


def test_chat_returns_module_fallback_within_servicio_medico() -> None:
    response = _post_chat("api-medico-fallback-test", "medico")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "servicio_medico_menu"

    response = _post_chat("api-medico-fallback-test", "asdf")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "servicio_medico_menu"
    assert payload["reply"]["content"] == FALLBACK_MODULE_MENU


def test_chat_routes_conversational_flow_to_aviso_enfermedad() -> None:
    response = _post_chat("api-aviso-enfermedad-flow-test", "medico")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "servicio_medico_menu"

    response = _post_chat("api-aviso-enfermedad-flow-test", "a")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "aviso_enfermedad_menu"
    assert payload["reply"]["content"] == AVISO_ENFERMEDAD_MENU


def test_chat_routes_conversational_flow_to_justificar_licencia_medica() -> None:
    response = _post_chat("api-licencia-medica-flow-test", "medico")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "servicio_medico_menu"

    response = _post_chat("api-licencia-medica-flow-test", "justificar")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "justificar_licencia_medica_menu"
    assert payload["reply"]["content"] == JUSTIFICAR_LICENCIA_MEDICA_MENU


def test_chat_returns_module_fallback_within_busquedas_internas() -> None:
    response = _post_chat("api-busquedas-fallback-test", "busquedas")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "busquedas_internas_menu"

    response = _post_chat("api-busquedas-fallback-test", "asdf")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "busquedas_internas_menu"
    assert payload["reply"]["content"] == FALLBACK_MODULE_MENU


def test_chat_returns_module_fallback_within_justificar_licencias() -> None:
    response = _post_chat("api-justificar-fallback-test", "administracion")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "administracion_personal_menu"

    response = _post_chat("api-justificar-fallback-test", "justificar")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "justificar_licencias_menu"

    response = _post_chat("api-justificar-fallback-test", "asdf")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "justificar_licencias_menu"
    assert payload["reply"]["content"] == FALLBACK_MODULE_MENU


def test_chat_routes_conversational_flow_to_licencias_disponibles(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        flow_engine_module,
        "get_vacaciones",
        lambda: {"dias_disponibles": 21},
    )

    response = _post_chat("api-licencias-disponibles-test", "administracion")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "administracion_personal_menu"

    response = _post_chat("api-licencias-disponibles-test", "disponibles")

    assert response.status_code == 200
    payload = response.json()
    assert payload["flow_state"] == "licencias_disponibles"
    assert payload["reply"]["content"] == "Según SAP, tenés 21 días de vacaciones disponibles."
