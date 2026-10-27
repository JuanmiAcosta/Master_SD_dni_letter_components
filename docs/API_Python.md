# API DNI — Microservicio REST (Python / FastAPI)

Microservicio que calcula la letra de control del DNI español y valida DNI completos.

- **Carpeta:** `microservicio_python/`
- **Especificación:** [`microservicio_python/docs/openapi.yaml`](../microservicio_python/docs/openapi.yaml) (OpenAPI 3.1)
- **URL base por defecto:** `http://127.0.0.1:8000`

## Instalación y arranque

```bash
cd microservicio_python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Con el servidor arrancado, la documentación interactiva está en:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Especificación JSON: http://127.0.0.1:8000/openapi.json

## Endpoints

### `POST /dni/{numero}` — Calcular letra

| Parámetro | Ubicación | Tipo | Restricciones |
|-----------|-----------|------|---------------|
| `numero`  | ruta      | entero | 0 – 99999999 |

```bash
curl -X POST http://127.0.0.1:8000/dni/12345678
```

Respuesta `200`:

```json
{ "numero": 12345678, "letra": "Z", "dni": "12345678Z" }
```

El campo `dni` se devuelve siempre con 8 dígitos (`/dni/1` → `"00000001R"`).

### `GET /dni/validar?dni=...` — Validar DNI

| Parámetro | Ubicación | Tipo | Formato |
|-----------|-----------|------|---------|
| `dni`     | query     | texto | 8 dígitos + letra (mayúscula o minúscula) |

```bash
curl "http://127.0.0.1:8000/dni/validar?dni=12345678Z"
```

Respuesta `200`:

```json
{ "dni": "12345678Z", "valido": true }
```

Un DNI con formato incorrecto o letra errónea devuelve `"valido": false` (no es un error HTTP).

### Errores

| Código | Causa |
|--------|-------|
| `422`  | `numero` fuera de rango o no numérico; falta el parámetro `dni` |

## Clientes incluidos

```bash
# Cliente Python (usa httpx)
python client/client.py                     # demo
python client/client.py letra 12345678      # Z
python client/client.py validar 12345678Z   # True

# Cliente curl
./client/client.sh [URL_BASE]
```

Ambos aceptan otra URL mediante la variable de entorno `API_URL`.

## Uso desde código Python

Consumiendo el servicio, con la clase `DniClient` de `client/client.py`:

```python
from client.client import DniClient   # ejecutado desde microservicio_python/

cliente = DniClient("http://127.0.0.1:8000")
cliente.calcular_letra(12345678)   # 'Z'
cliente.validar_dni("12345678Z")   # True
```

La lógica también puede reutilizarse sin servidor, importando el módulo `app/dni_utils.py`:

```python
from app.dni_utils import calcular_letra, validar_dni

calcular_letra(12345678)   # 'Z'  (ValueError si está fuera de rango)
validar_dni("12345678Z")   # True
```

## Regenerar `openapi.yaml`

FastAPI genera la especificación a partir del código. Tras modificar `app/main.py`:

```bash
python -c "
import yaml
from app.main import app
with open('docs/openapi.yaml', 'w', encoding='utf-8') as f:
    yaml.safe_dump(app.openapi(), f, allow_unicode=True, sort_keys=False)
"
```
