package client;

import com.example.DniUtils;

/**
 * Cliente de ejemplo de la librería de utilidades DNI.
 */
public class Main {

    public static void main(String[] args) {
        System.out.println(
            "La letra del DNI 12345678 es: " + DniUtils.calcularLetra(12345678)
        );

        System.out.println(
            "¿El DNI 12345678 es válido?: " + DniUtils.validarDni("12345678Z")
        );
    }
}
