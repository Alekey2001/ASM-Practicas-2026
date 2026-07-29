# 🌐 [ASM-02] Mapeo de Superficie de Ataque Web

**Proyecto:** AIACO Corp – Attack Surface Management (ASM)  
**Fase:** Semana 2 - Reconocimiento y Mapeo Web  
**Activo Auditado:** `https://aiaco.netlify.app` (*Infraestructura Simulada real*)

## 🎯 Objetivo
Identificar todos los componentes públicos expuestos del sitio web de AIACO para mapear su superficie de ataque antes de iniciar cualquier evaluación de seguridad activa. El enfoque es estrictamente de reconocimiento (OSINT/Fingerprinting), enumerando puertos, servicios, tecnologías y directorios públicos sin realizar explotación.

---

## 📊 Resumen 
El activo web auditado presenta una **superficie de ataque reducida y bien controlada**. Se encuentra alojado en una infraestructura serverless (Netlify), exponiendo únicamente los servicios HTTP/HTTPS esperados. No se detectaron fugas de información, archivos de configuración sensibles ni directorios administrativos expuestos. 

**Nivel de Exposición Inicial:** Riesgo Bajo.

---

## 🔍 Fases del Escaneo y Hallazgos

### 1. Fingerprinting y Tecnologías
Se realizó un análisis pasivo del stack tecnológico utilizando **Wappalyzer** para identificar las herramientas subyacentes.

*   **Hosting / Infraestructura:** Netlify
*   **Frontend Framework:** Tailwind CSS
*   **Tipografía / Assets:** Google Font API
*   *Nota:* No se detectaron lenguajes de backend tradicionales (PHP, ASP.NET) ni CMS (WordPress), lo cual es consistente con una Single Page Application (SPA) o un sitio estático.

### 2. Análisis de Puertos y Servicios (Nmap)
Se ejecutó un escaneo de puertos y detección de versiones para mapear los servicios expuestos.

| Puerto | Protocolo | Estado | Servicio | Notas |
| :--- | :--- | :--- | :--- | :--- |
| **53** | TCP | Abierto | DNS | Resolución de nombres. |
| **80** | TCP | Abierto | HTTP | Redirección estándar. |
| **443** | TCP | Abierto | HTTPS | Tráfico seguro. Servidor: Netlify. |

*Servicios como SSH (22), FTP (21), RDP (3389) o MySQL (3306) se encuentran correctamente filtrados o cerrados.*

### 3. Auditoría de Cabeceras HTTP
Se auditaron las cabeceras de respuesta del servidor utilizando Nmap (scripts NSE) y `SecurityHeaders.com`.

*   **Métodos Permitidos:** `GET, HEAD, POST, OPTIONS` (Buena práctica: `PUT` y `DELETE` deshabilitados).
*   **Cabeceras de Seguridad Presentes:** `Strict-Transport-Security` (HSTS habilitado, forzando HTTPS).
*   **Cabeceras Ausentes (Oportunidad de Mejora):** 
    *   `Content-Security-Policy` (CSP)
    *   `X-Frame-Options`
    *   `X-Content-Type-Options`

### 4. Descubrimiento de Contenido (Fuzzing de Rutas)
Se utilizó **Gobuster** con un diccionario estándar de Kali Linux (`common.txt`) para identificar rutas ocultas.

*   **Rutas Accesibles (HTTP 200):** `/index.html`, `/servicio`.
*   **Rutas Restringidas (HTTP 403):** `/company`, `/community`, `/comments`. (El servidor responde a la ruta, pero deniega el acceso).
*   **Fugas (Inexistentes):** No se detectaron archivos sensibles (`.env`, `.git`, `backup.zip`, `config.php`).

---

## 🛡️ Conclusión y Recomendaciones (Blue Team)
La infraestructura principal de la aplicación web está correctamente asegurada por el proveedor de hosting. La principal recomendación técnica es **reforzar las cabeceras de seguridad HTTP** (Hardening) implementando CSP y protecciones contra Clickjacking (X-Frame-Options) para incrementar la protección del lado del cliente (navegador).