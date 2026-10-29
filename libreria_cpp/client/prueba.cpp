/**
 * @file prueba.cpp
 * @brief Cliente de línea de comandos que consume la librería dni_utils.
 *
 * Uso:
 * @code{.sh}
 * ./prueba                     # demo
 * ./prueba letra 12345678      # Z
 * ./prueba validar 12345678Z   # true
 * @endcode
 */

#include "dni_utils.h"

#include <cstring>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>

using namespace std;

/// Mensaje de ayuda que se muestra si los argumentos no son válidos.
static const char* USO =
    "Uso:\n"
    "  prueba                     ejecuta una demo\n"
    "  prueba letra <numero>      calcula la letra de control\n"
    "  prueba validar <dni>       valida un DNI completo\n";

/// Muestra algunos ejemplos de uso de la librería.
static void demo() {
    for (int numero : {12345678, 0, 87654321}) {
        cout << "Letra de " << setw(8) << setfill('0') << numero << ": "
             << calcular_letra(numero) << '\n';
    }
    for (const char* dni : {"12345678Z", "12345678A", "1234Z"}) {
        cout << "¿" << dni << " es válido? " << boolalpha << validar_dni(dni) << '\n';
    }
}

/**
 * @brief Punto de entrada del cliente.
 *
 * @param argc Número de argumentos.
 * @param argv Argumentos: ninguno (demo), `letra <numero>` o `validar <dni>`.
 * @return 0 si todo va bien, 1 si el número no es válido, 2 si el uso es incorrecto.
 */
int main(int argc, char* argv[]) {
    if (argc == 1) {
        demo();
        return 0;
    }
    if (argc == 3 && strcmp(argv[1], "letra") == 0) {
        try {
            size_t leidos = 0;
            int numero = stoi(argv[2], &leidos);
            if (leidos != strlen(argv[2])) {
                throw invalid_argument("no numérico");
            }
            cout << calcular_letra(numero) << '\n';
            return 0;
        } catch (const out_of_range& error) {
            cerr << "Error: " << error.what() << '\n';
        } catch (const invalid_argument&) {
            cerr << "Error: '" << argv[2] << "' no es un número entero\n";
        }
        return 1;
    }
    if (argc == 3 && strcmp(argv[1], "validar") == 0) {
        cout << boolalpha << validar_dni(argv[2]) << '\n';
        return 0;
    }
    cerr << USO;
    return 2;
}
