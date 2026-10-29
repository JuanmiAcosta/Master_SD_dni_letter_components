/**
 * @file dni_utils.h
 * @brief API pública de la librería para calcular y validar el DNI español.
 *
 * La letra de control se obtiene con el resto de dividir el número entre 23,
 * usado como índice en la tabla oficial `TRWAGMYFPDXBNJZSQVHLCKE`.
 *
 * Ejemplo de uso:
 * @code
 * #include "dni_utils.h"
 *
 * char letra = calcular_letra(12345678);   // 'Z'
 * bool ok    = validar_dni("12345678Z");   // true
 * @endcode
 */

#ifndef DNI_UTILS_H
#define DNI_UTILS_H

/// Valor mínimo admitido para la parte numérica del DNI.
const int DNI_NUMERO_MIN = 0;

/// Valor máximo admitido para la parte numérica del DNI (8 dígitos).
const int DNI_NUMERO_MAX = 99999999;

/**
 * @brief Calcula la letra de control de un número de DNI.
 *
 * @param numero Parte numérica del DNI, entre ::DNI_NUMERO_MIN y ::DNI_NUMERO_MAX.
 * @return La letra de control en mayúscula.
 * @throws std::out_of_range Si @p numero está fuera de rango.
 */
char calcular_letra(int numero);

/**
 * @brief Comprueba si un DNI completo es válido.
 *
 * Se aceptan exactamente 8 dígitos seguidos de una letra (mayúscula o
 * minúscula). Se ignoran los espacios al principio y al final.
 *
 * @param dni Cadena terminada en nulo con el DNI, p. ej. `"12345678Z"`.
 *            Puede ser `nullptr`.
 * @return `true` si el formato es correcto y la letra coincide;
 *         `false` en cualquier otro caso (nunca lanza excepciones).
 */
bool validar_dni(const char* dni);

#endif // DNI_UTILS_H
