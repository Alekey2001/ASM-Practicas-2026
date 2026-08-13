# ⚙️ Guía de Entorno e Instalación de Herramientas

Este documento detalla el entorno de trabajo utilizado para la práctica de Attack Surface Management (ASM) y el paso a paso de verificación e instalación de las herramientas de auditoría.

## 💻 Entorno Utilizado
*   **Máquina Principal (Host):** Windows
*   **Máquina Virtual (Auditoría):** Kali Linux
*   **Objetivo Auditado:** `https://aiaco.netlify.app`

---

## 🛠️ Herramientas y Proceso de Instalación

Las pruebas requirieron cuatro herramientas principales. A continuación, se detalla el proceso de preparación en la terminal de Kali Linux:

### 1. Nmap (Mapeo de Redes y Puertos)
Nmap se utiliza para descubrir puertos abiertos, servicios, versiones y encabezados HTTP. En Kali Linux viene preinstalado.
*   **Comando de verificación:**
    ```bash
    nmap --version
    ```
*   **Resultado esperado:**
    ```text
    Nmap version 7.95
    ```

### 2. Gobuster (Descubrimiento de Contenido)
Gobuster se utiliza para realizar fuerza bruta sobre directorios y archivos web buscando recursos ocultos.
*   **Comando de verificación previa:**
    ```bash
    gobuster version
    ```
*   **Proceso de instalación (si no está presente):**
    ```bash
    sudo apt update
    sudo apt install gobuster
    ```
*   *Nota:* Tras la instalación, se vuelve a ejecutar `gobuster version` para asegurar que el binario está listo para ejecutarse.

### 3. Wappalyzer (Fingerprinting Tecnológico)
Utilizado para conocer frameworks, CMS, lenguajes, librerías y hosting del sitio web analizado.
*   **Instalación:** No se realiza mediante terminal. Se instaló directamente como **Extensión desde la Chrome Web Store** en el navegador del entorno de trabajo.

### 4. SecurityHeaders (Evaluación de Cabeceras)
Utilizado para evaluar de forma pasiva la presencia y calidad de las cabeceras HTTP de seguridad (como HSTS, CSP, X-Frame-Options).
*   **Instalación:** No requiere instalación.
*   **Uso:** Herramienta basada en web. Se accede directamente navegando a `https://securityheaders.com` e ingresando la URL del objetivo.
# 🛠️ Infraestructura, Entorno y Herramientas del Laboratorio

Este documento especifica la pila tecnológica, la estructura de archivos y las herramientas utilizadas durante el desarrollo del laboratorio de **Seguridad de Correos y Credenciales Corporativas**.

---

## 💻 1. Arquitectura del Entorno de Pruebas

* **Sistema Operativo Anfitrión:** Windows 10 Pro
* **Consola de Comandos:** Windows PowerShell
* **Capa de Virtualización / Subsistema:** WSL2 (Ubuntu Linux)
* **Motor de Contenedores:** Docker Desktop (Docker Engine / Docker Compose)
* **Gestor de Base de Datos:** MySQL 8.0 (Ejecutándose en contenedor aislado)
* **IDE / Editor de Código:** Visual Studio Code

---

## 📂 2. Estructura del Proyecto (`emailscorp/`)

```text
emailscorp/
│
├── docker-compose.yml          # Definición del contenedor MySQL 8.0 y volúmenes
├── aiaco_corporate_emails.csv  # Fuente de datos cruda de correos corporativos
├── case1.md                    # Documentación y análisis del caso de estudio
└── mysql/
      └── init.sql              # Script SQL de creación de DB e inserción de datos