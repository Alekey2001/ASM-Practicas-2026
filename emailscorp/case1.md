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