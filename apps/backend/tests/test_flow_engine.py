import pytest

from app.core.messages import (
    ACCESO_RESPUESTA,
    ADMINISTRACION_PERSONAL_MENU,
    AVISO_ENFERMEDAD_MENU,
    AVISO_ENFERMEDAD_RESPUESTA,
    BUSQUEDAS_MENU,
    CERTIFICADO_RESPUESTA,
    DONACION_SANGRE_RESPUESTA,
    EXODONCIA_RESPUESTA,
    FALLBACK_MAIN_MENU,
    FALLBACK_MODULE_MENU,
    JUSTIFICAR_LICENCIA_MEDICA_MENU,
    PROXIMA_CITA_RESPUESTA,
    SERVICIO_MEDICO_MENU,
    SOPORTE_MENU,
    VOLVER_MENU_PRINCIPAL,
)
from app.domain.conversation import ConversationState
import app.services.flow_engine as flow_engine_module
from app.services.flow_engine import FlowEngine


@pytest.mark.parametrize(
    ("user_input", "expected_flow_state"),
    [
        ("disponibles", "licencias_disponibles"),
        ("justificar", "justificar_licencias_menu"),
    ],
)
def test_flow_engine_routes_from_administracion_personal_menu(
    user_input: str, expected_flow_state: str
) -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="administracion_personal_menu",
    )

    result = engine.next_step(state=state, user_input=user_input)

    assert result.flow_state == expected_flow_state


@pytest.mark.parametrize(
    "initial_flow_state",
    [
        "administracion_personal_menu",
        "justificar_licencias_menu",
        "licencias_disponibles",
        "busquedas_internas_menu",
        "servicio_medico_menu",
        "aviso_enfermedad_menu",
        "justificar_licencia_medica_menu",
        "soporte_menu",
    ],
)
def test_flow_engine_returns_to_main_menu_from_submenus(
    initial_flow_state: str,
) -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state=initial_flow_state,
    )

    result = engine.next_step(state=state, user_input="volver")

    assert result.flow_state == "main_menu"
    assert result.reply_text == VOLVER_MENU_PRINCIPAL


@pytest.mark.parametrize(
    "initial_flow_state",
    [
        "administracion_personal_menu",
        "justificar_licencias_menu",
        "busquedas_internas_menu",
        "servicio_medico_menu",
        "aviso_enfermedad_menu",
        "justificar_licencia_medica_menu",
        "soporte_menu",
    ],
)
def test_flow_engine_returns_module_fallback_from_submenus(
    initial_flow_state: str,
) -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state=initial_flow_state,
    )

    result = engine.next_step(state=state, user_input="asdf")

    assert result.flow_state == initial_flow_state
    assert result.reply_text == FALLBACK_MODULE_MENU


@pytest.mark.parametrize(
    "user_input",
    [
        "volver",
        "menu",
        "menú",
        "inicio",
    ],
)
def test_flow_engine_returns_to_main_menu_from_administracion_personal_menu_aliases(
    user_input: str,
) -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="administracion_personal_menu",
    )

    result = engine.next_step(state=state, user_input=user_input)

    assert result.flow_state == "main_menu"
    assert result.reply_text == VOLVER_MENU_PRINCIPAL


@pytest.mark.parametrize(
    "initial_flow_state",
    [
        "soporte_menu",
        "servicio_medico_menu",
        "aviso_enfermedad_menu",
        "justificar_licencia_medica_menu",
        "busquedas_internas_menu",
    ],
)
@pytest.mark.parametrize(
    "user_input",
    [
        "menu",
        "men\u00fa",
    ],
)
def test_flow_engine_returns_to_main_menu_from_submenu_aliases(
    initial_flow_state: str,
    user_input: str,
) -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state=initial_flow_state,
    )

    result = engine.next_step(state=state, user_input=user_input)

    assert result.flow_state == "main_menu"
    assert result.reply_text == VOLVER_MENU_PRINCIPAL


def test_flow_engine_routes_to_licencias_disponibles_with_reply_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        flow_engine_module,
        "get_vacaciones",
        lambda: {"dias_disponibles": 21},
    )

    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="administracion_personal_menu",
    )

    result = engine.next_step(state=state, user_input="disponibles")

    assert result.flow_state == "licencias_disponibles"
    assert result.reply_text == "Según SAP, tenés 21 días de vacaciones disponibles."


@pytest.mark.parametrize(
    ("user_input", "expected_flow_state", "expected_reply_text"),
    [
        ("administracion", "administracion_personal_menu", ADMINISTRACION_PERSONAL_MENU),
        ("admin", "administracion_personal_menu", ADMINISTRACION_PERSONAL_MENU),
        ("adm personal", "administracion_personal_menu", ADMINISTRACION_PERSONAL_MENU),
        ("personal", "administracion_personal_menu", ADMINISTRACION_PERSONAL_MENU),
        ("licencias", "administracion_personal_menu", ADMINISTRACION_PERSONAL_MENU),
        ("busquedas", "busquedas_internas_menu", BUSQUEDAS_MENU),
        ("busqueda", "busquedas_internas_menu", BUSQUEDAS_MENU),
        ("medico", "servicio_medico_menu", SERVICIO_MEDICO_MENU),
        ("médico", "servicio_medico_menu", SERVICIO_MEDICO_MENU),
        ("servicio medico", "servicio_medico_menu", SERVICIO_MEDICO_MENU),
        ("soporte", "soporte_menu", SOPORTE_MENU),
    ],
)
def test_flow_engine_routes_from_main_menu(
    user_input: str,
    expected_flow_state: str,
    expected_reply_text: str,
) -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="main_menu",
    )

    result = engine.next_step(state=state, user_input=user_input)

    assert result.flow_state == expected_flow_state
    assert result.reply_text == expected_reply_text


@pytest.mark.parametrize(
    ("user_input", "expected_flow_state", "expected_reply_text"),
    [
        ("a", "aviso_enfermedad_menu", AVISO_ENFERMEDAD_MENU),
        ("aviso", "aviso_enfermedad_menu", AVISO_ENFERMEDAD_MENU),
        ("b", "justificar_licencia_medica_menu", JUSTIFICAR_LICENCIA_MEDICA_MENU),
        ("justificar", "justificar_licencia_medica_menu", JUSTIFICAR_LICENCIA_MEDICA_MENU),
    ],
)
def test_flow_engine_routes_from_servicio_medico_menu(
    user_input: str,
    expected_flow_state: str,
    expected_reply_text: str,
) -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="servicio_medico_menu",
    )

    result = engine.next_step(state=state, user_input=user_input)

    assert result.flow_state == expected_flow_state
    assert result.reply_text == expected_reply_text


@pytest.mark.parametrize(
    ("user_input", "expected_reply_text"),
    [
        ("aviso", AVISO_ENFERMEDAD_RESPUESTA),
        ("cita", PROXIMA_CITA_RESPUESTA),
    ],
)
def test_flow_engine_returns_aviso_enfermedad_responses(
    user_input: str,
    expected_reply_text: str,
) -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="aviso_enfermedad_menu",
    )

    result = engine.next_step(state=state, user_input=user_input)

    assert result.flow_state == "aviso_enfermedad_menu"
    assert result.reply_text == expected_reply_text


@pytest.mark.parametrize(
    ("user_input", "expected_reply_text"),
    [
        ("certificado", CERTIFICADO_RESPUESTA),
        ("exodoncia", EXODONCIA_RESPUESTA),
        ("donacion de sangre", DONACION_SANGRE_RESPUESTA),
    ],
)
def test_flow_engine_returns_justificar_licencia_medica_responses(
    user_input: str,
    expected_reply_text: str,
) -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="justificar_licencia_medica_menu",
    )

    result = engine.next_step(state=state, user_input=user_input)

    assert result.flow_state == "justificar_licencia_medica_menu"
    assert result.reply_text == expected_reply_text


@pytest.mark.parametrize(
    "user_input",
    [
        "soporte",
        "acceso",
        "problema",
        "app",
    ],
)
def test_flow_engine_returns_soporte_response(
    user_input: str,
) -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="soporte_menu",
    )

    result = engine.next_step(state=state, user_input=user_input)

    assert result.flow_state == "soporte_menu"
    assert result.reply_text == ACCESO_RESPUESTA


def test_flow_engine_returns_main_menu_fallback() -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="main_menu",
    )

    result = engine.next_step(state=state, user_input="asdf")

    assert result.flow_state == "main_menu"
    assert result.reply_text == FALLBACK_MAIN_MENU


def test_flow_engine_routes_conversational_flow_to_justificar_vacaciones() -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="main_menu",
    )

    step_1 = engine.next_step(state=state, user_input="administracion")
    assert step_1.flow_state == "administracion_personal_menu"

    state = ConversationState(
        session_id="test-session",
        flow_state=step_1.flow_state,
    )
    step_2 = engine.next_step(state=state, user_input="justificar")
    assert step_2.flow_state == "justificar_licencias_menu"

    state = ConversationState(
        session_id="test-session",
        flow_state=step_2.flow_state,
    )
    step_3 = engine.next_step(state=state, user_input="vacaciones")
    assert step_3.flow_state == "justificar_vacaciones"


def test_flow_engine_routes_conversational_flow_to_licencias_disponibles() -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="main_menu",
    )

    step_1 = engine.next_step(state=state, user_input="administracion")
    assert step_1.flow_state == "administracion_personal_menu"

    state = ConversationState(
        session_id="test-session",
        flow_state=step_1.flow_state,
    )
    step_2 = engine.next_step(state=state, user_input="disponibles")
    assert step_2.flow_state == "licencias_disponibles"


def test_flow_engine_routes_conversational_flow_to_licencias_disponibles_from_admin_alias() -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="main_menu",
    )

    step_1 = engine.next_step(state=state, user_input="admin")
    assert step_1.flow_state == "administracion_personal_menu"

    state = ConversationState(
        session_id="test-session",
        flow_state=step_1.flow_state,
    )
    step_2 = engine.next_step(state=state, user_input="disponibles")
    assert step_2.flow_state == "licencias_disponibles"


def test_flow_engine_routes_conversational_flow_to_soporte() -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="main_menu",
    )

    step_1 = engine.next_step(state=state, user_input="soporte")
    assert step_1.flow_state == "soporte_menu"

    state = ConversationState(
        session_id="test-session",
        flow_state=step_1.flow_state,
    )
    step_2 = engine.next_step(state=state, user_input="acceso")
    assert step_2.flow_state == "soporte_menu"


def test_flow_engine_routes_conversational_flow_to_servicio_medico() -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="main_menu",
    )

    step_1 = engine.next_step(state=state, user_input="medico")
    assert step_1.flow_state == "servicio_medico_menu"

    state = ConversationState(
        session_id="test-session",
        flow_state=step_1.flow_state,
    )
    step_2 = engine.next_step(state=state, user_input="aviso")
    assert step_2.flow_state == "aviso_enfermedad_menu"


def test_flow_engine_routes_conversational_flow_to_busquedas_internas() -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="main_menu",
    )

    step_1 = engine.next_step(state=state, user_input="busquedas")
    assert step_1.flow_state == "busquedas_internas_menu"

    state = ConversationState(
        session_id="test-session",
        flow_state=step_1.flow_state,
    )
    step_2 = engine.next_step(state=state, user_input="vacantes")
    assert step_2.flow_state == "busquedas_internas_menu"


@pytest.mark.parametrize(
    ("user_input", "expected_flow_state"),
    [
        ("a", "justificar_vacaciones"),
        ("examen", "justificar_examen"),
        ("mudanza", "justificar_mudanza"),
    ],
)
def test_flow_engine_routes_from_justificar_licencias_menu(
    user_input: str, expected_flow_state: str
) -> None:
    engine = FlowEngine()
    state = ConversationState(
        session_id="test-session",
        flow_state="justificar_licencias_menu",
    )

    result = engine.next_step(state=state, user_input=user_input)

    assert result.flow_state == expected_flow_state
