import pytest

from app.services.entity_extractor import EntityExtractor


@pytest.fixture
def extractor() -> EntityExtractor:
    return EntityExtractor()


# ---------------------------------------------------------------------------
# Fecha
# ---------------------------------------------------------------------------
class TestFecha:
    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            ("quiero un turno el lunes", "lunes"),
            ("el martes que viene", "martes"),
            ("el viernes a las 3", "viernes"),
            ("mañana a la mañana", "manana"),
            ("pasado mañana", "pasado manana"),
            ("hoy no puedo", "hoy"),
            ("el 15 de abril", "15 de abril"),
            ("el 3 de marzo por la tarde", "3 de marzo"),
            ("el 15/04", "15/04"),
            ("reserva para el 15/4/2025", "15/4/2025"),
        ],
    )
    def test_extrae_fecha(self, extractor: EntityExtractor, text: str, expected: str) -> None:
        result = extractor.extract(text)
        assert result.get("fecha") == expected

    def test_sin_fecha_no_incluye_clave(self, extractor: EntityExtractor) -> None:
        result = extractor.extract("quiero hablar con alguien")
        assert "fecha" not in result


# ---------------------------------------------------------------------------
# Hora
# ---------------------------------------------------------------------------
class TestHora:
    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            ("a las 10:30", "10:30"),
            ("las 3", "3"),
            ("a las 15", "15"),
            ("a las 9 de la mañana", "9"),
            ("3pm", "3"),
            ("10am", "10"),
            ("por la tarde", "por la tarde"),
            ("a la noche", "a la noche"),
            ("por la mañana", "por la manana"),
        ],
    )
    def test_extrae_hora(self, extractor: EntityExtractor, text: str, expected: str) -> None:
        result = extractor.extract(text)
        assert result.get("hora") == expected

    def test_sin_hora_no_incluye_clave(self, extractor: EntityExtractor) -> None:
        result = extractor.extract("quiero un turno el lunes")
        assert "hora" not in result


# ---------------------------------------------------------------------------
# Combinados
# ---------------------------------------------------------------------------
class TestCombinados:
    def test_extrae_fecha_y_hora_juntas(self, extractor: EntityExtractor) -> None:
        result = extractor.extract("quiero turno el martes a las 10:30")
        assert result["fecha"] == "martes"
        assert result["hora"] == "10:30"

    def test_fecha_no_contamina_hora(self, extractor: EntityExtractor) -> None:
        # "15 de abril" no debe leerse como hora "15"
        result = extractor.extract("turno el 15 de abril a las 9")
        assert result["fecha"] == "15 de abril"
        assert result["hora"] == "9"

    def test_numero_sin_contexto_horario_no_es_hora(self, extractor: EntityExtractor) -> None:
        result = extractor.extract("somos 2 personas")
        assert "hora" not in result

    def test_texto_sin_entidades_devuelve_dict_vacio(self, extractor: EntityExtractor) -> None:
        result = extractor.extract("hola, ¿cómo estás?")
        assert result == {}
