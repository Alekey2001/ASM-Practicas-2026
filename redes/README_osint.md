# OSINT — indexación, robots.txt y Google Dorking

**Código:** REP-ASM-2026-OSINT01. [Inicio](../README.md) · [Informe histórico](REP-ASM-2026-OSINT01_Fundamentos_OSINT_Web.pdf) · [Fe de erratas](../docs/revision/FE_DE_ERRATAS.md).

Este módulo es un estudio teórico-práctico basado en TryHackMe y ejercicios de búsqueda. La [captura de finalización](../images/osint/tryhackme-dorking.png) acredita una actividad educativa; no es certificación profesional, auditoría formal ni evidencia de exposición de una empresa.

## Descubrimiento e indexación

```text
Internet → crawler (descubre) → índice (organiza) → buscador (consulta)
```

El crawler visita páginas y sigue enlaces; el índice almacena referencias y el buscador responde a consultas sobre ese índice. SEO trata de facilitar descubrimiento e interpretación del contenido. Consultar un índice de terceros es reconocimiento indirecto; visitar resultados, robots.txt o sitemap.xml genera solicitudes al servidor. No se garantiza ausencia de logs o alertas.

## Archivos de control: ejemplo sintético

```text
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/
Sitemap: https://example.com/sitemap.xml
```

`robots.txt` indica preferencias de rastreo; `Disallow` no autentica ni impide acceso humano. Las rutas pueden revelar estructura. Un sitemap suele ser XML con URLs del sitio; no es un listado exhaustivo de rutas privadas ni un control de acceso.

El material anterior utilizaba `aiaco.local` como ejemplo. Ese dominio pertenece al escenario sintético y no se asume indexado públicamente. Los ejemplos siguientes usan `example.com`, sin sustituir el activo web histórico `aiaco.netlify.app`.

## Operadores y ejemplos didácticos

| Operador | Objetivo | Ejemplo no ejecutado en esta revisión |
|---|---|---|
| `site:` | Limitar dominio | `site:example.com` |
| Comillas | Buscar frase | `"AIACO Corp"` |
| `filetype:` | Filtrar formato | `site:example.com filetype:pdf` |
| `intitle:` | Filtrar título | `site:example.com intitle:login` |

```text
site:example.com (intitle:login OR intitle:admin OR intitle:dashboard)
site:example.com (filetype:pdf OR filetype:docx OR filetype:xlsx)
site:github.com "example.com" (filetype:env OR filetype:json)
site:linkedin.com/in/ "AIACO Corp" ("DevOps" OR "Desarrollador")
```

Son diseños de consulta, no resultados de exposición ni campañas realizadas. El operador `cache:` se conserva únicamente como referencia histórica del PDF; no se utiliza ni se afirma su disponibilidad actual.

## Conceptos del ejercicio

| Concepto | Respuesta registrada |
|---|---|
| Colección de recursos y ubicaciones | Index |
| Descubrimiento de contenido | Crawling |
| Extensión de configuración del ejercicio | .conf |
| Formato típico del sitemap | XML |
| Metáfora del sitemap | Map |
| Camino hacia una página | Route |

El valor para ASM es organizar fuentes públicas y separar información indexada de acceso efectivo. No hay evidencia de una filtración real ni de compromiso de identidades en este módulo.
