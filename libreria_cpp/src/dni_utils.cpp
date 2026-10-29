/**
 * @file dni_utils.cpp
 * @brief Implementación de las funciones declaradas en dni_utils.h.
 */

#include "dni_utils.h"

#include <cctype>
#include <cstring>
#include <stdexcept>
#include <string>

using namespace std;

/// Tabla oficial de letras de control, indexada por `numero % 23`.
static const char LETRAS[] = "TRWAGMYFPDXBNJZSQVHLCKE";

char calcular_letra(int numero) {
    if (numero < DNI_NUMERO_MIN || numero > DNI_NUMERO_MAX) {
        throw out_of_range("El número debe estar entre " + to_string(DNI_NUMERO_MIN)
                           + " y " + to_string(DNI_NUMERO_MAX));
    }
    return LETRAS[numero % 23];
}

bool validar_dni(const char* dni) {
    if (dni == nullptr) {
        return false;
    }

    // Recortar espacios al principio y al final.
    const char* inicio = dni;
    const char* fin = dni + strlen(dni);
    while (inicio < fin && isspace(static_cast<unsigned char>(*inicio))) {
        ++inicio;
    }
    while (fin > inicio && isspace(static_cast<unsigned char>(fin[-1]))) {
        --fin;
    }

    // Formato: exactamente 8 dígitos + 1 letra.
    if (fin - inicio != 9) {
        return false;
    }
    int numero = 0;
    for (int i = 0; i < 8; ++i) {
        if (!isdigit(static_cast<unsigned char>(inicio[i]))) {
            return false;
        }
        numero = numero * 10 + (inicio[i] - '0');
    }
    unsigned char letra = static_cast<unsigned char>(inicio[8]);
    if (!isalpha(letra)) {
        return false;
    }

    return calcular_letra(numero) == toupper(letra);
}
