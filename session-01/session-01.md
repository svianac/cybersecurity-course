# Sesión 01 --- Reconocimiento y análisis de autenticación web {#sesión-01--reconocimiento-y-análisis-de-autenticación-web}

**Fecha:** 22/11/2026\
**Laboratorio:** Linux Mint + Docker\
**Objetivos:** OWASP Juice Shop y DVWA\
**Herramienta principal:** Burp Suite Community\
**Navegador:** Firefox

------------------------------------------------------------------------

## 1. Objetivos de la sesión {#1-objetivos-de-la-sesión}

-   Comprobar que los servicios vulnerables del laboratorio estaban
    funcionando.
-   Identificar puertos y servicios mediante Nmap.
-   Observar peticiones HTTP con Burp Suite.
-   Analizar el inicio de sesión de Juice Shop.
-   Comprender el funcionamiento básico de la autenticación mediante
    JWT.
-   Comprobar cómo responde el servidor ante tokens ausentes o
    manipulados.

## 2. Entorno del laboratorio {#2-entorno-del-laboratorio}

El laboratorio está desplegado en Docker sobre Linux Mint.

  Aplicación         Dirección                   Puerto
  ------------------ ------------------------- --------
  OWASP Juice Shop   `http://127.0.0.1:3000`       3000
  DVWA               `http://127.0.0.1:8081`       8081

Los puertos están publicados en localhost para evitar exponer las
aplicaciones vulnerables a otros dispositivos de la red. MariaDB
funciona dentro de la red interna de Docker.

## 3. Reconocimiento con Nmap {#3-reconocimiento-con-nmap}

### Comando utilizado

``` bash
nmap -sV -sC -p 3000,8081 127.0.0.1
```

-   `-sV`: intenta identificar las versiones de los servicios.
-   `-sC`: ejecuta los scripts predeterminados de Nmap.
-   `-p`: especifica los puertos que se van a analizar.
-   `127.0.0.1`: analiza los servicios locales.

### Resultados obtenidos

**Puerto 3000 --- Juice Shop**

-   Puerto abierto.
-   Servicio HTTP.
-   Respuesta HTTP `200 OK`.
-   Se observaron cabeceras como:
    -   `Access-Control-Allow-Origin: *`
    -   `X-Content-Type-Options: nosniff`
    -   `X-Frame-Options: SAMEORIGIN`

Nmap no identificó inicialmente el servicio con precisión, pero se
confirmó que correspondía a Juice Shop mediante la aplicación y sus
respuestas HTTP.

**Puerto 8081 --- DVWA**

-   Puerto abierto.
-   Servicio HTTP.
-   Servidor Apache `2.4.69 (Debian)`.
-   Título de la página:
    `Login :: Damn Vulnerable Web Application (DVWA)`.
-   Se observó una entrada en `robots.txt` que deshabilita el rastreo de
    `/`.

### Observación sobre las cabeceras HTTP

Se observó:

``` http
Access-Control-Allow-Origin: *
```

Esto indica que el servidor anuncia una política CORS que permite
solicitudes desde cualquier origen para los recursos a los que se
aplique dicha política.

También se observó:

``` http
Access-Control-Allow-Methods: GET,HEAD,PUT,PATCH,POST,DELETE
```

Esta cabecera anuncia los métodos permitidos mediante CORS. No demuestra
por sí sola que todos esos métodos funcionen en todos los endpoints ni
que estén autorizados.

## 4. Primer contacto con Burp Suite {#4-primer-contacto-con-burp-suite}

Se configuró Firefox para utilizar Burp Suite como proxy HTTP/HTTPS.

Durante las primeras pruebas se observó que Firefox funcionaba
lentamente y algunas páginas no cargaban correctamente.

### Causa identificada

La opción `Intercept is on` de Burp puede detener las peticiones hasta
que se reenvían manualmente. Esto puede provocar que la página parezca
bloqueada o que algunas funcionalidades no respondan.

### Aprendizaje

-   Para navegar normalmente, utilizar `Intercept is off`.
-   Burp continúa registrando las peticiones en `Proxy → HTTP history`.
-   Activar la interceptación únicamente cuando se quiera detener y
    examinar una petición concreta.

## 5. Análisis de peticiones HTTP {#5-análisis-de-peticiones-http}

En Burp Suite se observaron diferentes peticiones generadas durante la
navegación.

Se identificó una petición de inicio de sesión:

``` http
POST /rest/user/login HTTP/1.1
Host: 127.0.0.1:3000
Content-Type: application/json
```

Cuerpo de ejemplo observado:

``` json
{
  "email": "test",
  "password": "test"
}
```

La petición enviaba las credenciales en formato JSON.

También se observaron cookies relacionadas con las preferencias y el
estado de la interfaz, como:

-   `language`
-   `welcomebanner_status`
-   `cookieconsent_status`

No se debe confundir estas cookies con el token de autenticación.

### Observación sobre HTTP

La aplicación del laboratorio se estaba utilizando mediante HTTP, sin
TLS. Por tanto, las peticiones pueden ser observadas en claro por
alguien que tenga acceso al tráfico correspondiente.

Esto no demuestra que se hayan utilizado credenciales reales ni que se
haya producido una filtración. Es una característica que conviene tener
presente al estudiar la seguridad de las comunicaciones.

## 6. Análisis del inicio de sesión y JWT {#6-análisis-del-inicio-de-sesión-y-jwt}

Durante el análisis de la petición `POST /rest/user/login` se observó
que el servidor devolvía un token de autenticación.

Posteriormente, las peticiones siguientes incorporaban una cabecera
similar a:

``` http
Authorization: Bearer <token>
```

Esto permitió identificar que Juice Shop utiliza autenticación mediante
tokens para mantener el estado autenticado del usuario.

### ¿Qué es un JWT?

JWT significa JSON Web Token. Es un formato utilizado para transmitir
información o claims entre partes.

Su estructura habitual tiene tres secciones separadas por puntos:

``` text
HEADER.PAYLOAD.SIGNATURE
```

-   **Header:** contiene información sobre el tipo de token y el
    algoritmo utilizado.
-   **Payload:** contiene los claims o datos asociados al token. Puede
    incluir identificadores, fechas de emisión, expiración y otros
    atributos.
-   **Signature:** permite verificar la integridad del token y comprobar
    que no ha sido manipulado.

El contenido del header y del payload normalmente está codificado en
Base64URL, no cifrado. Por eso no debe considerarse información secreta.

### Pruebas realizadas con Burp Suite

Se seleccionó una petición autenticada y se realizaron tres
comprobaciones.

#### Prueba A --- Token original {#prueba-a--token-original}

-   Se utilizó el token original recibido tras iniciar sesión.
-   La petición fue aceptada por el servidor.

**Resultado:** autenticación correcta.

#### Prueba B --- Petición sin token {#prueba-b--petición-sin-token}

-   Se eliminó la cabecera `Authorization`.
-   Se reenvió la petición.

Respuesta observada:

``` http
401 Unauthorized
```

**Interpretación:** el endpoint requiere autenticación y rechaza la
petición cuando no se presenta un token válido.

#### Prueba C --- Token modificado {#prueba-c--token-modificado}

-   Se modificó el token.
-   Se reenvió la petición.

El servidor indicó que el token no tenía una firma válida.

**Interpretación:** el servidor detectó que el token había sido
manipulado y rechazó la petición.

### Conclusión de las pruebas JWT

  Situación        Resultado
  ---------------- --------------------------
  Token original   Petición aceptada
  Sin token        `401 Unauthorized`
  Token alterado   Firma inválida y rechazo

Las pruebas permiten comprobar el comportamiento básico de
autenticación: el endpoint comprueba la presencia del token y valida su
firma.

Esto no demuestra todavía que todos los permisos, roles y endpoints
estén correctamente protegidos.

### Nota sobre un error 500 observado inicialmente

En una prueba inicial de modificación del token se observó un
`500 Internal Server Error`. En pruebas posteriores, al modificar el
token, el servidor indicó que la firma no era válida.

Por tanto, el error 500 queda como una observación inicial pendiente de
reproducir y analizar. No se considera demostrado que exista una
vulnerabilidad.

## 7. Herramientas utilizadas {#7-herramientas-utilizadas}

  Herramienta   Uso durante la sesión
  ------------- ---------------------------------------
  Nmap          Reconocimiento de puertos y servicios
  Firefox       Navegación por las aplicaciones
  Burp Suite    Interceptación y análisis HTTP
  Docker        Ejecución del laboratorio
  Juice Shop    Objetivo de análisis
  DVWA          Segundo objetivo disponible

## 8. Principales aprendizajes {#8-principales-aprendizajes}

Durante esta sesión he aprendido a:

1.  Realizar un reconocimiento básico de servicios web mediante Nmap.
2.  Identificar puertos abiertos y obtener información de los servicios.
3.  Interpretar algunas cabeceras HTTP y entender qué información
    proporcionan.
4.  Configurar Firefox para trabajar con Burp Suite.
5.  Diferenciar entre interceptar peticiones y simplemente registrarlas.
6.  Identificar una petición POST de inicio de sesión.
7.  Observar cómo se envían credenciales mediante JSON.
8.  Identificar el uso de tokens JWT.
9.  Reconocer la estructura de tres partes de un JWT.
10. Comprobar el comportamiento de una petición con token válido, sin
    token y con token manipulado.
11. Interpretar los códigos HTTP `200`, `401` y `500` en el contexto de
    las pruebas.

## 9. Aspectos pendientes para próximas sesiones {#9-aspectos-pendientes-para-próximas-sesiones}

-   Examinar el contenido del header y payload del JWT.
-   Identificar el algoritmo indicado en el campo `alg`.
-   Comprobar si existe una fecha de expiración (`exp`).
-   Identificar otros claims, como `iat`, `id`, `email` o `role`, si
    aparecen.
-   Analizar el comportamiento de la sesión cuando el token caduca.
-   Comprobar la autorización de diferentes recursos y endpoints.
-   Investigar el error 500 inicial si vuelve a reproducirse.
-   Continuar con las pruebas de seguridad de Juice Shop y DVWA.

## 10. Conclusión de la sesión {#10-conclusión-de-la-sesión}

La primera sesión ha permitido completar un reconocimiento inicial del
laboratorio y comenzar el análisis del funcionamiento interno de una
aplicación web.

Se han identificado los servicios de Juice Shop y DVWA, se ha
configurado Burp Suite como proxy de análisis y se ha observado el
proceso de autenticación de Juice Shop.

El hallazgo más importante ha sido identificar el uso de JWT y comprobar
experimentalmente que el servidor acepta el token original, rechaza las
peticiones sin autenticación y detecta tokens manipulados mediante la
validación de su firma.

La sesión se considera finalizada con los objetivos principales
cumplidos.

------------------------------------------------------------------------

**Estado:** Sesión 01 completada.

**Próxima sesión propuesta:** análisis de la estructura del JWT, sus
claims, algoritmo y expiración, seguido de una introducción al análisis
de autorización.
