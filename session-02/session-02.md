# Sesión 02 --- Análisis de JWT y autenticación {#sesión-02--análisis-de-jwt-y-autenticación}

**Fecha:** 24/11/2026  
**Laboratorio:** Linux Mint + Docker  
**Objetivo:** OWASP Juice Shop en `http://127.0.0.1:3000`  
**Herramientas principales:** Burp Suite Community, Firefox y un script local de Python

------------------------------------------------------------------------

## 1. Objetivos de la sesión

- Examinar las secciones Header y Payload de un JWT.
- Comprender Base64URL, los algoritmos de firma y los claims.
- Observar la emisión y reutilización de tokens.
- Diferenciar autenticación de autorización.
- Analizar el acceso a recursos de cesta con Burp Suite.

## 2. Entorno y precauciones

Se trabajó contra la instancia local de OWASP Juice Shop. Los tokens se
trataron como credenciales: no se incluyeron en este informe ni se
utilizaron decodificadores públicos. Los valores identificativos y
personales del payload se omiten.

## 3. Decodificación local del JWT

### Comandos utilizados

```bash
python3 scripts/python-jwt-decoder.py
date -d "@1795549022"
date -u -d "@1795549022"
```

El script permitió leer localmente el Header y el Payload. El valor Unix
de `iat` se mostró en hora local y en UTC; la diferencia observada fue
de una hora, coherente con la zona CET del equipo frente a UTC. El claim
`createdAt` describe la creación del registro de usuario, mientras que
`iat` describe la emisión del token; no son el mismo evento.

### Header y algoritmo

El Header observado contenía:

```json
{
  "typ": "JWT",
  "alg": "RS256"
}
```

`RS256` identifica una firma RSA con SHA-256. La firma permite verificar
la integridad y autenticidad del token; no cifra su contenido. No se
realizaron pruebas de manipulación del algoritmo ni de claves.

### Payload y claims

El Payload contenía un objeto de usuario anidado bajo `data`, un claim
`bid` y el claim `iat`. Se observaron, entre otros, campos de identidad y
de perfil, un rol y fechas de cuenta. Un payload incluía un campo llamado
`password` cuyo valor observado era un marcador (`deleted`); esto no
demuestra que se haya expuesto una contraseña válida, pero incluir un
campo de contraseña en un token es una señal de diseño que merece
revisión.

El token de la cuenta administrativa indicaba el rol `admin`. En una
prueba posterior se usó una cuenta de rol `customer`. No se incluyeron
emails, tokens ni otros datos personales en estas notas.

Base64URL es una codificación, no cifrado: quien obtiene un JWT puede
decodificar su Header y Payload. No debe usarse para ocultar información
secreta.

## 4. Emisión y ciclo de vida del token

- Las peticiones posteriores al login reutilizaban el mismo token.
- Tras cerrar sesión e iniciar de nuevo, se observó un token distinto y
  un valor `iat` nuevo.
- No se observó el claim estándar `exp` en los payloads analizados.
- No se esperó a que un token caducara ni se comprobó una política de
  expiración del servidor independiente del JWT.

La ausencia de `exp` significa que no se vio una fecha de expiración en
el Payload; no demuestra que el token nunca caduque.

## 5. Autenticación y respuesta ante peticiones

En Burp se analizó `POST /api/BasketItems/`:

- Con la cabecera de autorización, la operación inicial fue aceptada.
- Al repetir el POST con el mismo producto, el servidor respondió `500`
  con el mensaje `ProductId must be unique`.
- Al quitar la cabecera `Authorization`, la respuesta fue `401
  Unauthorized`.

El `401` observado indica que esa operación requiere autenticación. El
`500` ocurrió al repetir una operación que violaba la regla de unicidad
observada; por sí solo no demuestra una vulnerabilidad, aunque es una
respuesta de error de aplicación que se puede documentar.

## 6. Autorización de acceso a cestas

Se consultó `GET /rest/basket/1`. La primera respuesta fue `304 Not
Modified`; al repetir la consulta sin las cabeceras condicionales de
caché, se obtuvo `200 OK` con datos de cesta y `UserId`.

Después, con una cuenta de rol `customer` y el mismo token:

- `GET /rest/basket/6` permitió consultar la cesta asociada a esa cuenta.
- Las consultas a `/rest/basket/2` y `/rest/basket/1` también devolvieron
  datos de cesta con los `UserId` correspondientes a esos recursos.

### Interpretación

Autenticación responde quién realiza la petición; autorización decide
qué recursos puede consultar o modificar. Que un token sea aceptado no
significa que el acceso a todos los identificadores esté autorizado.

El acceso de una cuenta `customer` a varias cestas constituye evidencia
de un posible BOLA/IDOR de lectura. Para dejar documentada la relación de
propiedad sin ambigüedad, queda pendiente cotejar el `data.id` de esa
cuenta con el `UserId` de `/rest/basket/6` y confirmar que los `UserId`
de las otras respuestas son distintos. No se probaron operaciones de
escritura o eliminación sobre cestas ajenas.

## 7. Aprendizajes

1. Un JWT suele tener Header, Payload y Signature.
2. Base64URL no cifra los datos del Payload.
3. `iat` es un claim estándar de emisión; `exp` no apareció en los tokens
   observados.
4. `bid` y el objeto `data` son datos específicos de la aplicación; no
   deben confundirse automáticamente con claims estándar.
5. Un `401` por falta de token es una comprobación de autenticación, no
   prueba de que los controles de autorización sean correctos.
6. La autorización debe comprobarse por recurso, no inferirse solo del
   rol o de que la petición esté autenticada.
7. Una respuesta `200` al consultar una cesta ajena puede indicar un
   control de acceso por objeto deficiente; hay que verificar la
   identidad propietaria y registrar el alcance exacto.

## 8. Conclusiones y ejercicios pendientes

Se completó el análisis básico de JWT y autenticación de la sesión. Se
observó `RS256`, se identificó información legible en el Payload, se
comparó el comportamiento entre peticiones autenticadas y sin token, y
se encontró evidencia de posible acceso de lectura entre cestas.

Pendiente:

- Comparar `data.id` de la cuenta `customer` con el `UserId` de su cesta
  propia y registrar la comparación con las otras cestas.
- Investigar en una sesión posterior si existe una política de
  expiración del servidor, sin asumir que la ausencia de `exp` implica
  duración ilimitada.
- No modificar ni eliminar recursos de otras cuentas durante estas
  comprobaciones.

------------------------------------------------------------------------

**Estado:** Sesión 02 completada; quedan pendientes las verificaciones
indicadas para cerrar el hallazgo de autorización y el ciclo de vida.

**Próxima sesión propuesta:** redes y reconocimiento avanzado.
