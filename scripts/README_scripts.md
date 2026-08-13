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
```markdown
# 💻 Comandos, Consultas SQL y Casos de Estudio (Email Security)

Este documento contiene el registro de los comandos de administración de contenedores y todas las consultas SQL ejecutadas para el diagnóstico, clasificación, estadistas y remediación de la base de datos `aiaco`.

---

## 🐳 1. Comandos de Administración y Contenedores (Docker / WSL2)

```bash
# Verificación del estado de WSL2
wsl -l -v

# Validar estado del motor Docker y contenedores activos
docker version
docker compose version
docker ps

# Despliegue del entorno de laboratorio
docker compose up -d

# Inspección de logs de inicialización de la base de datos
docker logs aiaco_mysql

# Acceso interactivo a la consola de MySQL dentro del contenedor
docker exec -it aiaco_mysql mysql -u root -p
📊 2. Consultas SQL de Diagnóstico y Clasificación
Selección de base de datos e inspección inicial
SQL
SHOW DATABASES;
USE aiaco;
SHOW TABLES;
SELECT * FROM leaked_credentials;
Identificación de credenciales en texto plano
SQL
SELECT email, password_plain 
FROM leaked_credentials 
WHERE password_plain IS NOT NULL;
Búsqueda de contraseñas extremadamente débiles
SQL
SELECT email, password_plain 
FROM leaked_credentials 
WHERE password_plain IN ('password', '123456', 'admin', 'qwerty');
Identificación de usuarios con almacenamiento de hash
SQL
SELECT email, password_md5 
FROM leaked_credentials 
WHERE password_plain IS NULL;
Clasificación dinámica del nivel de riesgo
SQL
SELECT email,
  CASE 
    WHEN password_plain IS NOT NULL THEN 'CRITICO'
    ELSE 'MEDIO'
  END AS nivel_riesgo
FROM leaked_credentials;
Conteo estadístico general
SQL
SELECT 
  COUNT(*) AS total_usuarios,
  SUM(password_plain IS NOT NULL) AS texto_plano,
  SUM(password_plain IS NULL) AS solo_hash
FROM leaked_credentials;
Análisis de dominios corporativos
SQL
SELECT 
  SUBSTRING_INDEX(email, '@', -1) AS dominio,
  COUNT(*) AS total
FROM leaked_credentials
GROUP BY dominio;


🛠️ 3. Scripts SQL de Remediación y Validación
Creación de tabla de respaldo y saneamiento
SQL
-- Creación de la tabla de respaldo
CREATE TABLE leaked_credentials_backup AS SELECT * FROM leaked_credentials;

-- Eliminación de contraseñas en texto plano
UPDATE leaked_credentials_backup 
SET password_plain = NULL 
WHERE password_plain IS NOT NULL;
Validaciones post-remediación
SQL
-- Comprobar que no existan datos en texto plano (Resultado esperado: Empty set)
SELECT * FROM leaked_credentials_backup WHERE password_plain IS NOT NULL;

-- Confirmar la conservación de la totalidad de los usuarios (Resultado esperado: 5)
SELECT COUNT(*) FROM leaked_credentials_backup;

