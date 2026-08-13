# AIACO Corp
## Laboratorio de Gestión de Superficie de Ataque (ASM)

# Caso de Estudio

## Incidente AIACO-2026-001

### Descripción

Durante una revisión rutinaria de los activos digitales de AIACO Corp se detectó la posible exposición de información sensible relacionada con usuarios corporativos.

La investigación preliminar identificó una base de datos de desarrollo que contenía información de autenticación utilizada para pruebas internas. Dicha base de datos permanecía accesible desde un entorno que no contaba con los controles de seguridad esperados para un ambiente de desarrollo.

Como resultado de esta exposición, un tercero no autorizado logró obtener una copia de una tabla denominada **leaked_credentials**, la cual contenía direcciones de correo electrónico corporativas junto con información relacionada con sus credenciales.

Hasta este momento se desconoce si la información fue utilizada para acceder a otros sistemas de la organización; sin embargo, la existencia de contraseñas débiles y mecanismos de almacenamiento inseguros representa un riesgo importante para la infraestructura tecnológica de AIACO Corp.

---

# Objetivo del laboratorio

Como integrante del equipo de Ciberseguridad de AIACO Corp, deberás realizar el análisis técnico del incidente para determinar:

- Qué información fue comprometida.
- Qué debilidades permitieron la exposición de la base de datos.
- Qué riesgos representan las credenciales filtradas.
- Qué impacto tendría el incidente para la organización.
- Qué controles de seguridad deberán implementarse posteriormente.

En esta primera fase únicamente se realizará el reconocimiento del incidente y el análisis de la evidencia disponible.

No se implementarán acciones correctivas hasta finalizar el proceso de investigación.

---

# Evidencia disponible

Base de datos:

```
aiaco
```

Tabla comprometida:

```
leaked_credentials
```

Número de registros afectados:

```
5
```

Información almacenada:

- Correo corporativo
- Hash MD5 de contraseña
- Contraseña en texto plano (en algunos registros)

---

# Información disponible para el análisis

El equipo de respuesta a incidentes cuenta únicamente con una copia de la base de datos obtenida del servidor afectado.

No existe información adicional sobre el atacante ni sobre el vector de acceso utilizado.

Será responsabilidad del analista determinar el nivel de exposición y documentar los hallazgos durante el desarrollo del laboratorio.

# 🛡️ [ASM-03] Solución, Remediación y Análisis del Vector de Credenciales Corporativas

**Proyecto:** AIACO Corp – Attack Surface Management (ASM)  
**Vector:** Correos Corporativos y Gestión de Credenciales Exposibles (`emailscorp`)  
**Dominio Analizado:** `aiaco.local`

---

## 🔍 1. Diagnóstico de la Situación Inicial

Durante la auditoría del repositorio de credenciales simulado (`leaked_credentials`), se identificó una grave deficiencia en el almacenamiento y gestión de la identidad digital del personal de **AIACO Corp**.

### Hallazgos Principales:
1. **Almacenamiento de Contraseñas en Texto Plano (Severidad: CRÍTICA):**  
   3 de los 5 usuarios (60% de la muestra) mantenían sus contraseñas expuestas directamente sin ningún tipo de hashing (`laura.garcia`, `miguel.lopez`, `juan.torres`).
2. **Uso de Contraseñas Débiles/Triviales (Severidad: CRÍTICA):**  
   Se detectaron credenciales de alto riesgo como `password` y `123456`, vulnerables a ataques automatizados de fuerza bruta y *Credential Stuffing*.
3. **Uso de Criptografía Obsoleta (Severidad: MEDIA):**  
   2 usuarios (`alejandro.rodriguez`, `fernanda.silva`) almacenaban sus claves mediante **MD5**, un algoritmo criptográficamente roto y vulnerable a ataques de tablas arcoíris (*Rainbow Tables*).
4. **Patrón de Nombres de Usuario Predictible (Severidad: BAJA):**  
   Estructura estandarizada `nombre.apellido@aiaco.local`, lo que facilita la enumeración de usuarios por parte de un atacante.

---

## 📊 2. Matriz de Evaluación de Riesgo (Pre-Remediación)

| Usuario | Formato Credencial | Calificación de Riesgo | Impacto Potencial |
| :--- | :--- | :--- | :--- |
| `laura.garcia@aiaco.local` | Texto Plano (`password`) | **CRÍTICO** | Compromiso inmediato de cuenta / Acceso inicial. |
| `miguel.lopez@aiaco.local` | Texto Plano | **CRÍTICO** | Escalación lateral dentro del dominio. |
| `juan.torres@aiaco.local` | Texto Plano (`123456`) | **CRÍTICO** | Compromiso de credenciales por diccionario. |
| `alejandro.rodriguez@aiaco.local`| Hash MD5 | **MEDIO** | Reversión por fuerza bruta u offline cracking. |
| `fernanda.silva@aiaco.local` | Hash MD5 | **MEDIO** | Reversión por fuerza bruta u offline cracking. |

---

## 🛠️ 3. Estrategia de Remediación Aplicada

Para solucionar la vulnerabilidad sin destruir la evidencia forense ni afectar la continuidad operativa de los usuarios, se ejecutó una **remediación simulada por medio de duplicado y saneamiento de tabla**:

1. **Aislamiento de Evidencias:**  
   Se creó una réplica de la tabla denominada `leaked_credentials_backup`.
2. **Saneamiento de Datos Sensibles (Data Sanitization):**  
   Se ejecutó un borrado lógico de las contraseñas en texto plano, estableciendo su valor en `NULL`.

```sql
UPDATE leaked_credentials_backup
SET password_plain = NULL
WHERE password_plain IS NOT NULL;