# API DNI — Librería compartida (C++)

Librería que calcula la letra de control del DNI español y valida DNI completos.

- **Carpeta:** `libreria_cpp/`
- **Cabecera pública:** [`libreria_cpp/src/dni_utils.h`](../libreria_cpp/src/dni_utils.h)
- **Especificación:** Doxygen ([`libreria_cpp/docs/Doxyfile`](../libreria_cpp/docs/Doxyfile)), salida en `libreria_cpp/docs/html/`
- **Requisitos:** compilador con C++17 (g++), CMake ≥ 3.16; Doxygen para la documentación

## Compilación

Con CMake (desde `libreria_cpp/`):

```bash
cmake -S . -B build
cmake --build build
```

Genera la librería compartida `build/libdni_utils.so` y el cliente `build/prueba`.
Para una librería estática (`.a`):

```bash
cmake -S . -B build -DBUILD_SHARED_LIBS=OFF
cmake --build build
```

Solo con g++:

```bash
g++ -fPIC -shared src/dni_utils.cpp -o libdni_utils.so
g++ client/prueba.cpp -Isrc -L. -ldni_utils -o prueba
LD_LIBRARY_PATH=. ./prueba
```

## Funciones

### `char calcular_letra(int numero)` — Calcular letra

| Parámetro | Tipo  | Restricciones |
|-----------|-------|---------------|
| `numero`  | `int` | 0 – 99999999  |

Devuelve la letra de control en mayúscula.

```cpp
calcular_letra(12345678);   // 'Z'
calcular_letra(0);          // 'T'
```

### `bool validar_dni(const char* dni)` — Validar DNI

| Parámetro | Tipo          | Formato |
|-----------|---------------|---------|
| `dni`     | `const char*` | 8 dígitos + letra (mayúscula o minúscula) |

Devuelve `true` si el formato es correcto y la letra coincide. Se ignoran los
espacios al principio y al final.

```cpp
validar_dni("12345678Z");     // true
validar_dni(" 12345678z ");   // true
validar_dni("12345678A");     // false (letra incorrecta)
validar_dni("1234Z");         // false (formato incorrecto)
validar_dni(nullptr);         // false
```

### Constantes

| Constante        | Valor      |
|------------------|------------|
| `DNI_NUMERO_MIN` | `0`        |
| `DNI_NUMERO_MAX` | `99999999` |

### Errores

| Función          | Caso | Comportamiento |
|------------------|------|----------------|
| `calcular_letra` | `numero` fuera de rango | lanza `std::out_of_range` |
| `validar_dni`    | formato incorrecto, letra errónea o `nullptr` | devuelve `false` (nunca lanza) |

## Cliente incluido

```bash
./build/prueba                     # demo
./build/prueba letra 12345678      # Z
./build/prueba validar 12345678Z   # true
```

Códigos de salida: `0` correcto, `1` número fuera de rango o no numérico, `2` uso incorrecto.

## Uso desde otro programa C++

```cpp
#include "dni_utils.h"

#include <iostream>
#include <stdexcept>

using namespace std;

int main() {
    try {
        cout << calcular_letra(12345678) << '\n';           // Z
    } catch (const out_of_range& error) {
        cerr << error.what() << '\n';
    }
    cout << boolalpha << validar_dni("12345678Z") << '\n';  // true
}
```

Compilar enlazando con la librería:

```bash
g++ mi_programa.cpp -I<ruta>/libreria_cpp/src -L<ruta>/libreria_cpp/build -ldni_utils -o mi_programa
LD_LIBRARY_PATH=<ruta>/libreria_cpp/build ./mi_programa
```

Desde otro proyecto CMake:

```cmake
add_subdirectory(<ruta>/libreria_cpp dni_utils)
target_link_libraries(mi_programa PRIVATE dni_utils)
```

## Generar la documentación Doxygen

```bash
cd libreria_cpp/docs
doxygen Doxyfile
xdg-open html/index.html
```

O bien `cmake --build build --target docs` (disponible si CMake detecta Doxygen al configurar).
