"""Cliente de ejemplo que consume el microservicio DNI.

Uso::

    python client/client.py                       # demo
    python client/client.py letra 12345678
    python client/client.py validar 12345678Z
    API_URL=http://otro-host:8000 python client/client.py letra 1
"""

import os
import sys

import httpx

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")


class DniClient:
    """Envoltorio sencillo sobre la API REST."""

    def __init__(self, base_url: str = API_URL, timeout: float = 5.0):
        self._http = httpx.Client(base_url=base_url, timeout=timeout)

    def calcular_letra(self, numero: int) -> str:
        respuesta = self._http.post(f"/dni/{numero}")
        respuesta.raise_for_status()
        return respuesta.json()["letra"]

    def validar_dni(self, dni: str) -> bool:
        respuesta = self._http.get("/dni/validar", params={"dni": dni})
        respuesta.raise_for_status()
        return respuesta.json()["valido"]

    def close(self) -> None:
        self._http.close()


def demo(cliente: DniClient) -> None:
    for numero in (12345678, 0, 87654321):
        print(f"Letra de {numero:08d}: {cliente.calcular_letra(numero)}")
    for dni in ("12345678Z", "12345678A", "1234Z"):
        print(f"¿{dni} es válido? {cliente.validar_dni(dni)}")


def main(argv: list[str]) -> int:
    cliente = DniClient()
    try:
        if len(argv) == 0:
            demo(cliente)
        elif len(argv) == 2 and argv[0] == "letra":
            print(cliente.calcular_letra(int(argv[1])))
        elif len(argv) == 2 and argv[0] == "validar":
            print(cliente.validar_dni(argv[1]))
        else:
            print(__doc__, file=sys.stderr)
            return 2
    except httpx.HTTPStatusError as error:
        print(f"Error {error.response.status_code}: {error.response.text}", file=sys.stderr)
        return 1
    except httpx.ConnectError:
        print(f"No se pudo conectar con {API_URL}. ¿Está arrancado el servidor?", file=sys.stderr)
        return 1
    finally:
        cliente.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
