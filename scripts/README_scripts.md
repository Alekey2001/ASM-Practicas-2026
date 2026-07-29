# 📜 Documentación Completa de Comandos y Scripts de mapeo web 

Este archivo contiene la relación exhaustiva de **todos los comandos** ejecutados en la terminal de Kali Linux durante las fases de verificación, instalación de herramientas y el mapeo de superficie del activo web `https://aiaco.netlify.app`.

---

## 🛠️ 1. Fase de Verificación e Instalación de Herramientas

### 1.1. Verificación de Nmap
Comando ejecutado para comprobar si Nmap estaba instalado en el sistema y revisar su versión actual.
```bash
nmap --version
1.2. Verificación Previa de Gobuster
Comando para revisar si la herramienta Gobuster ya se encontraba disponible en el sistema.

Bash
gobuster version
1.3. Actualización de Repositorios e Instalación de Gobuster
Comandos para actualizar la lista de paquetes de Kali Linux e instalar Gobuster.

Bash
sudo apt update
sudo apt install gobuster
1.4. Re-verificación de Gobuster
Comando ejecutado tras la instalación para confirmar que el binario quedó instalado correctamente.

Bash
gobuster version
🔍 2. Fase de Reconocimiento y Escaneo con Nmap
2.1. Escaneo Completo y Agresivo
Primer escaneo ejecutado contra el dominio objetivo para descubrir puertos abiertos, servicios, versiones y sistema operativo.

Bash
nmap -A aiaco.netlify.app
-A: Habilita detección de SO, detección de versiones de servicios, escaneo de scripts predeterminados y traceroute en un solo comando.

2.2. Escaneo Específico de Encabezados, Métodos y Título HTTP
Segundo escaneo ejecutado con el motor de scripts de Nmap (NSE) enfocado exclusivamente en los puertos web para auditar la seguridad de las cabeceras y métodos.

Bash
nmap --script http-title,http-headers,http-methods -p 80,443 aiaco.netlify.app
--script http-title,http-headers,http-methods: Ejecuta los tres scripts NSE seleccionados.

http-title: Extrae el título HTML del sitio ("AIACO").

http-headers: Muestra los encabezados de respuesta del servidor (Server, HSTS, Cache-Control, etc.).

http-methods: Enumera los métodos HTTP habilitados (GET, HEAD, POST, OPTIONS).

-p 80,443: Restringe el escaneo a los puertos 80 (HTTP) y 443 (HTTPS).

📂 3. Fase de Descubrimiento de Contenido con Gobuster
3.1. Fuerza Bruta de Directorios y Archivos (Fuzzing)
Comando ejecutado para realizar búsquedas de directorios ocultos, archivos públicos, respaldos o paneles administrativos.

Bash
gobuster dir -u [https://aiaco.netlify.app](https://aiaco.netlify.app) -w /usr/share/wordlists/dirb/common.txt
dir: Indica que se utilizará el modo de enumeración de directorios/URIs.

-u https://aiaco.netlify.app: URL objetivo a analizar.

-w /usr/share/wordlists/dirb/common.txt: Especifica la ruta completa del diccionario utilizado (common.txt de DIRB en Kali Linux).