# Caso 3 — Exposición de EC2 Instance Metadata Service e implementación de IMDSv2

## 1. Descripción

Durante la evaluación de seguridad de la instancia EC2 `devsecops-lab` se analizó el comportamiento del Amazon EC2 Instance Metadata Service (IMDS).

La configuración inicial permitía utilizar IMDSv1 porque IMDSv2 estaba configurado como `Optional`.

Se realizó una prueba controlada para determinar si el endpoint de metadata podía ser consultado sin proporcionar un token.

Posteriormente se implementó la medida de Blue Team consistente en hacer obligatorio IMDSv2.

---

## 2. Objetivo

Los objetivos fueron:

* Comprobar el acceso al servicio de metadata.
* Determinar si IMDSv2 era obligatorio.
* Evaluar el riesgo asociado con una configuración permisiva.
* Determinar si existía un IAM Role asociado.
* Evitar extracción de credenciales.
* Aplicar hardening.
* Validar la nueva configuración.

---

## 3. Activo analizado

| Elemento          | Valor                         |
| ----------------- | ----------------------------- |
| Servicio          | EC2 Instance Metadata Service |
| Endpoint          | 169.254.169.254               |
| Instancia         | devsecops-lab                 |
| Región            | us-east-1                     |
| Sistema operativo | Ubuntu 22.04.5 LTS            |
| IMDS inicial      | Optional                      |
| IAM Role          | Ninguno                       |

---

## 4. Situación inicial

La configuración de metadata era:

```text
IMDSv2: Optional
```

Esto significaba que no era obligatorio proporcionar un token de IMDSv2 para consultar el servicio.

Esta configuración incrementaba la superficie de riesgo en escenarios donde una aplicación vulnerable pudiera realizar solicitudes HTTP internas, por ejemplo, mediante una vulnerabilidad SSRF.

---

## 5. Simulación Red Team

Se realizó una consulta controlada:

```bash
curl -s http://169.254.169.254/latest/meta-data/
```

La instancia respondió con diferentes categorías de metadata, incluyendo:

```text
ami-id
hostname
instance-id
instance-type
local-ipv4
mac
network/
placement/
public-hostname
public-ipv4
public-keys/
security-groups
services/
```

---

## 6. Resultado

La respuesta confirmó que el servicio de metadata era accesible sin proporcionar inicialmente un token.

Esto confirmó la condición:

```text
IMDSv2 Optional
```

y permitió identificar una oportunidad de hardening.

---

## 7. Revisión de IAM

Se realizó una consulta controlada:

```bash
curl -s http://169.254.169.254/latest/meta-data/iam/info
```

La respuesta fue:

```text
404
```

La evaluación de la instancia confirmó que:

```text
IAM Role = ninguno
```

Por lo tanto, no existían credenciales temporales de un Instance Profile disponibles para esta instancia.

---

## 8. Alcance de la prueba

La prueba se mantuvo deliberadamente dentro de un alcance seguro.

No se realizó:

* Extracción de credenciales AWS.
* Robo de tokens.
* Acceso a recursos externos.
* Escalada de privilegios.
* Persistencia.
* Modificación destructiva.
* Explotación de terceros.

El objetivo fue únicamente demostrar la condición de configuración y posteriormente corregirla.

---

## 9. Validación de IMDSv2

Se comprobó que el mecanismo de token estaba disponible mediante una solicitud PUT al endpoint de token.

Se utilizó un TTL corto de:

```text
60 segundos
```

Esto permitió demostrar que IMDSv2 estaba disponible sin realizar acciones adicionales sobre recursos AWS.

---

## 10. Remediación Blue Team

Desde AWS Console se modificó la configuración de metadata de la instancia:

### Antes

```text
IMDSv2: Optional
```

### Después

```text
IMDSv2: Required
```

La modificación obligó a utilizar el mecanismo de autenticación mediante token para acceder al servicio.

---

## 11. Validación posterior

Después de aplicar la modificación se ejecutó:

```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
http://169.254.169.254/latest/meta-data/
```

Resultado:

```text
HTTP 401
```

---

## 12. Interpretación del resultado

El código:

```text
401 Unauthorized
```

demostró que las solicitudes sin el mecanismo requerido ya no podían acceder al servicio de metadata.

La situación evolucionó de:

```text
IMDSv2 Optional
```

a:

```text
IMDSv2 Required
```

con validación exitosa.

---

## 13. Riesgo inicial

La configuración inicial representaba un riesgo de seguridad principalmente en escenarios donde se combinara con:

* Vulnerabilidades SSRF.
* Aplicaciones comprometidas.
* Acceso no autorizado a procesos internos.
* Instance Profiles con permisos excesivos.

En este laboratorio no existía un IAM Role asociado, por lo que no había credenciales temporales de Instance Profile que pudieran ser obtenidas.

---

## 14. Resultado Blue Team

La remediación fue aplicada correctamente.

La validación confirmó:

```text
Solicitud sin token
        ↓
IMDSv2 Required
        ↓
HTTP 401
```

Esto confirma que la protección se encontraba funcionando.

---

## 15. Clasificación

| Elemento                   | Resultado                       |
| -------------------------- | ------------------------------- |
| Hallazgo                   | IMDSv2 no obligatorio           |
| Configuración inicial      | Optional                        |
| Prueba                     | Consulta controlada de metadata |
| IAM Role                   | No asociado                     |
| Credenciales AWS extraídas | No                              |
| Remediación                | IMDSv2 Required                 |
| Validación                 | HTTP 401                        |
| Estado                     | Completado                      |
| Riesgo posterior           | Bajo/Controlado                 |

---

## 16. Lecciones aprendidas

La configuración de IMDS es un componente importante del hardening de EC2.

La utilización obligatoria de IMDSv2 reduce el riesgo de accesos no autenticados al servicio de metadata y constituye una medida defensiva importante frente a determinados escenarios de SSRF.

También se comprobó la importancia de aplicar el principio de mínimo privilegio. La ausencia de un IAM Role innecesario evitó que existieran credenciales de Instance Profile disponibles en la instancia.

---

## 17. Recomendaciones

Se recomienda:

* Mantener IMDSv2 como `Required`.
* Evitar IMDSv1 cuando no sea estrictamente necesario.
* Aplicar mínimo privilegio a los IAM Roles.
* No asignar permisos AWS innecesarios a instancias.
* Revisar aplicaciones susceptibles a SSRF.
* Mantener actualizados los componentes del sistema.
* Registrar cambios de configuración.
* Revisar periódicamente las configuraciones de EC2.

---

## 18. Conclusión

La evaluación confirmó que la instancia inicialmente permitía acceso al servicio de metadata sin exigir obligatoriamente IMDSv2.

La prueba fue controlada y no se realizó extracción de credenciales ni explotación adicional.

Posteriormente se modificó la configuración de EC2 para establecer:

```text
IMDSv2 Required
```

La validación posterior devolvió:

```text
HTTP 401
```

confirmando que las solicitudes sin el mecanismo requerido eran rechazadas.

Por lo tanto, el caso fue **remediado y validado correctamente**.
