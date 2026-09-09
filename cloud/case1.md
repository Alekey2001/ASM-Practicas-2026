# ☁️ AIACO AWS DevSecOps & Cloud Security Lab

Laboratorio práctico de infraestructura, administración, DevSecOps y seguridad en Amazon Web Services (AWS).

El objetivo del proyecto es construir una infraestructura cloud controlada que posteriormente permita realizar prácticas de **Red Team, Blue Team, hardening, monitoreo, detección y respuesta a incidentes**.

> **Entorno educativo y autorizado.**  
> Todas las pruebas de seguridad documentadas en este repositorio se realizan exclusivamente sobre infraestructura propia y autorizada.
---
## 1. Arquitectura del laboratorio
Región principal utilizada:
```text
AWS Region: us-east-1
US East (N. Virginia)
```

Servicios trabajados hasta el momento:

- Amazon EC2
- AWS Lambda
- Amazon Aurora PostgreSQL
- Amazon Bedrock
- AWS Budgets
- AWS IAM
- AWS CloudShell
- AWS CLI
- AWS STS
Arquitectura general:

```text
                  AWS CLOUD
                     │
              us-east-1
                     │
        ┌────────────┴─────────────┐
        │                          │
       EC2                       Lambda
 devsecops-lab                lab-aws-APT
        │                          │
 Ubuntu 22.04                Node.js 24.x
        │                     Function URL
        │
        └──────────┐
                   │
                   ▼
           Aurora PostgreSQL
               Serverless
             database-1
                   │
             PostgreSQL 17.7
```

---

# 2. Amazon EC2

## Instancia principal

| Parámetro | Configuración |
|---|---|
| Nombre | `devsecops-lab` |
| Tipo | `t3.micro` |
| Región | `us-east-1` |
| Zona de disponibilidad | `us-east-1d` |
| Sistema operativo | Ubuntu Server 22.04 LTS |
| Plataforma | Linux/UNIX |
| Arquitectura AMI | AMD64 |
| Virtualización | HVM |
| vCPU | 2 |
| Estado actual | Detenida |
| IPv4 privada | `172.31.34.81` |
| IPv4 pública actual | No asignada |
| IPv6 | No asignada |
| Security Group | `launch-wizard-3` |
| Key Pair | `devsecops-key-new` |
| IAM Role | No asignado |
| Monitoreo detallado | Desactivado |
| IMDSv2 | Optional |

La instancia utiliza la AMI:

```text
ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20260503
```

El hostname privado generado por AWS es:

```text
ip-172-31-34-81.ec2.internal
```

---

# 3. Red AWS

La instancia EC2 está desplegada dentro de una VPC y una subred de AWS.

```text
EC2
 │
 ├── VPC
 │
 ├── Subnet
 │
 ├── Private IPv4
 │
 └── Security Group
```

La instancia actualmente no dispone de:

- Elastic IP
- IPv6
- DNS público
- IPv4 pública

Esto se debe considerar al realizar las futuras pruebas de conectividad y exposición externa.

---

# 4. Security Group

Security Group asociado:

```text
launch-wizard-3
```

Las reglas de entrada y salida serán auditadas durante la fase de reconocimiento del laboratorio.

El objetivo será determinar:

- Puertos permitidos.
- Protocolos permitidos.
- Orígenes autorizados.
- Servicios expuestos a Internet.
- Reglas excesivamente permisivas.
- Posibles mejoras de hardening.

---

# 5. Instance Metadata Service — IMDS

Estado actual:

```text
IMDSv2: Optional
```

Esto significa que la instancia permite IMDSv2 pero actualmente no está configurada para exigirlo obligatoriamente.

Durante la fase Blue Team se evaluará cambiar la configuración a:

```text
HttpTokens = required
```

para exigir IMDSv2.

---

# 6. IAM

Actualmente la instancia EC2 no tiene un IAM Role asociado.

```text
EC2
 │
 └── IAM Role: NONE
```

Además, durante las pruebas administrativas se verificó la identidad utilizada mediante:

```bash
aws sts get-caller-identity
```

La sesión administrativa utilizada correspondía a la identidad root de la cuenta.

Esto se documenta como un punto de mejora de seguridad.

Durante la fase Blue Team se trabajará en:

- Separación del usuario root.
- Identidades administrativas.
- IAM Roles.
- Políticas IAM.
- Least Privilege.
- MFA.
- Rotación/eliminación de credenciales innecesarias.

---

# 7. AWS Lambda

Se creó una función AWS Lambda para estudiar arquitectura Serverless.

Configuración utilizada:

```text
Runtime: Node.js 24.x
Architecture: x86_64
Function URL: Enabled
Invocation Mode: BUFFERED
CORS: Disabled
```

Para el laboratorio inicial se utilizó una Function URL pública.

Esto permitió estudiar el flujo:

```text
Cliente
   │
 HTTPS
   │
   ▼
Function URL
   │
   ▼
AWS Lambda
   │
Node.js
   │
   ▼
HTTP Response
```

En un entorno productivo se deberán evaluar mecanismos adicionales de autenticación y autorización.

---

# 8. Amazon Aurora PostgreSQL Serverless

Se desplegó un clúster Aurora PostgreSQL mediante AWS CloudShell y AWS CLI.

Comando utilizado:

```bash
aws rds create-db-cluster \
  --db-cluster-identifier database-1 \
  --engine aurora-postgresql \
  --with-express-configuration \
  --region us-east-1
```

Configuración obtenida:

```text
Cluster: database-1
Engine: aurora-postgresql
Engine Version: 17.7
Port: 5432
Master Username: postgres
Serverless: Enabled
Status: available
```

La configuración Express estableció un entorno Aurora Serverless.

El estado fue verificado mediante:

```bash
aws rds describe-db-clusters \
  --db-cluster-identifier database-1 \
  --region us-east-1 \
  --query "DBClusters[0].[DBClusterIdentifier,Status,Engine,EngineVersion]" \
  --output table
```

Resultado:

```text
database-1
available
aurora-postgresql
17.7
```

---

# 9. AWS CloudShell y AWS CLI

AWS CloudShell fue utilizado para administrar y verificar recursos directamente mediante CLI.

Primero se comprobó la identidad activa:

```bash
aws sts get-caller-identity
```

Posteriormente se utilizó AWS CLI para:

- Crear Aurora.
- Consultar clústeres RDS/Aurora.
- Verificar estados.
- Consultar las actividades de AWS Free Tier.

Esto permitió continuar trabajando incluso cuando una operación de la interfaz web de AWS Console no respondía correctamente.

---

# 10. Amazon Bedrock

Se realizó una prueba básica con Amazon Bedrock utilizando:

```text
Model Provider: Amazon
Model: Nova 2 Lite
Inference: Global
```

Se realizó una invocación controlada desde el Playground para comprender el funcionamiento básico de los Foundation Models administrados mediante AWS.

---

# 11. AWS Budgets

Se configuró AWS Budgets como mecanismo de control financiero del laboratorio.

Su objetivo es:

- Supervisar consumo.
- Detectar incrementos de gasto.
- Mantener control sobre los créditos disponibles.
- Evitar despliegues innecesarios.

El laboratorio prioriza recursos compatibles con el AWS Free Plan y los créditos disponibles.

---

# 12. Explore AWS

Se realizaron las actividades prácticas disponibles en Explore AWS.

Estado confirmado mediante:

```bash
aws freetier list-account-activities \
  --language-code es-ES \
  --query "activities[*].[title,status,reward.credit.amount]" \
  --output table
```

Estado registrado:

| Actividad | Estado | Reward |
|---|---|---:|
| AWS Budgets | COMPLETED | $20 |
| Amazon EC2 | COMPLETED | $20 |
| Amazon Bedrock | COMPLETED | $20 |
| AWS Lambda | COMPLETED | $20 |
| Amazon Aurora / RDS | NOT_STARTED* | $20 |

**Créditos confirmados por Explore AWS: $80 USD.**

### Incidencia RDS/Aurora

Aurora fue desplegado correctamente mediante AWS CLI y alcanzó:

```text
Status: available
```

Sin embargo, el sistema de actividades Free Tier continúa mostrando:

```text
Crear una base de datos de Aurora o RDS
Status: NOT_STARTED
```

Por este motivo, la recompensa correspondiente a esta actividad no se considera obtenida hasta que AWS registre oficialmente su finalización.

---

# 13. Estado actual de seguridad

Antes de comenzar las pruebas ofensivas se identificaron los siguientes puntos para revisión:

| Área | Estado actual | Próxima revisión |
|---|---|---|
| EC2 | Detenida | Preparar para laboratorio |
| IPv4 pública | No asignada actualmente | Revisar al iniciar EC2 |
| IAM Role EC2 | No asignado | Least Privilege |
| IMDSv2 | Optional | Evaluar `required` |
| Root account | Utilizada administrativamente | Hardening IAM |
| Security Group | `launch-wizard-3` | Auditar reglas |
| Monitoring EC2 | Desactivado | Evaluar monitoreo |
| Lambda Function URL | Pública para laboratorio | Revisar autenticación |
| Aurora | Available | Revisar exposición y acceso |

Estos elementos todavía no representan automáticamente vulnerabilidades confirmadas. Serán evaluados individualmente durante las fases Red Team y Blue Team.

---

# 14. Metodología del laboratorio

El proyecto seguirá cuatro fases.

## Fase 1 — Asset Discovery & Scope

```text
Inventario
   ↓
EC2
   ↓
Networking
   ↓
Security Groups
   ↓
IAM
   ↓
Superficie autorizada
```

Objetivo:

Definir exactamente qué recursos pertenecen al laboratorio y cuáles están autorizados para pruebas.

---

## Fase 2 — Red Team

Se realizarán pruebas controladas sobre infraestructura propia.

Objetivos:

- Reconocimiento.
- Enumeración.
- Identificación de exposición.
- Análisis de configuraciones.
- Validación controlada de hallazgos.
- Generación de eventos de seguridad.

---

## Fase 3 — Blue Team

Los eventos generados durante Red Team serán utilizados para trabajar en:

- Hardening.
- Logging.
- Monitoring.
- IAM.
- CloudTrail.
- CloudWatch.
- Security Groups.
- Detección.
- Alertamiento.
- Respuesta a incidentes.

---

## Fase 4 — DevSecOps

Cada hallazgo seguirá el ciclo:

```text
Detect
  ↓
Analyze
  ↓
Remediate
  ↓
Validate
  ↓
Document
```

Para cada vulnerabilidad o misconfiguration se documentará:

1. Activo afectado.
2. Evidencia.
3. Riesgo.
4. Impacto.
5. Remediación.
6. Validación posterior.

---
# 15. Próximo paso

El siguiente objetivo del laboratorio es completar el inventario de seguridad de:

```text
devsecops-lab
```

especialmente:

```text
Security Group
     │
     ├── Inbound Rules
     └── Outbound Rules
```
Después se establecerá formalmente el alcance autorizado antes de comenzar cualquier prueba Red Team.
---
## Disclaimer

Este repositorio tiene fines exclusivamente educativos, profesionales y de laboratorio.
Las técnicas de seguridad se ejecutan únicamente sobre sistemas propios o expresamente autorizados.