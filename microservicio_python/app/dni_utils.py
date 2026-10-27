"""Lógica de negocio para el cálculo y la validación del DNI español.

Este módulo no depende de FastAPI, de modo que puede reutilizarse desde
cualquier otro programa Python.

La letra de control se obtiene con el resto de dividir el número entre 23,
usado como índice en la tabla oficial ``TRWAGMYFPDXBNJZSQVHLCKE``.
"""

import re

LETRAS = "TRWAGMYFPDXBNJZSQVHLCKE"
NUMERO_MIN = 0
NUMERO_MAX = 99_999_999

_PATRON_DNI = re.compile(r"^(\d{8})([A-Za-z])$")


def calcular_letra(numero: int) -> str:
    """Calcula la letra de control de un número de DNI.

    :param numero: parte numérica del DNI, entre 0 y 99 999 999.
    :return: la letra de control en mayúscula.
    :raises ValueError: si el número está fuera de rango.
    :raises TypeError: si ``numero`` no es un entero.
    """
    if isinstance(numero, bool) or not isinstance(numero, int):
        raise TypeError("El número debe ser un entero")
    if not NUMERO_MIN <= numero <= NUMERO_MAX:
        raise ValueError(f"El número debe estar entre {NUMERO_MIN} y {NUMERO_MAX}")
    return LETRAS[numero % 23]


def formatear_dni(numero: int) -> str:
    """Devuelve el DNI completo (8 dígitos con ceros a la izquierda + letra)."""
    return f"{numero:08d}{calcular_letra(numero)}"


def validar_dni(dni: str) -> bool:
    """Comprueba si un DNI completo es válido.

    Se aceptan exactamente 8 dígitos seguidos de una letra (mayúscula o
    minúscula). Se ignoran los espacios al principio y al final.

    :param dni: cadena con el DNI, p. ej. ``"12345678Z"``.
    :return: ``True`` si el formato es correcto y la letra coincide.
    """
    if not isinstance(dni, str):
        return False
    coincidencia = _PATRON_DNI.match(dni.strip())
    if coincidencia is None:
        return False
    numero, letra = coincidencia.groups()
    return calcular_letra(int(numero)) == letra.upper()
