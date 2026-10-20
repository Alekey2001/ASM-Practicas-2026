# Caso 1 — Análisis de falso positivo por actividad administrativa

## 1. Descripción

Durante la supervisión de seguridad del laboratorio AWS se detectó una actividad asociada a una cuenta con privilegios administrativos que inicialmente fue considerada potencialmente sospechosa.

Debido al nivel de privilegios de la cuenta involucrada, la actividad requirió un proceso de análisis y seguimiento para determinar si se trataba de una acción administrativa legítima o de una posible actividad no autorizada.

El objetivo del caso fue analizar el evento, revisar el contexto disponible y determinar su clasificación desde el punto de vista de seguridad.

---

## 2. Objetivo

Los objetivos fueron:

* Analizar una actividad asociada a una cuenta administrativa.
* Determinar si existían indicadores de compromiso.
* Revisar el contexto de la actividad.
* Diferenciar una actividad legítima de una actividad potencialmente maliciosa.
* Identificar posibles deficiencias en los procedimientos de comunicación.
* Clasificar finalmente el evento como incidente real o falso positivo.

---

## 3. Situación inicial

El evento fue detectado debido a que una actividad administrativa podía interpretarse inicialmente como potencialmente sospechosa.

La cuenta involucrada contaba con privilegios elevados, por lo que cualquier actividad asociada debía analizarse cuidadosamente.

La investigación no se limitó a observar una única alerta, sino que requirió revisar el contexto y mantener seguimiento para determinar la legitimidad de la operación.

---

## 4. Análisis Blue Team

Durante el análisis se revisó:

* Identidad asociada a la actividad.
* Naturaleza de la operación.
* Contexto administrativo.
* Evidencia disponible.
* Indicadores de compromiso.
* Posibles acciones posteriores.
* Existencia o ausencia de comportamiento malicioso.

No se encontraron evidencias suficientes que indicaran:

* Acceso no autorizado.
* Escalada de privilegios no autorizada.
* Persistencia maliciosa.
* Extracción de credenciales.
* Ejecución de código malicioso.
* Compromiso de la instancia.

---

## 5. Resultado de la investigación

Después del análisis, la actividad fue clasificada como:

**FALSO POSITIVO**

La actividad correspondía a una operación legítima de administración y no se identificaron indicadores suficientes para considerarla un incidente de seguridad real.

---

## 6. Problema procedimental identificado

Aunque la actividad era legítima, se identificó una deficiencia en el procedimiento operativo.

El administrador involucrado no realizó previamente el protocolo de notificación correspondiente al equipo de seguridad.

Como consecuencia, una actividad legítima generó una situación que inicialmente tuvo que ser tratada como potencialmente sospechosa.

Esto obligó al equipo de seguridad a realizar un análisis adicional para determinar que no existía un compromiso.

---

## 7. Impacto

No se identificó compromiso de la infraestructura.

El impacto principal fue operativo:

* Generación de una alerta potencial.
* Consumo de tiempo de análisis.
* Necesidad de seguimiento continuo.
* Investigación adicional por parte del equipo de seguridad.
* Falta de correlación inicial entre la actividad administrativa y el evento detectado.

---

## 8. Causa raíz

La causa raíz identificada no fue una vulnerabilidad técnica de AWS.

El problema principal estuvo relacionado con:

**Falta de comunicación y cumplimiento del protocolo de notificación para actividades administrativas.**

---

## 9. Lecciones aprendidas

Este caso demuestra que una actividad legítima puede convertirse en una alerta de seguridad cuando no existe una correcta comunicación entre los administradores y el equipo de seguridad.

Las actividades administrativas sensibles deben:

1. Ser previamente autorizadas.
2. Ser registradas.
3. Ser notificadas cuando corresponda.
4. Tener una ventana de mantenimiento o actividad definida.
5. Contar con una persona responsable.
6. Poder correlacionarse posteriormente con los logs de seguridad.

---

## 10. Recomendaciones

Se recomienda:

* Establecer un procedimiento formal para actividades administrativas.
* Notificar al equipo de seguridad antes de operaciones sensibles.
* Mantener registros de cambios administrativos.
* Utilizar tickets o registros de cambio.
* Definir ventanas de mantenimiento.
* Correlacionar actividades administrativas con logs.
* Documentar excepciones.
* Reducir falsos positivos mediante contexto operacional.

---

## 11. Clasificación final

| Elemento               | Resultado                   |
| ---------------------- | --------------------------- |
| Tipo                   | Falso positivo              |
| Actividad              | Administrativa legítima     |
| Compromiso             | No identificado             |
| Escalada no autorizada | No identificada             |
| Robo de credenciales   | No identificado             |
| Persistencia           | No identificada             |
| Problema principal     | Falta de notificación       |
| Impacto                | Operativo                   |
| Estado                 | Cerrado como falso positivo |

---

## 12. Conclusión

El análisis permitió determinar que la actividad inicialmente considerada sospechosa correspondía a una operación administrativa legítima.

No se encontraron evidencias suficientes de compromiso de la infraestructura.

Sin embargo, el caso permitió identificar una debilidad importante en los procedimientos operativos: la falta de notificación previa al equipo de seguridad.

Por lo tanto, aunque el evento fue cerrado como falso positivo, se recomienda mejorar los procesos de comunicación y gestión de cambios para reducir futuras alertas innecesarias y facilitar la correlación entre las actividades administrativas y los eventos de seguridad.
