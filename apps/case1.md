# 📱 Mapeo 5: Seguridad en Aplicaciones Móviles (AppSec & SAST)
**ID del Reporte:** `REP-ASM-2026-MOB01`  
**Vector de Ataque:** Aplicación Móvil (Android APK)  
**Metodología:** OWASP MASVS (Mobile Application Security Verification Standard)  

---

## 🎯 Objetivo del Mapeo
Ejecutar un Análisis Estático de Seguridad (SAST) sobre el binario de la aplicación móvil de AIACO Corp. El propósito es identificar vulnerabilidades en el código fuente, exposición de configuraciones, permisos excesivos en el manifiesto y fugas en la autorización de APIs, para posteriormente aplicar el *hardening* necesario.

## 🛠️ Entorno y Herramientas
* **Entorno de Análisis:** Contenedores Docker.
* **Herramienta Principal:** Mobile Security Framework (MobSF).
* **Archivos Analizados:** Binario APK de prueba, `app.json`, y archivos de configuración `XML`.

---

## 🔴 Fase 1: Diagnóstico y Escaneo (Red Team)
Se generó un APK de prueba de respaldo y se sometió a ingeniería inversa y escaneo automatizado mediante MobSF.

**Resultados Iniciales (Security Score): 52 / 100**
* **Advertencia de Plataforma:** Identificación del log `DEP 0040` durante la carga y deconstrucción del entorno.
* **Manifest Analysis:** **1 Hallazgo (Advertencia)**. Identificación de permisos y configuraciones potencialmente inseguras en la declaración del `AndroidManifest.xml`.
* **Code Analysis:** **0 Vulnerabilidades Críticas, 3 Advertencias**. Se detectaron prácticas de código que requieren revisión, incluyendo exposición de esquemas de autorización de API y metadatos en archivos JSON.

---

## 🔵 Fase 2: Remediación y Hardening (Blue Team)
Con base en los hallazgos del reporte de MobSF, se procedió a parchar la aplicación generando un nuevo binario seguro (`fixes.apk`).

**Acciones Correctivas Ejecutadas:**
1. **Revisión de Autorización API:** Se ajustaron los parámetros de validación para el consumo de la API, evitando consultas anónimas o sin token.
2. **Hardening de `app.json`:** Se modificaron las variables de entorno y metadatos expuestos dentro de la configuración del framework (JSON y XML) para ofuscar información sensible.
3. **Validación Final:** Verificación de las advertencias emergentes, confirmando la mitigación de los riesgos señalados en el Manifest y el Code Analysis.

---
*Este mapeo concluye el ciclo del programa de Attack Surface Management (ASM) para AIACO Corp, cubriendo exitosamente la capa de infraestructura móvil.*