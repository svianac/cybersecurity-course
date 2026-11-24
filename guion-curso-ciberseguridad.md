# Guion del curso de ciberseguridad

## Contexto y objetivo

Curso práctico de ciberseguridad en Linux Mint, orientado a un nivel
avanzado y organizado en 12 sesiones (aproximadamente 2--3 horas por
semana).

El objetivo es aprender a analizar aplicaciones web y redes, identificar
y validar vulnerabilidades en entornos propios, comprender cómo
funcionan los mecanismos de autenticación y autorización, y aplicar
medidas defensivas.

**Enfoque didáctico:** aprender mediante observación, hipótesis,
experimentación controlada, validación y documentación. No limitarse a
memorizar comandos.

**Alcance de seguridad:** realizar las prácticas únicamente en el
laboratorio propio o en sistemas para los que exista autorización
explícita.

## Entorno del laboratorio

-   Sistema anfitrión: Linux Mint.
-   Contenedores: Docker y Docker Compose.
-   Aplicaciones principales: OWASP Juice Shop y DVWA.
-   Base de datos: MariaDB para DVWA.
-   Burp Suite Community y Firefox para analizar tráfico web.

### Direcciones locales conocidas

  Aplicación         Dirección
  ------------------ -------------------------
  OWASP Juice Shop   `http://127.0.0.1:3000`
  DVWA               `http://127.0.0.1:8081`

Los puertos de las aplicaciones vulnerables están publicados en loopback
para evitar exponerlas a la red local. La base de datos permanece en la
red interna de Docker.

## Plan de 12 sesiones

### Sesión 1 --- Reconocimiento y análisis HTTP

**Estado: completada.**

-   Nmap: puertos, servicios y versiones.
-   HTTP: peticiones, respuestas y cabeceras.
-   Burp Suite: interceptación y análisis del tráfico.
-   Inicio de sesión y autenticación mediante JWT.
-   Comprobación de tokens válidos, ausentes y manipulados.

Hallazgos prácticos: - Juice Shop disponible en el puerto 3000 y DVWA en
el 8081. - Se identificó `POST /rest/user/login`. - La respuesta de
login contenía un token con estructura de tres secciones, compatible con
JWT. - Las peticiones posteriores incluían
`Authorization: Bearer <token>`. - Token original: petición aceptada. -
Sin token: respuesta `401 Unauthorized`. - Token alterado: rechazo por
firma no válida. - Se observó inicialmente un
`500 Internal Server Error` al modificar un token; quedó pendiente de
reproducir y analizar. - Se aprendió que `Intercept is on` puede detener
las peticiones; para navegar normalmente se puede dejar en
`Intercept is off` y consultar `Proxy → HTTP history`.

### Sesión 2 --- Análisis de JWT y autenticación

**Estado: completada; quedan verificaciones pendientes documentadas en
`session-02/session-02.md`.**

-   Estructura de JWT: Header, Payload y Signature.
-   Codificación Base64URL y diferencia entre codificación y cifrado.
-   Algoritmos de firma.
-   Claims habituales: `iat`, `exp`, `id`, `email`, `role`, si están
    presentes.
-   Expiración y ciclo de vida de los tokens.
-   Diferencia entre autenticación y autorización.
-   Análisis de sesiones con Burp Suite.

### Sesión 3 --- Redes y reconocimiento avanzado

-   TCP/IP, DNS y puertos.
-   Nmap avanzado.
-   Enumeración de servicios.
-   Wireshark y tcpdump.
-   Análisis del tráfico de red.

### Sesión 4 --- Enumeración web

-   Directorios y archivos ocultos.
-   Gobuster y FFUF.
-   Identificación de tecnologías.
-   Superficie de ataque.

### Sesión 5 --- Burp Suite avanzado

-   Proxy y HTTP History.
-   Repeater e Intruder.
-   Análisis de parámetros.
-   Manipulación controlada de peticiones.
-   Pruebas de autenticación y autorización.

### Sesión 6 --- OWASP Top 10

-   Principales categorías de vulnerabilidades web.
-   Fallos de control de acceso.
-   Errores de autenticación.
-   Configuraciones inseguras.
-   Componentes vulnerables.

### Sesión 7 --- Vulnerabilidades prácticas

-   SQL Injection.
-   Cross-Site Scripting (XSS).
-   Manipulación de entradas.
-   Validación y sanitización.
-   Pruebas en Juice Shop y DVWA.

### Sesión 8 --- Análisis automatizado

-   OWASP ZAP.
-   Nikto.
-   Escaneo de aplicaciones.
-   Interpretación de resultados.
-   Falsos positivos y validación manual.

### Sesión 9 --- API Security

-   REST y JSON.
-   Autenticación mediante tokens.
-   Autorización por recursos.
-   IDOR/BOLA.
-   Laboratorio práctico con APIs vulnerables.

### Sesión 10 --- Seguridad Linux

-   Usuarios y permisos.
-   SSH seguro.
-   Firewall.
-   Servicios y procesos.
-   Hardening del sistema.

### Sesión 11 --- Detección y monitorización

-   Wazuh.
-   Suricata.
-   Análisis de logs.
-   Detección de actividad sospechosa.
-   Alertas e incidentes.

### Sesión 12 --- Proyecto final: auditoría completa

-   Reconocimiento de Juice Shop.
-   Identificación de vulnerabilidades.
-   Validación de hallazgos.
-   Evaluación de riesgos.
-   Propuestas de mitigación.
-   Elaboración de un informe profesional de auditoría.

## Herramientas previstas

  Herramienta            Uso principal
  ---------------------- -----------------------------------------------
  Nmap                   Reconocimiento de redes y servicios
  Burp Suite Community   Análisis e inspección de tráfico web
  OWASP ZAP              Análisis de seguridad de aplicaciones web
  Wireshark              Análisis de tráfico
  tcpdump                Captura de paquetes desde terminal
  Gobuster               Enumeración de directorios y recursos
  FFUF                   Fuzzing y descubrimiento de recursos
  SQLmap                 Apoyo en pruebas controladas de SQL Injection
  Nikto                  Comprobaciones de seguridad en servidores web
  Metasploit Framework   Validación controlada de vulnerabilidades
  Wazuh                  Monitorización y detección
  Suricata               Detección de actividad de red

La incorporación de herramientas se hará progresivamente, según las
necesidades de cada sesión.

## Resultados de aprendizaje esperados

Al finalizar el curso, el alumno debería poder:

1.  Reconocer una infraestructura y sus servicios.
2.  Identificar tecnologías y puntos de entrada.
3.  Analizar aplicaciones web y APIs.
4.  Detectar y validar vulnerabilidades en entornos autorizados.
5.  Comprender los mecanismos de autenticación y autorización.
6.  Interpretar los resultados de herramientas de seguridad.
7.  Aplicar medidas de protección y hardening.
8.  Monitorizar sistemas y detectar actividades sospechosas.
9.  Documentar hallazgos en un informe técnico.

## Método de trabajo para cada sesión

Cada sesión debe incluir, en la medida de lo posible:

1.  **Objetivos:** qué se aprenderá y por qué.
2.  **Conceptos:** explicación breve de los fundamentos necesarios.
3.  **Preparación:** comprobación del laboratorio y herramientas.
4.  **Práctica guiada:** pasos y comandos explicados.
5.  **Validación:** observar resultados y contrastar hipótesis.
6.  **Análisis:** distinguir hechos observados de suposiciones.
7.  **Documentación:** registrar comandos, evidencias, resultados y
    conclusiones.
8.  **Cierre:** resumen de aprendizajes y preparación de la siguiente
    sesión.

El usuario prefiere avanzar paso a paso, con explicaciones didácticas y
sin introducir demasiadas herramientas de golpe. Cuando se elaboren
informes, deben quedar listos para guardar en Markdown.

## Continuidad: punto de partida de la próxima sesión

La siguiente sesión es la **Sesión 3 --- Redes y reconocimiento
avanzado**.

Retomar el programa con TCP/IP, DNS y puertos; ampliar el reconocimiento
con Nmap y analizar tráfico con Wireshark o tcpdump. La sesión 2 dejó
pendiente documentar la comparación entre el `data.id` de la cuenta
`customer` y el `UserId` de su cesta, así como investigar en una sesión
posterior si existe una política de expiración adicional a los claims
del token.

**Precaución:** tratar los JWT como credenciales mientras sean válidos.
No pegarlos en decodificadores públicos ni compartirlos completos. No
modificar ni atacar sistemas fuera del laboratorio autorizado.
