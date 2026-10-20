# Caso 2 — Exposición pública de SSH y simulación controlada de acceso

## 1. Descripción

Durante la evaluación de seguridad de la instancia EC2 `devsecops-lab` se identificó que el servicio SSH estaba expuesto públicamente a Internet mediante TCP/22.

El objetivo fue comprobar la exposición del servicio y realizar una simulación controlada de un intento de acceso utilizando un usuario inexistente, sin utilizar credenciales legítimas ni realizar fuerza bruta.

---

## 2. Activo analizado

| Elemento            | Valor              |
| ------------------- | ------------------ |
| Servicio            | SSH                |
| Puerto              | TCP/22             |
| Sistema operativo   | Ubuntu 22.04.5 LTS |
| Instancia           | devsecops-lab      |
| Tipo                | t3.micro           |
| Región              | us-east-1          |
| Security Group      | launch-wizard-3    |
| IP pública evaluada | 34.235.163.220     |

---

## 3. Situación inicial

El Security Group permitía:

```text
TCP/22
Source: 0.0.0.0/0
```

Esto significaba que cualquier dirección IPv4 podía intentar conectarse al servicio SSH.

La exposición no implicaba automáticamente un compromiso, pero representaba una superficie de ataque innecesariamente amplia.

---

## 4. Reconocimiento

Se utilizó Nmap para comprobar el servicio:

```powershell
nmap -Pn -p 22 -sV --reason <IP_PUBLICA>
```

El servicio fue identificado como:

```text
22/tcp open ssh
OpenSSH 8.9p1 Ubuntu
```

También se confirmó conectividad mediante:

```powershell
Test-NetConnection <IP_PUBLICA> -Port 22
```

Resultado:

```text
TcpTestSucceeded : True
```

---

## 5. Revisión de configuración SSH

Se ejecutó:

```bash
sudo sshd -T | grep -Ei 'permitrootlogin|passwordauthentication|pubkeyauthentication|kbdinteractiveauthentication|x11forwarding|port|authenticationmethods'
```

Se obtuvo:

```text
port 22
permitrootlogin no
pubkeyauthentication yes
passwordauthentication no
kbdinteractiveauthentication no
x11forwarding yes
authenticationmethods any
```

---

## 6. Controles positivos identificados

La configuración presentaba varios controles de seguridad:

* Acceso SSH directo como root deshabilitado.
* Autenticación mediante contraseña deshabilitada.
* Autenticación mediante clave pública habilitada.
* Autenticación interactiva deshabilitada.

Esto reducía significativamente la posibilidad de acceso mediante credenciales de contraseña.

---

## 7. Simulación Red Team

Se realizó un intento controlado utilizando un usuario inexistente:

```powershell
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no usuario-falso@34.235.163.220
```

No se utilizó la llave privada `.pem`.

La finalidad fue simular el comportamiento de un atacante externo que no dispone de la clave legítima.

---

## 8. Resultado

El servidor respondió:

```text
Permission denied (publickey).
```

Esto confirmó:

* El servicio era accesible.
* El usuario inexistente no pudo autenticarse.
* La autenticación por contraseña no estaba disponible.
* No se obtuvo una sesión.
* No se consiguió acceso al sistema.

---

## 9. Análisis de logs

Se revisaron los registros de autenticación:

```bash
sudo grep -Ei 'usuario-falso|Failed|Invalid user|authentication failure' /var/log/auth.log | tail -30
```

Se encontraron eventos relacionados con:

```text
Invalid user usuario-falso
```

y:

```text
Connection reset by invalid user usuario-falso
```

Estos registros demostraron que el sistema registra intentos de usuarios inválidos.

Los eventos históricos encontrados no fueron atribuidos automáticamente al último intento debido a diferencias temporales y de contexto.

---

## 10. Evaluación de Fail2Ban

Se verificó:

```bash
sudo fail2ban-client status
```

El jail SSH estaba activo:

```text
sshd
```

Posteriormente:

```bash
sudo fail2ban-client status sshd
```

Resultado:

```text
Currently failed: 0
Total failed: 0
Currently banned: 0
Total banned: 0
```

Por lo tanto, durante esta prueba no se produjo un bloqueo mediante Fail2Ban.

No se debe considerar que Fail2Ban bloqueó el intento.

---

## 11. Riesgo identificado

El principal riesgo fue la exposición pública del servicio SSH:

```text
Internet
   ↓
TCP/22
   ↓
EC2
```

Además, la cuenta administrativa `devsecops` pertenecía al grupo `sudo`.

Esto implica que el compromiso de una llave SSH administrativa podría tener un impacto elevado.

---

## 12. Remediación Blue Team

La medida de seguridad propuesta consiste en modificar la regla del Security Group:

### Configuración inicial

```text
TCP/22
0.0.0.0/0
```

### Configuración recomendada

```text
TCP/22
IP_ADMINISTRATIVA/32
```

De esta forma, únicamente la dirección administrativa autorizada podrá iniciar conexiones SSH.

---

## 13. Estado de remediación

**Estado: PENDIENTE DE CIERRE/VALIDACIÓN**

El hallazgo fue identificado y la medida de remediación quedó definida.

Para cerrar completamente el caso se debe:

1. Cambiar el origen de TCP/22.
2. Mantener abierta la sesión SSH actual durante el cambio.
3. Verificar acceso desde la IP autorizada.
4. Confirmar que una IP no autorizada no pueda establecer conexión.
5. Documentar el resultado.

---

## 14. Clasificación

| Elemento                   | Resultado                             |
| -------------------------- | ------------------------------------- |
| Hallazgo                   | SSH expuesto públicamente             |
| Severidad inicial          | Alta                                  |
| Ataque                     | Simulación controlada                 |
| Acceso obtenido            | No                                    |
| Credenciales comprometidas | No                                    |
| Fuerza bruta               | No                                    |
| Persistencia               | No                                    |
| Fail2Ban                   | Activo, sin bloqueo durante la prueba |
| Remediación                | Restricción de Security Group         |
| Estado                     | Pendiente de validación               |

---

## 15. Conclusión

La prueba demostró que el servicio SSH era públicamente accesible, pero los controles de autenticación existentes impidieron obtener acceso mediante el usuario falso utilizado durante la simulación.

El principal riesgo identificado fue la exposición innecesaria del puerto SSH a Internet.

La recomendación principal es restringir el acceso TCP/22 a la dirección IP administrativa autorizada mediante una regla `/32`.

El caso debe considerarse completamente cerrado únicamente después de aplicar y validar dicha restricción.
