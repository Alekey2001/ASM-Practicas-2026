# Mapeo de superficie web — REP-ASM-2026-S02

[Inicio](../README.md) · [Informe histórico](REP-ASM-2026-S02_AIACO_ASM_Sprint.pdf) · [Fe de erratas](../docs/public/FE_DE_ERRATAS.md).

## Activo y alcance histórico

El activo documentado es `https://aiaco.netlify.app`. No se sustituye por otro dominio ni se comprueba su estado actual. Los informes lo describen como un activo real; las capturas corresponden a actividades históricas de reconocimiento. Nmap y Gobuster generan tráfico y son técnicas activas; no deben describirse como reconocimiento exclusivamente pasivo ni como autorización para repetirlas.

## Evidencia disponible

| Técnica | Resultado observado o reportado | Evidencia y límites |
|---|---|---|
| Fingerprinting | Netlify, Tailwind CSS, Google Font API | [Wappalyzer](../images/web/fingerprinting/wappalyzer-tecnologias.png); identificación de herramientas, no garantía de arquitectura interna |
| Puertos y servicios | 53/TCP, 80/TCP y 443/TCP abiertos en la respuesta observada | [Nmap](../images/web/nmap/puertos-servicios.png); la IP puede corresponder a infraestructura compartida, no atribuir DNS a la aplicación sin evidencia |
| Métodos y cabeceras | GET, HEAD, POST, OPTIONS; HSTS presente | [NSE](../images/web/nmap/metodos-cabeceras.png); que un método no se anuncie no demuestra su bloqueo efectivo |
| Cabeceras ausentes | CSP, X-Frame-Options y X-Content-Type-Options, entre otras señaladas | [Resumen](../images/web/headers/evaluacion-cabeceras.png) y [detalle](../images/web/headers/cabeceras-detalle.png); no hay validación posterior |
| Enumeración de rutas | Respuestas 200 y 403 | [Gobuster](../images/web/gobuster/enumeracion-resultados.png); 403 por sí solo no prueba que exista la ruta ni que su control de acceso sea correcto |

La documentación histórica indica respuestas 200 para `/index.html` y `/servicio`, y 403 para rutas como `/company`, `/community` y `/comments`. No se reportaron fugas en el alcance explorado; no equivale a demostrar cero fugas en todo el sistema ni ausencia de archivos sensibles fuera de ese alcance.

## Conclusión y acciones pendientes

El informe asignó riesgo bajo al mapeo. Esa calificación no certifica el estado actual ni la seguridad global del proveedor o de la aplicación. Se propone revisar CSP, protección frente a framing y MIME sniffing, probar compatibilidad y documentar las respuestas posteriores. No se declara implementado ese hardening.

[Comandos históricos y sus límites](../scripts/README_scripts.md) · [Herramientas](../tools/README_instalacion.md).
