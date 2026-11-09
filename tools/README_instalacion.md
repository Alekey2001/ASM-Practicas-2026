# Preparación del entorno de laboratorio

[Inicio](../README.md) · [Scripts y consultas](../scripts/README_scripts.md).

## Entornos históricos

El material documenta Windows, Kali Linux en VM y WSL2/Ubuntu para ejercicios diferentes. Los informes mencionan distintas ediciones de Windows; no se presume que todas las capturas provengan de una única instalación. Nmap, Gobuster, Wappalyzer, SecurityHeaders y MobSF son herramientas usadas en los casos; sus versiones históricas no equivalen a recomendaciones actuales de instalación.

La comprobación de cabeceras mediante un servicio web puede generar tráfico al activo. No se ejecutó reconocimiento externo durante esta revisión. Los comandos históricos se conservan en la [guía de scripts](../scripts/README_scripts.md).

## MySQL local: preparar secretos

Requisitos: Docker con Compose y un motor local disponible. Desde la raíz, en PowerShell:

```powershell
# Crear .env únicamente si todavía no existe.
if (-not (Test-Path -LiteralPath 'emailscorp/.env')) {
    Copy-Item -LiteralPath 'emailscorp/.env.example' -Destination 'emailscorp/.env'
}
```

Editar el archivo local y reemplazar los dos marcadores por secretos exclusivos del laboratorio. El [.env.example](../emailscorp/.env.example) contiene valores ficticios, no credenciales listas para usar. Mantener comillas simples alrededor de valores con `$` o `#`. El [.gitignore](../.gitignore) excluye el archivo local, pero no borra secretos de archivos ya seguidos o del historial.

```powershell
docker compose --env-file emailscorp/.env -f emailscorp/docker-compose.yml config --quiet
docker compose --env-file emailscorp/.env -f emailscorp/docker-compose.yml up -d
docker compose --env-file emailscorp/.env -f emailscorp/docker-compose.yml ps
docker compose --env-file emailscorp/.env -f emailscorp/docker-compose.yml logs mysql
docker compose --env-file emailscorp/.env -f emailscorp/docker-compose.yml exec mysql mysql -u root -p
```

La contraseña se solicita de forma interactiva. El servicio expone `127.0.0.1:3307`, no todas las interfaces del host. El script de inicialización se monta en solo lectura y se ejecuta automáticamente solo si el directorio de datos está vacío. El volumen nombrado conserva los datos.

**Volúmenes existentes:** cambiar `.env` no cambia las contraseñas ya guardadas por MySQL. La rotación debe hacerse de forma deliberada en esa instancia; no borrar el volumen para forzarla. No ejecutar el fixture con `DROP TABLE` sobre datos que se necesiten conservar.

Detener el laboratorio manteniendo el volumen:

```powershell
docker compose --env-file emailscorp/.env -f emailscorp/docker-compose.yml down
```

No añadir `--volumes` a ese comando si se quieren preservar los datos. Las contraseñas sintéticas de la tabla son material del ejercicio, distinto de los secretos del servicio MySQL.

## MailHog local, opcional

```powershell
docker compose -f scripts/docker-compose.yml config --quiet
docker compose -f scripts/docker-compose.yml up -d
docker compose -f scripts/docker-compose.yml down
```

SMTP escucha en `127.0.0.1:1025` y la interfaz en `127.0.0.1:8025`. MailHog usa almacenamiento en memoria: al recrear o detener el proceso se pueden perder mensajes del ejercicio. Se conserva la etiqueta histórica `latest`; fijar una versión o digest probado queda pendiente. No se inició este servicio durante la revisión.

## Archivos y datos

| Recurso | Propósito |
|---|---|
| [Compose MySQL](../emailscorp/docker-compose.yml) | Servicio y volumen de laboratorio |
| [Fixture SQL](../emailscorp/mysql/init.sql) | Datos vulnerables intencionales de inicialización |
| [Saneamiento de copia](../emailscorp/mysql/sanitize_copy.sql) | Ejercicio reproducible sin modificar la tabla original |
| [Generador](../scripts/email.py) | CSV sintético, con semilla y reemplazo explícitos |
| [Caso de identidades](../emailscorp/case1.md) | Evidencia y límites de remediación |

El generador y sus pruebas usan únicamente la biblioteca estándar de Python. Las herramientas de revisión de PDF requieren `pypdf`; las de OCR y anonimización usan Windows y .NET. No son dependencias de los laboratorios.
