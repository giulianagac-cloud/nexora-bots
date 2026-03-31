"""
EntityExtractor — extracción de entidades con regex para español.

Entidades soportadas:
  fecha  — días de la semana, "mañana", "pasado mañana", fechas DD/MM o "15 de abril"
  hora   — "las 3", "a las 10:30", "3pm", "15hs", "por la mañana/tarde/noche"
"""
from __future__ import annotations

import re
import unicodedata


def _normalize(text: str) -> str:
    nfd = unicodedata.normalize("NFD", text.lower().strip())
    return "".join(c for c in nfd if not unicodedata.combining(c))


# ---------------------------------------------------------------------------
# Patrones de fecha
# ---------------------------------------------------------------------------
_DIAS = r"(?:lunes|martes|miercoles|jueves|viernes|sabado|domingo)"
_MESES = (
    r"(?:enero|febrero|marzo|abril|mayo|junio|"
    r"julio|agosto|septiembre|octubre|noviembre|diciembre)"
)

_FECHA_PATTERNS: list[re.Pattern] = [
    # "el martes", "el lunes que viene"
    re.compile(rf"\b(?:el\s+)?({_DIAS})(?:\s+que\s+viene)?\b"),
    # "mañana", "pasado mañana" — excluye "por la mañana" y "a la mañana" (expresiones de hora)
    re.compile(r"(?<!por la )(?<!a la )\b(pasado\s+manana|manana)\b"),
    # "hoy"
    re.compile(r"\b(hoy)\b"),
    # "15 de abril", "3 de marzo"
    re.compile(rf"\b(\d{{1,2}}\s+de\s+{_MESES})\b"),
    # "15/04", "15/4/2025"
    re.compile(r"\b(\d{1,2}/\d{1,2}(?:/\d{2,4})?)\b"),
]

# ---------------------------------------------------------------------------
# Patrones de hora
# ---------------------------------------------------------------------------
_HORA_PATTERNS: list[re.Pattern] = [
    # "a las 10:30", "las 3:15"
    re.compile(r"\b(?:a\s+)?las\s+(\d{1,2}(?::\d{2})?)\b"),
    # "3pm", "10am" — antes del patrón genérico para evitar falsos negativos
    re.compile(r"\b(\d{1,2})\s*([ap]\.?m\.?)\b"),
    # "a las 3", "las 15", "9 hs"
    re.compile(r"\b(?:a\s+)?(?:las?\s+)?(\d{1,2})(?:\s*hs?\.?)?\b"),
    # "por la mañana/tarde/noche"
    re.compile(r"\b(por\s+la\s+(?:manana|tarde|noche))\b"),
    # "a la mañana/tarde/noche"
    re.compile(r"\b(a\s+la\s+(?:manana|tarde|noche))\b"),
]


class EntityExtractor:
    def extract(self, text: str) -> dict[str, str]:
        """
        Devuelve un dict con las entidades encontradas.
        Ejemplo: {"fecha": "martes", "hora": "3"}
        Solo incluye las claves de entidades efectivamente encontradas.
        """
        normalized = _normalize(text)
        entities: dict[str, str] = {}

        # --- Fecha -----------------------------------------------------------
        for pattern in _FECHA_PATTERNS:
            m = pattern.search(normalized)
            if m:
                entities["fecha"] = m.group(1).strip()
                break

        # --- Hora ------------------------------------------------------------
        # Evitamos matchear el número de fecha como hora.
        # Usamos el texto original normalizado pero enmascaramos la fecha ya encontrada.
        hora_text = normalized
        if "fecha" in entities:
            hora_text = hora_text.replace(entities["fecha"], "")

        for pattern in _HORA_PATTERNS:
            m = pattern.search(hora_text)
            if m:
                # Filtramos matches espurios de un solo dígito sin contexto horario
                # (e.g. "2 personas" no es una hora)
                raw = m.group(1).strip()
                # Si es solo un número, verificamos que haya contexto horario
                if raw.isdigit():
                    ctx = hora_text[max(0, m.start() - 15): m.end() + 15]
                    if not re.search(r"\b(?:las?|hs?|hora)\b|[ap]\.?m\.?\b", ctx):
                        continue
                entities["hora"] = raw
                break

        return entities
