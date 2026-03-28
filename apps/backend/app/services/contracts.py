from typing import TypedDict


class VacacionesData(TypedDict):
    dias_disponibles: int


class AvisoEnfermedadData(TypedDict):
    fecha: str
    hora: str
    estado: str
