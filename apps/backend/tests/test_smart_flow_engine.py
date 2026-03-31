"""
Tests de SmartFlowEngine: slot-filling, template interpolation y flujos NLP.
"""
import pytest

from app.domain.conversation import ConversationState
from app.services.smart_flow_engine import SmartFlowEngine


@pytest.fixture
def engine() -> SmartFlowEngine:
    return SmartFlowEngine(client_id="demo-smart")


def _state(flow_state: str = "main_menu", entities: dict | None = None) -> ConversationState:
    return ConversationState(
        session_id="test",
        flow_state=flow_state,
        entities=entities or {},
    )


# ---------------------------------------------------------------------------
# Init trigger
# ---------------------------------------------------------------------------
def test_init_devuelve_main_menu(engine: SmartFlowEngine) -> None:
    result = engine.next_step(_state(), "__init__")
    assert result.flow_state == "main_menu"
    assert result.reply_text  # mensaje de bienvenida no vacío


# ---------------------------------------------------------------------------
# Back keywords
# ---------------------------------------------------------------------------
def test_back_keyword_vuelve_a_main_menu(engine: SmartFlowEngine) -> None:
    result = engine.next_step(_state("turnos_menu"), "volver")
    assert result.flow_state == "main_menu"


# ---------------------------------------------------------------------------
# Slot-filling: pedir entidades faltantes
# ---------------------------------------------------------------------------
def test_turnos_pide_fecha_si_no_viene_en_mensaje(engine: SmartFlowEngine) -> None:
    # El usuario clasifica intent "turnos" pero no da fecha ni hora.
    result = engine.next_step(_state("main_menu"), "quiero sacar un turno")
    assert result.flow_state == "turnos_menu"
    # Debe pedir la primera entidad faltante: fecha
    assert "día" in result.reply_text.lower() or "fecha" in result.reply_text.lower()


def test_turnos_pide_hora_si_ya_tiene_fecha(engine: SmartFlowEngine) -> None:
    # El usuario ya aportó fecha en el turno anterior (session entity).
    state = _state("turnos_menu", entities={"fecha": "martes"})
    result = engine.next_step(state, "el martes")  # repite fecha, sigue faltando hora
    assert result.flow_state == "turnos_menu"
    assert "hora" in result.reply_text.lower() or "mejor" in result.reply_text.lower()


def test_turnos_pide_hora_cuando_llega_en_mismo_mensaje(engine: SmartFlowEngine) -> None:
    # El usuario da fecha en el mensaje de turnos: falta hora.
    result = engine.next_step(_state("main_menu"), "quiero un turno el martes")
    assert result.flow_state == "turnos_menu"
    assert "hora" in result.reply_text.lower() or "mejor" in result.reply_text.lower()


# ---------------------------------------------------------------------------
# Slot-filling: mensaje final con interpolación
# ---------------------------------------------------------------------------
def test_turnos_mensaje_final_interpola_entidades(engine: SmartFlowEngine) -> None:
    # El usuario da fecha + hora en el mismo turno.
    result = engine.next_step(
        _state("main_menu"),
        "quiero un turno el martes a las 10",
    )
    assert result.flow_state == "turnos_menu"
    assert "martes" in result.reply_text
    assert "10" in result.reply_text


def test_turnos_mensaje_final_usa_entidades_de_sesion(engine: SmartFlowEngine) -> None:
    # Fecha viene de la sesión, hora viene del mensaje actual.
    state = _state("turnos_menu", entities={"fecha": "viernes"})
    result = engine.next_step(state, "a las 15")
    assert result.flow_state == "turnos_menu"
    assert "viernes" in result.reply_text
    assert "15" in result.reply_text


# ---------------------------------------------------------------------------
# Slot-filling: continuar colectando si NLP no clasifica
# ---------------------------------------------------------------------------
def test_sigue_colectando_cuando_nlp_no_clasifica(engine: SmartFlowEngine) -> None:
    # El usuario está en turnos_menu y escribe sólo "el lunes" sin contexto de intent.
    # NLP no debería clasificar eso como intent claro, pero el motor debe seguir
    # colectando (Paso 4) en lugar de mostrar el fallback.
    state = _state("turnos_menu", entities={"fecha": "lunes"})
    result = engine.next_step(state, "a las 9")
    # Con fecha=lunes y hora=9 ya están completas → mensaje final
    assert result.flow_state == "turnos_menu"
    assert "lunes" in result.reply_text
    assert "9" in result.reply_text


# ---------------------------------------------------------------------------
# Otros intents sin slot-filling
# ---------------------------------------------------------------------------
def test_precios_menu_no_hace_slot_filling(engine: SmartFlowEngine) -> None:
    result = engine.next_step(_state("main_menu"), "cuánto cuesta")
    assert result.flow_state == "precios_menu"
    # Mensaje directo, sin prompt de entidades
    assert result.reply_text


def test_fallback_en_main_menu(engine: SmartFlowEngine) -> None:
    result = engine.next_step(_state("main_menu"), "xyzxyz")
    assert result.flow_state == "main_menu"
    assert result.reply_text
