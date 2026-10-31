package com.example;

/**
 * Utilidades para calcular y validar DNIs españoles.
 */
public class DniUtils {

    private static final String LETRAS = "TRWAGMYFPDXBNJZSQVHLCKE";
    private static final int NUMERO_MIN = 0;
    private static final int NUMERO_MAX = 99999999;

    /**
     * Calcula la letra de control correspondiente a la parte numérica del DNI.
     *
     * @param numero número del DNI, entre 0 y 99999999
     * @return letra de control en mayúscula
     * @throws IllegalArgumentException si el número está fuera de rango
     */
    public static char calcularLetra(int numero) {
        if(numero < NUMERO_MIN || numero > NUMERO_MAX) {
            throw new IllegalArgumentException(
                    "El número debe estar entre " + NUMERO_MIN + " y " + NUMERO_MAX
                );
        }

        return LETRAS.charAt(numero % LETRAS.length());
    }

    /**
     * Comprueba si un DNI tiene un formato válido y su letra es correcta.
     * Se aceptan letras mayúsculas o minúsculas y espacios al principio o al final.
     *
     * @param dni DNI completo, con ocho dígitos y una letra
     * @return {@code true} si el DNI es válido; {@code false} en caso contrario
     */
    public static boolean validarDni(String dni) {
        if(dni == null) {
            return false;
        }

        String dniNormalizado = dni.strip();

        if(!dniNormalizado.matches("\\d{8}[A-Za-z]")) {
            return false;
        }

        int numero = Integer.parseInt(dniNormalizado.substring(0, 8));
        char letra = dniNormalizado.charAt(8);

        return calcularLetra(numero) == Character.toUpperCase(letra);
    }
}
