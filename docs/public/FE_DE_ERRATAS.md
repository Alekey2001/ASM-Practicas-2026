# Fe de erratas pública

Estado: revisión de preparación para publicación, 2026-11-09.

Este documento sustituye referencias a materiales de revisión interna. No
incluye informes privados, inventarios, resultados de saneamiento ni claves.

## Alcance y correcciones de lectura

- Los PDF y `Presentación.pptx` son documentos históricos y no constituyen
  una certificación de cierre, una autorización del activo ni una prueba de
  que todos los parches descritos sigan desplegados.
- Las afirmaciones de remediación deben comprobarse contra la evidencia
  pública que acompaña a cada caso. Si el informe menciona un APK, una API,
  una cuenta, una captura o una validación que no está en este repositorio,
  se considera no verificable aquí.
- La presentación requiere una edición pública anonimizada antes de
  distribuirse: retirar nombres, correos, identificadores de cuenta, rutas,
  endpoints, capturas con contexto identificable y cualquier afirmación no
  respaldada por evidencia pública.
- Las capturas de MobSF publicadas deben ser copias sanitizadas. La
  sanitización visual no demuestra la revocación de una clave que haya estado
  expuesta; esa clave debe revocarse y debe evaluarse el saneamiento del
  historial Git.

## Revisión de presentación, PDF e historial

La inspección local de `Presentación.pptx` encontró texto asociado con
credenciales, tokens, claves y direcciones de contacto. No se reproducen esos
valores. Se recomienda generar una copia pública desde el material fuente,
anonimizarla y someterla a una segunda revisión antes de distribuirla.

Los seis PDF históricos son legibles localmente, pero contienen referencias
operativas y de identidad que deben revisarse por documento. No se modificaron
ni se reescribieron silenciosamente. Para cualquier afirmación contradictoria
o no demostrable, debe publicarse un anexo fechado o una versión corregida
separada que conserve la trazabilidad.

La captura MobSF antigua con clave aparece accesible en commits anteriores.
La clave no se muestra ni se utiliza: requiere revocación inmediata y una
evaluación de saneamiento del historial. `export-ignore` en `.gitattributes`
solo afecta ciertos archivos de exportación; no impide que GitHub muestre o
descargue un archivo que permanezca en un commit.

## Documentos históricos

No se modifican silenciosamente los informes PDF históricos. La revisión de
privacidad y consistencia debe publicarse como un anexo o como una versión
corregida separada, conservando la procedencia y marcando claramente los
cambios.

En esta rama no se publican `RESULTADOS.md`, `PRIVACIDAD.md`, inventarios
previos/posteriores, CSV de clasificación ni instrumentos privados. Las
referencias a esos materiales deben permanecer fuera de la documentación
pública.

## Limitaciones de esta revisión

La base local de `main` no contiene el validador ni los artefactos de revisión
interna mencionados en cambios previos. Por ello, esta rama valida únicamente
archivos públicos presentes en el clon y no afirma haber reproducido controles
históricos que requieren insumos excluidos.

