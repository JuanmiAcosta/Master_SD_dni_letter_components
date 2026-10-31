# API DNI — Librería Java

Librería Java reutilizable para calcular la letra de un DNI español y validar DNIs completos.

- **Código de la librería:** `libreria_java/lib/src/main/java/com/example/DniUtils.java`
- **Cliente de ejemplo:** `libreria_java/client/Main.java`
- **Paquete de la librería:** `com.example`
- **Salida de compilación:** `build/`
- **JAR generado:** `build/dni-utils.jar`
- **Documentación generada:** `docs/javadoc/index.html`

## API pública

### `calcularLetra(int numero)` — Calcular letra

Calcula la letra correspondiente a la parte numérica del DNI. El número debe
estar entre `0` y `99999999`, incluidos.

```java
char letra = DniUtils.calcularLetra(12345678); // 'Z'
```

Si el número está fuera de rango, se lanza `IllegalArgumentException`.

### `validarDni(String dni)` — Validar DNI

Comprueba que el DNI tenga ocho dígitos, una letra correcta y un formato
válido. Se aceptan letras mayúsculas o minúsculas y espacios al principio o al
final.

```java
boolean valido = DniUtils.validarDni("12345678Z"); // true
```

Un formato incorrecto, una letra errónea o un valor `null` devuelve `false`.

## Compilación de la librería

La carpeta `libreria_java` no utiliza Maven ni Gradle. Desde este repositorio, se ejecutarán los siguientes comandos.

Primero se crea una carpeta para las clases compiladas:

```bash
mkdir -p build/classes
```

Después se compila la clase `DniUtils`:

```bash
javac -d build/classes \
  lib/src/main/java/com/example/DniUtils.java
```

La opción `-d` indica dónde se guardan los archivos `.class`. Java crea
automáticamente la estructura correspondiente al paquete `com.example`.

## Creación de la librería `.jar`

Una vez compilada la clase, se empaqueta como una librería Java:

```bash
jar --create \
  --file build/dni-utils.jar \
  -C build/classes .
```

El archivo `build/dni-utils.jar` es el componente reutilizable que se puede
distribuir a otros programas Java.

## Generación de la documentación JavaDoc

La documentación se genera a partir de los comentarios JavaDoc de `DniUtils`:

```bash
javadoc -d docs/javadoc \
  lib/src/main/java/com/example/DniUtils.java
```

El resultado es un sitio web HTML. El archivo principal es:

```text
docs/javadoc/index.html
```

Se puede abrir con un navegador. La documentación describe la clase, los
métodos públicos, sus parámetros, valores devueltos y excepciones.

## Compilación y ejecución del cliente

El cliente [Main.java](../libreria_java/client/Main.java) no forma parte de la
librería. Es un programa independiente que demuestra cómo utilizar el JAR.

Se compila indicando el JAR en el `classpath`:

```bash
javac -cp build/dni-utils.jar \
  -d build/classes \
  client/Main.java
```

Se ejecuta incluyendo tanto el JAR como las clases compiladas del cliente:

```bash
java -cp build/dni-utils.jar:build/classes client.Main
```

La salida esperada es similar a:

```text
La letra del DNI 12345678 es: Z
¿El DNI 12345678 es válido?: true
```

## Uso por consumidores Java

Un consumidor solo necesita recibir `build/dni-utils.jar` e importarlo:

```java
import com.example.DniUtils;

public class Aplicacion {
    public static void main(String[] args) {
        char letra = DniUtils.calcularLetra(12345678);
        boolean valido = DniUtils.validarDni("12345678Z");
    }
}
```

Al compilar su programa debe añadir el JAR al `classpath`:

```bash
javac -cp ruta/al/dni-utils.jar Aplicacion.java
```

Y al ejecutarlo debe volver a incluirlo:

```bash
java -cp ruta/al/dni-utils.jar:. Aplicacion
```

En un proyecto Maven o Gradle, el consumidor puede instalar el JAR en un
repositorio de artefactos y declararlo como dependencia. En ese caso, el
gestor de dependencias configura automáticamente el `classpath`.
