# Identidades y bases de datos — laboratorio sintético

**Documento relacionado:** [REP-ASM-2026-EML01](REP-ASM-2026-EML01_AIACO_Email_Security.pdf). [Inicio](../README.md) · [Fe de erratas](../docs/revision/FE_DE_ERRATAS.md).

## Escenario y alcance

`AIACO-2026-001` es el identificador de un **incidente ficticio**: el enunciado simula que un tercero obtuvo una copia de una tabla de desarrollo. No demuestra una intrusión, exfiltración ni compromiso real. Las identidades, correos y contraseñas vulnerables de `aiaco.local` son datos sintéticos necesarios para reproducir el ejercicio.

Se analiza MySQL 8.0 en Docker local. No se evaluaron correo real, SPF, DKIM, DMARC, MX, servicios OSINT externos ni autenticación de una aplicación productiva.

## Fuentes y hallazgos

El [fixture de inicialización](mysql/init.sql), su [copia histórica](../scripts/database.sql) y el [JSON sintético](../scripts/fault.json) describen los mismos cinco registros. El [CSV de identidades](aiaco_corporate_emails.csv) es otro conjunto de datos sintéticos; no contiene las contraseñas y no se importa automáticamente a MySQL.

| Observación del fixture | Alcance |
|---|---|
| Cinco registros | Muestra educativa; no representa plantilla real |
| Tres contraseñas en texto plano | Exposición intencional en la tabla original |
| Cinco valores MD5, dos registros sin texto plano | MD5 persiste también en la copia saneada; no son únicamente dos hashes |
| Dos contraseñas triviales en el ejercicio | Los valores débiles son deliberados; no deben reutilizarse como credenciales operativas |
| Un par texto plano / MD5 no coincide | Inconsistencia del fixture conservada como evidencia; no debe usarse para probar un sistema de login |

La calificación crítica del almacenamiento de texto plano y la clasificación de MD5 proceden del informe educativo. Un formato de correo predecible o compartir dominio no prueba por sí solo una vulnerabilidad de autenticación. Se corrigió la atribución histórica de una contraseña trivial al usuario equivocado: las consultas del fixture son la fuente de verdad.

## Acción histórica y validación

Se duplicó la tabla en `leaked_credentials_backup` y se estableció `password_plain = NULL` **en esa copia**. La [captura del UPDATE](../images/identity-database/remediation/saneamiento-copia.png) muestra la operación; la [validación de integridad](../images/identity-database/remediation/validacion-integridad-copia.png) compara ambas tablas.

| Objeto | Antes | Después observado | Estado |
|---|---|---|---|
| `leaked_credentials` | Cinco registros; tres textos planos | Tres textos planos permanecen | Vulnerable por diseño del laboratorio |
| `leaked_credentials_backup` | Copia de cinco registros | Cinco registros; cero textos planos; MD5 conservado | Saneamiento de copia documentado |
| Autenticación de aplicación | No aportada | No hay migración ni pruebas de login | Pendiente |

**Esto no es remediación integral del sistema.** Conservar filas no demuestra continuidad de autenticación, restauración segura, eliminación de otras copias ni integridad de un sistema productivo.

## Reproducción sin alterar el original

El nuevo [sanitize_copy.sql](mysql/sanitize_copy.sql) crea `leaked_credentials_sanitized`, una copia diferente de la evidencia histórica. Copia los identificadores, correos y hashes; nunca inserta texto plano. Su clave primaria permite repetir la operación sin duplicar registros. No borra filas adicionales que ya existieran en el destino: las señala con una consulta de validación. Requiere esquema compatible y ejecución exclusiva de laboratorio.

Las consultas antes/después informan conteos y diferencias, sin imprimir contraseñas. Para el fixture se esperan cinco filas, tres textos planos en el original y cero en la copia. Son **expectativas**, no resultados de una ejecución de MySQL realizada durante esta revisión. La sintaxis específica y la repetición sobre MySQL real quedan pendientes si no se dispone de servidor local.

El uso de `VALUES()` en el upsert es compatible con MySQL 8.0, aunque está deprecado en versiones de esa serie; no se afirma compatibilidad con versiones futuras. Los scripts de inicialización contienen `DROP TABLE`: solo deben usarse al inicializar un volumen vacío, nunca como remediación de una base con información que se deba conservar.

## Remediación del sistema pendiente

MD5 no es adecuado para almacenar contraseñas: es demasiado rápido para resistir ataques de adivinación. Se recomienda diseñar una migración de autenticación a **Argon2id** o, cuando corresponda, **bcrypt**, con salt individual y parámetros revisados. Los hashes no se convierten por simple sustitución SQL; hacen falta flujos de restablecimiento o actualización tras verificar la contraseña. Eliminar texto plano de una copia no implementa esa migración.

Quedan pendientes política de contraseñas, MFA según contexto, gestión de credenciales operativas y pruebas de autenticación. [Preparación e instrucciones locales](../tools/README_instalacion.md) · [Consultas y ejecución](../scripts/README_scripts.md).
