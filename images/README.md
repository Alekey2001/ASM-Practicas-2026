# Índice de imágenes y trazabilidad

[Inicio](../README.md) · [Resultados](../docs/revision/RESULTADOS.md) · [Tabla CSV con SHA-256](../docs/revision/clasificacion-imagenes.csv).

Las 57 imágenes se clasificaron por inspección visual. Se conservaron 56 sin cambiar un byte. La captura de arranque MobSF es una copia anonimizada autorizada, con respaldo cifrado del original fuera del repositorio. Los nombres históricos se conservan en la tabla para trazabilidad, no como rutas vigentes.

La carpeta adicional `cloud-aws/services/` agrupa Bedrock, Lambda, Aurora y actividades formativas que no corresponden a SSH o EC2. No se crearon carpetas vacías de remediación móvil: no hay evidencia de un parche. No quedaron archivos sin clasificación; la categoría visual no acredita que el hallazgo esté validado.

Casos: [Web](../sitiosweb/README_mapeo_web.md), [Identidades/DB](../emailscorp/case1.md), [AWS](../cloud/case1.md), [OSINT](../redes/README_osint.md), [Mobile](../apps/case1.md).

Antes de publicar deben revisarse datos de cuenta, IP, nombres, rutas y material de terceros en las capturas. Las contraseñas de las capturas SQL pertenecen al fixture sintético. La ilustración conceptual generada no es evidencia de una prueba. Véase [privacidad y publicación](../docs/revision/PRIVACIDAD.md).

| Origen histórico | Destino | Categoría | Justificación |
|---|---|---|---|
| `wevnmap1.PNG` | [web/nmap/puertos-servicios.png](web/nmap/puertos-servicios.png) | web/nmap | Salida Nmap con puertos 53, 80 y 443 |
| `webnmap2.PNG` | [web/nmap/metodos-cabeceras.png](web/nmap/metodos-cabeceras.png) | web/nmap | Salida NSE de métodos y cabeceras |
| `segurityheaders1.PNG` | [web/headers/evaluacion-cabeceras.png](web/headers/evaluacion-cabeceras.png) | web/headers | Resumen SecurityHeaders |
| `segurityheaders2.PNG` | [web/headers/cabeceras-detalle.png](web/headers/cabeceras-detalle.png) | web/headers | Cabeceras HTTP y recomendaciones |
| `wapp1.PNG` | [web/fingerprinting/wappalyzer-tecnologias.png](web/fingerprinting/wappalyzer-tecnologias.png) | web/fingerprinting | Wappalyzer sobre el sitio AIACO |
| `gobuster.PNG` | [web/gobuster/instalacion.png](web/gobuster/instalacion.png) | web/gobuster | Instalación de Gobuster |
| `gofisher1.PNG` | [web/gobuster/diccionarios.png](web/gobuster/diccionarios.png) | web/gobuster | Listado de diccionarios DIRB |
| `gofisher2.PNG` | [web/gobuster/enumeracion-inicio.png](web/gobuster/enumeracion-inicio.png) | web/gobuster | Ejecución de Gobuster; no es phishing |
| `gofisher3.PNG` | [web/gobuster/enumeracion-resultados.png](web/gobuster/enumeracion-resultados.png) | web/gobuster | Resultados HTTP de Gobuster |
| `version.PNG` | [web/gobuster/version-ayuda.png](web/gobuster/version-ayuda.png) | web/gobuster | Ayuda y versión de Gobuster |
| `webtools1.PNG` | [web/gobuster/documentacion-herramienta.png](web/gobuster/documentacion-herramienta.png) | web/gobuster | Página de herramienta Gobuster en Kali |
| `EMAILDATA1.PNG` | [identity-database/mysql/inicializacion-consulta.png](identity-database/mysql/inicializacion-consulta.png) | identity-database/mysql | Consola MySQL con tabla del fixture |
| `database3.PNG` | [identity-database/mysql/conteo-original.png](identity-database/mysql/conteo-original.png) | identity-database/mysql | Conteo de cinco registros originales |
| `database5.PNG` | [identity-database/mysql/clasificacion-riesgo.png](identity-database/mysql/clasificacion-riesgo.png) | identity-database/mysql | Consultas de clasificación del fixture |
| `database6.PNG` | [identity-database/mysql/resumen-original.png](identity-database/mysql/resumen-original.png) | identity-database/mysql | Conteo original: cinco registros; tres textos planos |
| `database2.PNG` | [identity-database/credentials/texto-plano-sintetico.png](identity-database/credentials/texto-plano-sintetico.png) | identity-database/credentials | Tres credenciales sintéticas en texto plano |
| `database 4.PNG` | [identity-database/credentials/credenciales-debiles-sinteticas.png](identity-database/credentials/credenciales-debiles-sinteticas.png) | identity-database/credentials | Consultas de contraseñas débiles del fixture |
| `database7.PNG` | [identity-database/remediation/conteos-original-copia.png](identity-database/remediation/conteos-original-copia.png) | identity-database/remediation | Cinco registros en original y copia |
| `database8.PNG` | [identity-database/remediation/saneamiento-copia.png](identity-database/remediation/saneamiento-copia.png) | identity-database/remediation | UPDATE sobre copia y resultados antes/después |
| `database9.PNG` | [identity-database/remediation/conteo-copia-saneada.png](identity-database/remediation/conteo-copia-saneada.png) | identity-database/remediation | Cero textos planos en la copia |
| `database10.PNG` | [identity-database/remediation/repeticion-saneamiento.png](identity-database/remediation/repeticion-saneamiento.png) | identity-database/remediation | UPDATE repetido sin cambios en la copia |
| `database11.PNG` | [identity-database/remediation/comparacion-original-copia.png](identity-database/remediation/comparacion-original-copia.png) | identity-database/remediation | Original vulnerable frente a copia saneada |
| `DATABASE1ALS.PNG` | [identity-database/remediation/validacion-integridad-copia.png](identity-database/remediation/validacion-integridad-copia.png) | identity-database/remediation | Cinco registros; original con tres textos planos; copia con cero |
| `DATABASEALS.PNG` | [identity-database/remediation/validacion-texto-plano-copia.png](identity-database/remediation/validacion-texto-plano-copia.png) | identity-database/remediation | Conteo de textos planos exclusivamente en copia |
| `estanacia ec2 aws.PNG` | [cloud-aws/ec2/instancia-consola.png](cloud-aws/ec2/instancia-consola.png) | cloud-aws/ec2 | Consola EC2, instancia detenida |
| `scanversions.PNG` | [cloud-aws/ec2/sistema-operativo.png](cloud-aws/ec2/sistema-operativo.png) | cloud-aws/ec2 | Identidad del sistema Ubuntu |
| `lisent.PNG` | [cloud-aws/ec2/servicios-escuchando.png](cloud-aws/ec2/servicios-escuchando.png) | cloud-aws/ec2 | Sockets y servicios de la instancia |
| `awssw.PNG` | [cloud-aws/ec2/servicios-systemd.png](cloud-aws/ec2/servicios-systemd.png) | cloud-aws/ec2 | Listado systemd |
| `ramas.PNG` | [cloud-aws/ec2/servicios-systemd-alternativa.png](cloud-aws/ec2/servicios-systemd-alternativa.png) | cloud-aws/ec2 | Otro encuadre systemd; se conserva aunque similar |
| `ScannmapAWS.PNG` | [cloud-aws/ssh/nmap-ssh-publico.png](cloud-aws/ssh/nmap-ssh-publico.png) | cloud-aws/ssh | Nmap muestra SSH abierto |
| `AWSREDHAD.PNG` | [cloud-aws/ssh/conectividad-tcp.png](cloud-aws/ssh/conectividad-tcp.png) | cloud-aws/ssh | Test-NetConnection exitoso; datos ya parcialmente ocultos |
| `autheAWSscan.PNG` | [cloud-aws/ssh/configuracion-autenticacion.png](cloud-aws/ssh/configuracion-autenticacion.png) | cloud-aws/ssh | Configuración efectiva de sshd |
| `conection AWS.PNG` | [cloud-aws/ssh/sesion-administrativa.png](cloud-aws/ssh/sesion-administrativa.png) | cloud-aws/ssh | Inicio de sesión SSH del laboratorio |
| `protoclos aws.PNG` | [cloud-aws/ssh/configuracion-sesion.png](cloud-aws/ssh/configuracion-sesion.png) | cloud-aws/ssh | sshd y sesión existente |
| `readteam.PNG` | [cloud-aws/ssh/intento-usuario-inexistente.png](cloud-aws/ssh/intento-usuario-inexistente.png) | cloud-aws/ssh | Permission denied para usuario ficticio |
| `user sacalado.PNG` | [cloud-aws/ssh/permisos-clave-publica.png](cloud-aws/ssh/permisos-clave-publica.png) | cloud-aws/ssh | Permisos y clave pública parcialmente ocultada; no prueba escalada |
| `aws token parch.PNG` | [cloud-aws/imdsv2/validacion-http401.png](cloud-aws/imdsv2/validacion-http401.png) | cloud-aws/imdsv2 | Consulta de metadata sin token devuelve HTTP 401 |
| `cosult.PNG` | [cloud-aws/imdsv2/consulta-ip-metadata.png](cloud-aws/imdsv2/consulta-ip-metadata.png) | cloud-aws/imdsv2 | Consulta de metadata de IP pública |
| `AWSCAN.PNG` | [cloud-aws/monitoring/historial-sesiones.png](cloud-aws/monitoring/historial-sesiones.png) | cloud-aws/monitoring | Historial de sesiones del sistema |
| `blue team.PNG` | [cloud-aws/monitoring/logs-ssh-fail2ban.png](cloud-aws/monitoring/logs-ssh-fail2ban.png) | cloud-aws/monitoring | Logs SSH y contadores Fail2Ban |
| `capcha.PNG` | [cloud-aws/monitoring/consulta-logs-autenticacion.png](cloud-aws/monitoring/consulta-logs-autenticacion.png) | cloud-aws/monitoring | Consulta de auth.log; no es CAPTCHA |
| `devsecops escan to id.PNG` | [cloud-aws/monitoring/revision-usuario-privilegios.png](cloud-aws/monitoring/revision-usuario-privilegios.png) | cloud-aws/monitoring | Identidad, grupos y estado de cuenta de laboratorio |
| `fail2ban.PNG` | [cloud-aws/monitoring/estado-fail2ban.png](cloud-aws/monitoring/estado-fail2ban.png) | cloud-aws/monitoring | Jail sshd y contadores sin bloqueos |
| `log to AWS user.PNG` | [cloud-aws/monitoring/revision-sudo-permisos.png](cloud-aws/monitoring/revision-sudo-permisos.png) | cloud-aws/monitoring | Comprobaciones de privilegios y permisos |
| `AWS1.PNG` | [cloud-aws/services/bedrock-consola.png](cloud-aws/services/bedrock-consola.png) | cloud-aws/services | Consola de Amazon Bedrock |
| `aws2.PNG` | [cloud-aws/services/lambda-consola.png](cloud-aws/services/lambda-consola.png) | cloud-aws/services | Consola de AWS Lambda |
| `consult AWS AURORA DATABASE.PNG` | [cloud-aws/services/aurora-actividades.png](cloud-aws/services/aurora-actividades.png) | cloud-aws/services | Consulta Aurora y actividades Explore AWS |
| `complete basics.PNG` | [cloud-aws/services/actividades-completadas.png](cloud-aws/services/actividades-completadas.png) | cloud-aws/services | Actividades Explore AWS; no es certificación |
| `complete.PNG` | [osint/tryhackme-dorking.png](osint/tryhackme-dorking.png) | osint | Pantalla de finalización del módulo Google Dorking |
| `installl apk.PNG` | [mobile-appsec/apk/preparacion-eas.png](mobile-appsec/apk/preparacion-eas.png) | mobile-appsec/apk | Instalación y autenticación EAS; no prueba APK corregido |
| `appfianlInstal.PNG` | [mobile-appsec/apk/configuracion-build-eas.png](mobile-appsec/apk/configuracion-build-eas.png) | mobile-appsec/apk | Configuración EAS y comienzo de build; no confirma parche |
| `maop app.PNG` | [mobile-appsec/mobsf/arranque-anonimizado.png](mobile-appsec/mobsf/arranque-anonimizado.png) | mobile-appsec/mobsf | Arranque MobSF; tres bandas opacas sobre credenciales |
| `mof.PNG` | [mobile-appsec/mobsf/interfaz-carga.png](mobile-appsec/mobsf/interfaz-carga.png) | mobile-appsec/mobsf | Pantalla Upload and Analyze de MobSF |
| `mofsf interface.PNG` | [mobile-appsec/mobsf/resultado-score52.png](mobile-appsec/mobsf/resultado-score52.png) | mobile-appsec/mobsf | Resultado SAST con score 52/100 |
| `firstsbluetam.PNG` | [mobile-appsec/mobsf/analisis-red-certificado.png](mobile-appsec/mobsf/analisis-red-certificado.png) | mobile-appsec/mobsf | Secciones de análisis; no prueba remediación |
| `redhad.PNG` | [mobile-appsec/mobsf/registro-analisis.png](mobile-appsec/mobsf/registro-analisis.png) | mobile-appsec/mobsf | Log de análisis APK; no es evidencia Red Hat |
| `Gemini_Generated_Image_23vq8s23vq8s23vq.jfif` | [diagrams/ilustracion-asm.jfif](diagrams/ilustracion-asm.jfif) | diagrams | Ilustración conceptual generada; no constituye evidencia técnica |
