# Mobile AppSec — análisis estático y límites de evidencia

**Código:** REP-ASM-2026-MOB01. [Informe histórico](REP-ASM-2026-MOB01_AppSec_SAST_Movil.pdf) · [Inicio](../README.md) · [Fe de erratas](../docs/public/FE_DE_ERRATAS.md).

**Estado: análisis inicial documentado; remediación y validación posterior NO VERIFICADAS.**

## Alcance observado

Las capturas muestran preparación de EAS, un escaneo de APK con MobSF y resultados de análisis estático. El informe describe la aplicación como un activo de AIACO. El repositorio no incluye el APK analizado, `fixes.apk`, el código fuente de la aplicación, `app.json`, el backend ni cambios de autorización de API. Los nombres de esos archivos son referencias del informe, no enlaces a artefactos disponibles.

La [captura de resultados](../images/mobile-appsec/mobsf/resultado-score52.png) muestra **52/100**. El [registro de análisis](../images/mobile-appsec/mobsf/registro-analisis.png) confirma actividades de análisis, sin demostrar su corrección posterior. El [inicio de un build EAS](../images/mobile-appsec/apk/configuracion-build-eas.png) no acredita un APK corregido.

## Comparación antes / después

| Elemento | Antes: evidencia disponible | Después: evidencia disponible | Conclusión |
|---|---|---|---|
| Security Score | Captura MobSF: 52/100 | No hay escaneo posterior vinculado a un binario | Pendiente; no usar 42/100 → 88/100 de la presentación |
| Manifest Analysis | Informe histórico reporta una advertencia | Sin reporte de reanálisis | Reportado, no verificado independientemente |
| Code Analysis | Informe reporta cero vulnerabilidades y tres advertencias | Sin reporte de reanálisis | No equivale a ausencia general de vulnerabilidades |
| `app.json`, XML y JSON | Afirmaciones narrativas del informe | No hay archivos ni diff | Exposición y hardening no verificables localmente |
| `fixes.apk` | Nombrado en el informe | Binario y hash no aportados | Generación y distribución no verificadas |
| Autorización de API | No hay solicitudes/respuestas ni código del servidor | No hay prueba positiva/negativa ni cambios de backend | Fallo y remediación no demostrados |
| Aviso DEP0040 | Visible en preparación del entorno EAS | No aplica como prueba de autorización | Advertencia del entorno, no hallazgo de seguridad del APK |

## Interpretación técnica

SAST inspecciona un binario y puede señalar configuraciones o patrones que requieren revisión. No valida por sí solo la autorización que aplica un servidor. Ocultar metadatos u ofuscar configuración cliente no sustituye controles de autorización en el backend. Tampoco debe inferirse que toda API necesite token: la protección depende del recurso y del modelo de acceso.

Para cerrar el caso se requieren identificador y hash de cada APK, reporte SAST antes/después sobre esos binarios, cambios de fuente revisables y pruebas de acceso del backend con usuario autorizado, no autorizado y solicitudes sin credenciales cuando el recurso sea privado. No se han fabricado binarios, capturas ni resultados para suplir esa ausencia.

## Evidencia y protección de credenciales

La [captura pública de arranque](../images/mobile-appsec/mobsf/arranque-anonimizado.png) contiene tres bandas opacas que sustituyen los píxeles de la clave REST API y las credenciales predeterminadas. Se conserva el original cifrado fuera del repositorio; su integridad fue comprobada antes del reemplazo. La anonimización no demuestra revocación de la clave ni corrige su presencia en el historial Git.

Las [secciones de red/certificado](../images/mobile-appsec/mobsf/analisis-red-certificado.png) y la [interfaz de carga](../images/mobile-appsec/mobsf/interfaz-carga.png) completan el material disponible, sin constituir prueba de un parche. [Índice de imágenes](../images/README.md).

OWASP MASVS es una referencia para organizar el trabajo pendiente, no una certificación de cumplimiento de la aplicación.
