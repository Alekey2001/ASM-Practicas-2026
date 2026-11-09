# AIACO — Prácticas de Attack Surface Management

> **Estado de publicación:** material histórico y educativo. Consulta la
> [fe de erratas pública](docs/public/FE_DE_ERRATAS.md) antes de reutilizar
> cualquier resultado.

Portafolio de prácticas de ciberseguridad en cinco áreas: Web, Identidades y bases de datos, Cloud AWS, OSINT y Mobile AppSec. La documentación distingue resultados observados, acciones reportadas y validaciones pendientes.

| Perfil | Información |
|---|---|
| Autor | Jesús Alejandro Rodríguez Medina |
| Formación declarada | TSU en Seguridad Informática — Universidad ONMEX (RVOE 2894) |
| Orientación profesional | GRC Junior · AppSec Junior · Analista de Ciberseguridad Junior |
| Proyecto | ASM-Practicas-2026 — prácticas profesionales |
| Contacto | [Correo](mailto:acuartnest@gmail.com) · [LinkedIn](https://www.linkedin.com/in/jesusalexandrorodriguez/) |

## Alcance y lectura de la evidencia

Web y aplicación móvil se describen en los informes como activos reales de AIACO. Las identidades y credenciales de `aiaco.local` son datos sintéticos. AWS es un laboratorio educativo sobre recursos cloud reales; no representa un incidente de producción. OSINT reúne ejercicios y fundamentos, sin evidencia de una filtración real. Las actividades históricas se describen como autorizadas por el autor; esta revisión solo trabaja con archivos locales y no comprueba el estado actual de ningún activo.

Se adopta **AIACO** por el nombre visible del sitio, los casos y los informes técnicos. La variante **AICO** aparece en el informe final histórico; no hay evidencia suficiente para afirmar que sea otra entidad o un cambio oficial de marca. Se conservan nombres y códigos de los documentos originales.

**Los PDF y la presentación son documentos históricos, no una certificación de cierre.** Consultar la [fe de erratas pública](docs/public/FE_DE_ERRATAS.md) junto con ellos. La presentación contiene información personal y afirmaciones pendientes de corrección; no está lista para publicación. La captura pública de arranque MobSF fue anonimizada, pero la clave permanece en el historial Git y su rotación está pendiente.

## Estado de los cinco casos

| Caso e informe histórico | Evidencia disponible | Estado sustentado |
|---|---|---|
| [Web](sitiosweb/README_mapeo_web.md) · [REP-ASM-2026-S02](sitiosweb/REP-ASM-2026-S02_AIACO_ASM_Sprint.pdf) | Capturas Nmap, Gobuster, Wappalyzer y cabeceras | Mapeo documentado; hardening de cabeceras propuesto, sin validación posterior |
| [Identidades / DB](emailscorp/case1.md) · [REP-ASM-2026-EML01](emailscorp/REP-ASM-2026-EML01_AIACO_Email_Security.pdf) | Cinco registros sintéticos; tres textos planos; cinco valores MD5, dos sin texto plano | Copia saneada validada en capturas; original vulnerable y migración de contraseñas pendientes |
| [Cloud AWS](cloud/case1.md) · [REP-ASM-2026-AWS01](cloud/REP-ASM-2026-AWS01_DevSecOps_AWS_Security_Lab.pdf) | SSH accesible, rechazo de usuario ficticio, logs y respuesta IMDS HTTP 401 | SSH **PENDIENTE DE VALIDACIÓN**; rechazo de consultas sin token IMDS documentado |
| [OSINT](redes/README_osint.md) · [REP-ASM-2026-OSINT01](redes/REP-ASM-2026-OSINT01_Fundamentos_OSINT_Web.pdf) | Fundamentos de indexación y finalización de módulo educativo | Estudio documentado; no acredita compromiso o exposición de una organización |
| [Mobile AppSec](apps/case1.md) · [REP-ASM-2026-MOB01](apps/REP-ASM-2026-MOB01_AppSec_SAST_Movil.pdf) | Captura MobSF con score 52/100 y registros de análisis | Análisis inicial documentado; parche, APK corregido y autorización de backend **NO VERIFICADOS** |

No se usa el número de casos como número de vulnerabilidades remediadas. La evidencia de una respuesta HTTP, una copia SQL saneada o un escaneo estático tiene alcance limitado al objeto y momento observados.

## Competencias demostradas y pendientes

- **GRC Junior:** inventario de activos y evidencias, priorización de riesgos del ejercicio, trazabilidad, documentación de controles y separación de recomendaciones frente a validaciones.
- **AppSec Junior:** lectura de resultados SAST, revisión de configuración web y móvil, reconocimiento de límites del análisis estático y planificación de pruebas posteriores.
- **Operación y DevSecOps:** laboratorio MySQL local, revisión de configuraciones Compose, análisis documentado de logs y hardening de IMDS.

ISO/IEC 27001, NIST SP 800-115, CIS y OWASP WSTG/MASVS/ASVS se usan como referencias educativas. El repositorio no acredita certificación, conformidad integral, auditoría formal ni cobertura completa de esos marcos. Las etiquetas históricas de riesgo pertenecen a la evaluación del ejercicio, no a una reevaluación de sistemas actuales.

## Navegación y reproducción local

- [Índice y clasificación completa de imágenes](images/README.md).
- [Preparación del laboratorio](tools/README_instalacion.md).
- [Scripts, generación sintética, SQL y comandos históricos](scripts/README_scripts.md).
- [Informe final histórico REP-ASM-2026-FIN01](REP-ASM-2026-FIN01_Informe_Final_ASM_AIACO.pdf), sujeto a la [fe de erratas pública](docs/public/FE_DE_ERRATAS.md).

Los comandos históricos de reconocimiento no son autorización para repetir pruebas contra recursos públicos. Las validaciones de esta revisión no iniciaron infraestructura ni contactaron los activos evaluados.
