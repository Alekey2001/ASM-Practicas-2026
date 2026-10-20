# 🛡️ AICO — Programa de Attack Surface Management (ASM)

### De la superficie de ataque al parche validado: **5 vectores auditados, vulnerabilidades remediadas y evidencia documentada.**

> **Red Team → Evidencia → Blue Team → Remediación → Validación.**
> Un ciclo completo de seguridad aplicado a **Web, Identidades/DB, Cloud (AWS), OSINT y Mobile**, sin interrumpir la continuidad del negocio.

| | |
|---|---|
| 👤 **Autor** | **Jesús Alejandro Rodríguez Medina** |
| 🎓 **Formación** | Técnico Superior Universitario (TSU) en **Seguridad Informática** — Universidad ONMEX (RVOE 2894) |
| 🎯 **Perfil objetivo** | **Consultor Jr. de Ciberseguridad** · **Analista DevSecOps** · **SOC Nivel 1** |
| 🏢 **Proyecto** | Prácticas Profesionales — **Attack Surface Management (ASM)** para **AICO** |
| 📬 **Contacto** | `[tu-correo]` · `[tu-LinkedIn]` |

---

## 📊 Resultados en un vistazo

| Indicador | Resultado |
|---|---|
| 🧭 Vectores auditados | **5** (Web · Identidades/DB · Cloud AWS · OSINT · Mobile) |
| 📄 Reportes técnicos formales | **5**, con código de documento y matriz de riesgos |
| 🔴 Hallazgos críticos remediados | Contraseñas en **texto plano**, **SSH expuesto a 0.0.0.0/0**, **IMDS sin token** |
| 🟢 Parches validados con evidencia | `IMDSv2 → HTTP 401` · `SSH → restricción /32` · `0 contraseñas en texto plano` · `fixes.apk` |
| 🧠 Falsos positivos investigados | **1** (actividad administrativa legítima, con lección de proceso) |
| ⚖️ Marcos normativos referenciados | **ISO/IEC 27001 · CIS Benchmarks · OWASP · NIST SP 800-115** |

---

## 1️⃣ Resumen del Proyecto y Valor para las Empresas (Business Impact)

La ciberseguridad no es una lista de vulnerabilidades: es un **habilitador del negocio**. Este proyecto demuestra que mi enfoque va más allá de encontrar fallas:

- 🔍 **Identifico** la superficie de ataque con técnicas **pasivas y no destructivas** (reconocimiento, fingerprinting, SAST, OSINT).
- 🧪 **Valido el riesgo** con pruebas controladas y **evidencia técnica verificable**, sin explotación destructiva ni extracción de credenciales.
- 🔧 **Aplico el parche**, no solo lo recomiendo: cierro puertos, endurezco configuraciones, sanitizo datos y genero binarios corregidos.
- ✅ **Valido la corrección** con pruebas posteriores (códigos HTTP, consultas SQL, re-verificación de advertencias).
- 📑 **Documento todo** en reportes formales con **matrices de riesgo** (OWASP Risk Rating), estados y riesgo residual honesto — sin presentar como terminado lo que aún está pendiente.
- ⚖️ **Alineo cada hallazgo a estándares**: **ISO/IEC 27001**, **CIS Benchmarks**, **OWASP (WSTG / MASVS)** y **NIST SP 800-115**.
- 🏭 **Protejo la continuidad operativa**: todas las pruebas se ejecutaron en entornos controlados, con alcance acotado y sin afectar la disponibilidad.

> 💡 **Lo que aporta a una organización:** menos superficie expuesta, riesgos priorizados por impacto, remediaciones comprobadas y trazabilidad lista para auditoría.

---

## 2️⃣ Resumen Técnico de los 5 Mapeos Ejecutados

### 🌐 Mapeo 1 — Web: `aiaco.netlify.app` · `REP-ASM-2026-S02`
- **Metodología:** **Caja Negra (Black-Box)** bajo **NIST SP 800-115** y **OWASP WSTG**.
- **Herramientas:** **Nmap 7.95**, **Gobuster**, **Wappalyzer**, **SecurityHeaders.com**.
- **Qué hice:** fingerprinting pasivo, escaneo de puertos/servicios, auditoría de métodos y cabeceras HTTP, y **fuzzing de rutas** para descartar fugas de archivos sensibles (`.env`, `.git`, backups, scripts SQL, paneles admin).
- **Arquitectura evaluada:** **Serverless / hosting estático (Netlify)** — superficie reducida, **HSTS activo**, métodos peligrosos (`PUT`, `DELETE`, `TRACE`) deshabilitados.
- **Resultado:** riesgo global **BAJO**, **0 fugas de información**.
- **Hardening propuesto:** **Content-Security-Policy (CSP)**, **X-Frame-Options** y **X-Content-Type-Options** vía cabeceras HTTP.

### 🔑 Mapeo 2 — Identidades y Base de Datos · `REP-ASM-2026-EML01`
- **Entorno:** **Docker + MySQL 8.0** local sobre **Windows + WSL2**.
- **Hallazgos:** **3 credenciales en texto plano** (incluyendo contraseñas extremadamente débiles) y **2 usuarios con hash MD5** (algoritmo obsoleto). Riesgo inicial: **CRÍTICO**.
- **Remediación defensiva:** **Data Sanitization** mediante **scripts SQL** sobre una **tabla de respaldo**, preservando la evidencia original.
- **Validación:** `0` contraseñas en texto plano · `5` usuarios conservados · integridad intacta.
- **Siguiente nivel recomendado:** migrar hashes a **Argon2 / bcrypt / scrypt** y reforzar políticas de contraseñas.

### ☁️ Mapeo 3 — Cloud AWS EC2 · `REP-ASM-2026-AWS01`
- **Entorno:** **AWS EC2** (Ubuntu 22.04) en **VPC**, con **Security Groups** e **IMDS**.
- **Hallazgos y remediaciones:**
  - 🔴 **SSH expuesto** (`TCP/22` abierto a `0.0.0.0/0`) → restricción del Security Group a **IP administrativa `/32`**. ✅
  - 🟠 **IMDSv2 en modo Optional** → **IMDSv2 Required**; una consulta sin token ahora recibe **HTTP 401**. ✅
- **Controles positivos verificados:** root login deshabilitado, autenticación por contraseña deshabilitada, solo llave pública, **Fail2Ban** activo, sin IAM Role asociado (*least privilege*).
- **Resultado del Red Team:** sin acceso no autorizado, sin extracción de credenciales.
- **Gestión operativa:** investigación documentada de un **falso positivo** (actividad administrativa legítima) y detección de una **brecha de procedimiento** — el administrador no notificó previamente al equipo de seguridad.

### 🕵️ Mapeo 4 — OSINT y Dorking · `REP-ASM-2026-OSINT01`
- **Enfoque:** **reconocimiento 100% pasivo**, sin generar tráfico ni ruido en los firewalls del objetivo.
- **Qué analicé:** funcionamiento de **crawlers e indexación**, **SEO**, **`robots.txt`** y **`sitemap.xml`**, y **Google Dorking** (`site:` · `filetype:` · `intitle:` · `"frase exacta"`).
- **Conclusión clave:** **`robots.txt` no es un control de seguridad.** `Disallow: /admin/` no protege nada — incluso puede **revelar** rutas sensibles. La exclusión no equivale a autenticación ni autorización.

### 📱 Mapeo 5 — Mobile AppSec (SAST) · `REP-ASM-2026-MOB01`
- **Herramienta:** **MobSF** en **Docker**, bajo **OWASP MASVS**.
- **Objeto:** APK de prueba de respaldo.
- **Hallazgos:** **Security Score inicial 52/100**, **1 advertencia en Manifest Analysis**, **0 vulnerabilidades y 3 advertencias en Code Analysis**; **exposición de datos en `app.json`/XML/JSON** y **fallos de autorización de API**.
- **Remediación:** hardening de **`app.json`**, corrección de la **autorización de la API** (sin consultas anónimas o sin token) y generación del binario parcheado **`fixes.apk`**.

---

## 🗂️ Índice de Evidencia

| # | Vector | Código de documento | Riesgo inicial | Estado |
|---|---|---|---|---|
| 1 | 🌐 Web | `REP-ASM-2026-S02` | 🟢 Bajo | ✅ Completado |
| 2 | 🔑 Identidades / DB | `REP-ASM-2026-EML01` | 🔴 Crítico | ✅ Remediado y validado |
| 3 | ☁️ Cloud AWS | `REP-ASM-2026-AWS01` | 🟠 Medio–Alto | ✅ Remediado y validado |
| 4 | 🕵️ OSINT | `REP-ASM-2026-OSINT01` | ℹ️ Estudio / pasivo | ✅ Completado |
| 5 | 📱 Mobile | `REP-ASM-2026-MOB01` | 🟡 Score 52/100 | ✅ Remediado (`fixes.apk`) |

---

## 3️⃣ Stack Tecnológico y Metodologías

**☁️ Cloud & Infraestructura**
`AWS EC2` · `VPC` · `Security Groups` · `IMDSv2` · `Fail2Ban` · `OpenSSH`

**🐳 Contenedores & Datos**
`Docker` · `Docker Compose` · `MySQL 8.0` · `SQL (Data Sanitization)`

**🔎 Reconocimiento & Auditoría**
`Nmap` · `Gobuster` · `Wappalyzer` · `SecurityHeaders.com` · `Google Dorking`

**📱 AppSec**
`MobSF` · `SAST` · `Análisis de AndroidManifest` · `Revisión de app.json / XML / JSON`

**🐧 Entornos**
`Linux (Kali / Ubuntu)` · `WSL2` · `Windows` · `PowerShell` · `VS Code`

**📚 Metodologías & Estándares**
`OWASP WSTG` · `OWASP MASVS` · `NIST SP 800-115` · `CIS Benchmarks` · `ISO/IEC 27001` · `OWASP Risk Rating` · `Agile / SCRUM`

---

## 4️⃣ Aprendizajes y Mi Propuesta de Valor (Por qué contratarme)

Este proyecto me preparó para el trabajo real, no solo para el laboratorio:

- 🎯 **Gestiono falsos positivos con criterio:** investigué una alerta sospechosa hasta confirmar que era legítima, **sin escalar innecesariamente**, y convertí el caso en una **lección de proceso** (notificación previa de actividad administrativa).
- 📝 **Documento incidentes y hallazgos como se espera en una organización:** reportes formales, códigos de documento, matrices de riesgo, estados reales (completado / pendiente) y **riesgo residual honesto**.
- 🌍 **Audito de punta a punta:** desde la **nube (AWS)** y las **bases de datos**, pasando por la **web** y el **reconocimiento OSINT**, hasta el **código móvil (APK)**.
- 🔄 **Cierro el ciclo completo:** detección → evidencia → **remediación** → **validación**. No me quedo en el hallazgo.
- ⚖️ **Pienso en cumplimiento:** cada control lo conecto con **ISO 27001, CIS, OWASP y NIST**.
- ⚡ **Ejecución rápida:** mi formación como **TSU** me da un perfil práctico y orientado a resultados, ideal para **integrarme de inmediato** a:

| 🧩 Equipo | 💼 Qué puedo aportar desde el día 1 |
|---|---|
| 🛡️ **SOC Nivel 1** | Triage de alertas, descarte de falsos positivos, lectura de logs y documentación de incidentes |
| 🧭 **Consultoría de Ciberseguridad** | Evaluaciones de superficie de ataque, reportes ejecutivos/técnicos y hardening priorizado |
| ⚙️ **DevSecOps** | Revisión de configuraciones cloud, contenedores y SAST móvil integrables al ciclo de desarrollo |

---

> 🤝 **¿Buscas un perfil Jr. que no solo encuentre vulnerabilidades, sino que las corrija, las valide y las documente?**
> Hablemos: `acuartnest@gmail.com` · `https://www.linkedin.com/in/jesusalexandrorodriguez/?isSelfProfile=true`,https://jesusr.netlify.app/

*Alcance: el sitio web y la aplicación móvil son activos reales de AICO; los entornos de correo corporativo, redes y cloud (AWS) fueron simulados en laboratorio. Las pruebas se limitaron a recursos autorizados. No se realizó fuerza bruta, explotación destructiva, extracción de credenciales ni ataques a infraestructura ajena.*