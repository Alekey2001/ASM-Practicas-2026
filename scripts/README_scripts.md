# Scripts y comandos del laboratorio

[Inicio](../README.md) · [Preparación de MySQL y MailHog](../tools/README_instalacion.md).

## Generación de identidades sintéticas

[email.py](email.py) escribe por defecto en [emailscorp/aiaco_corporate_emails.csv](../emailscorp/aiaco_corporate_emails.csv), calculando la ruta desde el propio script. Funciona desde cualquier directorio si se invoca con la ruta correcta al script. No envía correos ni consulta servicios externos.

```powershell
python scripts/email.py --seed 42
# Solo si se desea reemplazar expresamente el CSV existente:
python scripts/email.py --seed 42 --count 50 --replace
# Pruebas aisladas; no cambian el CSV versionado:
python -m unittest discover -s scripts -p 'test_email.py' -v
```

`python` representa el intérprete seleccionado en el entorno del usuario. La semilla reproduce el conjunto en el mismo entorno; no se promete idéntica salida entre todas las versiones de Python. Se permiten entre 1 y 950 combinaciones únicas. La cabecera es `Nombre,Apellido,Email`; los correos son sintéticos, en minúsculas y sin acentos, bajo `aiaco.local`. Sin `--replace`, un archivo existente provoca salida no exitosa y permanece intacto. No se regeneró el CSV versionado en esta revisión.

## Fuentes de credenciales del ejercicio

[database.sql](database.sql) y [init.sql](../emailscorp/mysql/init.sql) representan el mismo fixture; [fault.json](fault.json) contiene esos mismos datos. Los tres son exclusivamente sintéticos. El CSV de identidades es independiente y no es un cargador de contraseñas ni de MySQL.

Los fixtures contienen `DROP TABLE` y solo se deben usar para inicialización de un laboratorio vacío. No ejecutar esos archivos como migración de una base existente. El saneamiento se hace con el [script separado](../emailscorp/mysql/sanitize_copy.sql).

## Consultas de diagnóstico sin divulgar contraseñas

```sql
USE aiaco;
SHOW TABLES;
SELECT COUNT(*) AS total,
       SUM(password_plain IS NOT NULL) AS texto_plano,
       SUM(password_md5 IS NOT NULL) AS con_md5,
       SUM(password_plain IS NULL AND password_md5 IS NOT NULL) AS solo_md5
FROM leaked_credentials;

SELECT SUBSTRING_INDEX(email, '@', -1) AS dominio, COUNT(*) AS total
FROM leaked_credentials GROUP BY dominio;

SELECT COUNT(*) AS contrasenas_triviales
FROM leaked_credentials
WHERE password_plain IN ('password', '123456', 'admin', 'qwerty');
```

El fixture permite esperar cinco registros, tres textos planos, cinco MD5 y dos registros con solo MD5. Esa expectativa no se presenta como ejecución de una base de datos actual. La asignación histórica de riesgo puede explorarse con `CASE WHEN password_plain IS NOT NULL THEN 'CRITICO' ELSE 'REVISAR_MD5' END`; no sustituye un análisis de impacto del sistema.

## Saneamiento reproducible de una copia

Con MySQL ya iniciado según la [guía de entorno](../tools/README_instalacion.md), desde la raíz:

```powershell
docker compose --env-file emailscorp/.env -f emailscorp/docker-compose.yml cp emailscorp/mysql/sanitize_copy.sql mysql:/tmp/asm-sanitize-copy.sql
docker compose --env-file emailscorp/.env -f emailscorp/docker-compose.yml exec mysql mysql -u root -p
```

En la consola MySQL:

```sql
SOURCE /tmp/asm-sanitize-copy.sql;
-- Repetir para comprobar idempotencia sobre el mismo fixture:
SOURCE /tmp/asm-sanitize-copy.sql;
```

El script crea `leaked_credentials_sanitized`, conserva el original y muestra validaciones antes/después sin secretos. Los resultados esperados y las limitaciones están en el [caso de identidades](../emailscorp/case1.md). No recrea ni sustituye la copia histórica `leaked_credentials_backup`; los resultados de las capturas corresponden a esa otra tabla. MD5 continúa presente: Argon2id/bcrypt y la migración de autenticación siguen pendientes.

## Comandos históricos de reconocimiento web

Se preservan para interpretar las evidencias de `aiaco.netlify.app`. **No ejecutados durante esta revisión.** Repetirlos requiere alcance y autorización vigentes; Nmap y Gobuster generan tráfico.

```bash
nmap --version
gobuster version
sudo apt update
sudo apt install gobuster
gobuster version
```

El material histórico menciona `nmap -A`; la captura inicial disponible muestra `-sV`. No se atribuyen a la captura todas las funciones de `-A` (detección de SO, scripts y traceroute).

```bash
# Comando descrito en la documentación histórica:
nmap -A aiaco.netlify.app
# Detección de versiones visible en la captura:
nmap -sV aiaco.netlify.app
nmap --script http-title,http-headers,http-methods -p 80,443 aiaco.netlify.app
gobuster dir -u https://aiaco.netlify.app -w /usr/share/wordlists/dirb/common.txt
```

`-sV` intenta identificar versiones; `-p` selecciona puertos; los scripts NSE consultan título, cabeceras y métodos; `dir` enumera rutas con el diccionario indicado por `-w`. Los ejemplos son históricos, no una prueba de ejecución nueva ni una guía de instalación actualizada.

## Validación del repositorio

```powershell
python scripts/validate_repository.py
python -m unittest discover -s scripts -p 'test_email.py' -v
git diff --check
git diff --cached --check
```

El validador comprueba archivos locales y no contacta URLs externas. Los límites de SQL/Compose y de la evidencia pública se registran en la [fe de erratas pública](../docs/public/FE_DE_ERRATAS.md).
