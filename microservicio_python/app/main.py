"""API REST (FastAPI) que expone las funciones de :mod:`app.dni_utils`.

Arranque::

    uvicorn app.main:app --reload

Documentación interactiva en http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

from app import dni_utils

app = FastAPI(
    title="API DNI",
    version="1.0.0",
    description="Microservicio para calcular la letra y validar el DNI español.",
)


class LetraRespuesta(BaseModel):
    numero: int = Field(..., examples=[12345678])
    letra: str = Field(..., min_length=1, max_length=1, examples=["Z"])
    dni: str = Field(..., description="DNI completo con 8 dígitos", examples=["12345678Z"])


class ValidacionRespuesta(BaseModel):
    dni: str = Field(..., examples=["12345678Z"])
    valido: bool = Field(..., examples=[True])


@app.post(
    "/dni/{numero}",
    response_model=LetraRespuesta,
    summary="Calcula la letra de un DNI",
    tags=["dni"],
)
def calcular_letra(
    numero: int = Path(
        ...,
        ge=dni_utils.NUMERO_MIN,
        le=dni_utils.NUMERO_MAX,
        description="Parte numérica del DNI (0 - 99999999)",
        examples=[12345678],
    ),
) -> LetraRespuesta:
    """Devuelve la letra de control correspondiente al número indicado."""
    letra = dni_utils.calcular_letra(numero)
    return LetraRespuesta(numero=numero, letra=letra, dni=dni_utils.formatear_dni(numero))


@app.get(
    "/dni/validar",
    response_model=ValidacionRespuesta,
    summary="Valida un DNI completo",
    tags=["dni"],
)
def validar_dni(
    dni: str = Query(
        ...,
        description="DNI completo: 8 dígitos y letra",
        examples=["12345678Z"],
    ),
) -> ValidacionRespuesta:
    """Indica si el DNI tiene formato correcto y la letra coincide con el número."""
    return ValidacionRespuesta(dni=dni, valido=dni_utils.validar_dni(dni))
