# Nivel 1: Tipos y Clasificación de Seguridad

## Manual de Seguridad Informática para Debian 13 "Trixie"

---

## Introducción

Este documento constituye el primer nivel del manual de seguridad informática orientado a sistemas Debian 13 "Trixie". Su objetivo es proporcionar los fundamentos teóricos y conceptuales necesarios para comprender cómo se estructura, clasifica y gestiona la seguridad en entornos informáticos.

> **Nota para principiantes:** A lo largo de este documento, cada término técnico será definido la primera vez que aparezca, permitiendo una comprensión progresiva de los conceptos.

---

## 2.1. Tipos de Seguridad

La seguridad informática se divide en cuatro categorías fundamentales que trabajan de manera complementaria para proteger los activos de una organización.

### 2.1.1. Seguridad Física

**Definición:** La **seguridad física** comprende todas las medidas destinadas a proteger el hardware (equipos físicos), las instalaciones y el entorno donde se encuentran los sistemas informáticos contra amenazas tangibles como robos, desastres naturales o accesos no autorizados.

#### Elementos de protección física en Debian 13:

| Elemento | Descripción | Ejemplo en Debian |
|----------|-------------|-------------------|
| Control de acceso | Restricción de entrada a salas de servidores | Cerraduras, tarjetas de acceso |
| Protección ambiental | Resguardo contra factores ambientales | Sistemas de refrigeración, detectores de humo |
| Redundancia de hardware | Duplicación de componentes críticos | Discos en RAID, fuentes de alimentación redundantes |
| Respaldo energético | Continuidad eléctrica | UPS (Sistema de Alimentación Ininterrumpida) |

#### Configuración de ejemplo - Monitoreo de temperatura en Debian:

```bash
# Instalar herramientas de monitoreo de hardware
sudo apt install lm-sensors

# Detectar sensores disponibles
sudo sensors-detect

# Visualizar temperaturas del sistema
sensors
```

### 2.1.2. Seguridad Lógica

**Definición:** La **seguridad lógica** engloba los mecanismos de software y configuración que protegen los datos, aplicaciones y sistemas operativos contra accesos no autorizados, malware (software malicioso) y otras amenazas digitales.

#### Componentes principales en Debian 13:

1. **Autenticación:** Proceso de verificar la identidad de un usuario o sistema.
   ```bash
   # Configurar política de contraseñas en Debian
   sudo apt install libpam-pwquality
   sudo nano /etc/security/pwquality.conf
   ```

2. **Autorización:** Determinar qué acciones puede realizar un usuario autenticado.
   ```bash
   # Gestión de permisos en archivos
   chmod 750 /ruta/archivo    # rwxr-x---
   chown usuario:grupo /ruta/archivo
   ```

3. **Cifrado:** Proceso de convertir información legible en código ilegible para protegerla.
   ```bash
   # Cifrar partición con LUKS (Linux Unified Key Setup)
   sudo cryptsetup luksFormat /dev/sdX
   ```

4. **Firewall:** Sistema que filtra el tráfico de red según reglas predefinidas.
   ```bash
   # Configurar nftables (firewall por defecto en Debian 13)
   sudo apt install nftables
   sudo systemctl enable nftables
   ```

### 2.1.3. Seguridad Organizativa

**Definición:** La **seguridad organizativa** abarca las políticas, procedimientos, normas y estructuras que una organización implementa para gestionar la seguridad de manera sistemática.

#### Elementos clave:

| Componente | Descripción |
|------------|-------------|
| **Políticas de seguridad** | Documentos que establecen las directrices generales de seguridad |
| **Procedimientos operativos** | Instrucciones detalladas para ejecutar tareas de seguridad |
| **Gestión de riesgos** | Proceso de identificar, analizar y mitigar amenazas |
| **Plan de continuidad** | Estrategia para mantener operaciones durante incidentes |
| **Auditorías** | Revisiones periódicas del cumplimiento de políticas |

#### Ejemplo de política de contraseñas para Debian:

```
POLÍTICA DE CONTRASEÑAS - Versión 1.0

1. Longitud mínima: 12 caracteres
2. Complejidad: mayúsculas, minúsculas, números y símbolos
3. Vigencia máxima: 90 días
4. Historial: no reutilizar las últimas 5 contraseñas
5. Bloqueo: después de 5 intentos fallidos
```

### 2.1.4. Seguridad Personal

**Definición:** La **seguridad personal** (o seguridad del personal) se refiere a las medidas relacionadas con el factor humano: formación, concienciación, verificación de antecedentes y gestión del ciclo de vida de los empleados en relación con la seguridad.

#### Aspectos fundamentales:

- **Concienciación:** Programas de formación sobre amenazas como el **phishing** (técnica de engaño para obtener información confidencial).
- **Principio de mínimo privilegio:** Otorgar solo los permisos estrictamente necesarios.
- **Segregación de funciones:** Dividir tareas críticas entre múltiples personas.
- **Gestión de bajas:** Procedimientos para revocar accesos al cesar la relación laboral.

#### Implementación en Debian - Gestión de usuarios:

```bash
# Crear usuario con privilegios limitados
sudo adduser --disabled-login --gecos "Usuario Temporal" usuario_temp

# Asignar a grupo específico
sudo usermod -aG grupo_trabajo usuario_temp

# Establecer fecha de expiración de cuenta
sudo chage -E 2026-12-31 usuario_temp

# Verificar configuración de cuenta
sudo chage -l usuario_temp
```

---

## 2.2. Modelos Multinivel

Los modelos multinivel proporcionan marcos de referencia para evaluar y estructurar la seguridad de sistemas informáticos.

### 2.2.1. TCSEC (Trusted Computer System Evaluation Criteria)

**Definición:** El **TCSEC** (Criterios de Evaluación de Sistemas Informáticos de Confianza), también conocido como **Libro Naranja** (Orange Book), es un estándar del Departamento de Defensa de Estados Unidos publicado en 1983 que define criterios para evaluar la seguridad de sistemas informáticos.

#### Niveles de seguridad TCSEC:

| División | Nivel | Nombre | Descripción |
|----------|-------|--------|-------------|
| **D** | D | Protección Mínima | Sin seguridad; sistemas que no cumplen requisitos superiores |
| **C** | C1 | Protección Discrecional | Control de acceso básico por usuarios |
| **C** | C2 | Protección de Acceso Controlado | Auditoría de accesos; aislamiento de recursos |
| **B** | B1 | Protección de Seguridad Etiquetada | Etiquetas de sensibilidad en objetos; MAC básico |
| **B** | B2 | Protección Estructurada | Modelo formal de política; análisis de canales encubiertos |
| **B** | B3 | Dominios de Seguridad | Monitor de referencia; recuperación segura |
| **A** | A1 | Diseño Verificado | Verificación formal matemática del diseño |

> **Glosario:**
> - **MAC (Mandatory Access Control):** Control de acceso obligatorio donde el sistema impone las restricciones, no los usuarios.
> - **Canales encubiertos:** Métodos no previstos para transmitir información eludiendo controles de seguridad.
> - **Monitor de referencia:** Componente que media todos los accesos a objetos del sistema.

#### Relevancia para Debian 13:

Aunque TCSEC fue reemplazado por Common Criteria (ISO/IEC 15408), sus conceptos siguen siendo fundamentales:

```bash
# Debian implementa DAC (Control de Acceso Discrecional) por defecto
ls -la /etc/passwd  # Visualizar permisos (nivel C1)

# Para MAC, Debian soporta SELinux y AppArmor (nivel B1)
sudo apt install apparmor apparmor-utils
sudo aa-status  # Estado de AppArmor
```

### 2.2.2. Modelo OSI (Open Systems Interconnection)

**Definición:** El **modelo OSI** (Interconexión de Sistemas Abiertos) es un marco conceptual creado por la ISO (Organización Internacional de Normalización) que divide las comunicaciones de red en siete capas, cada una con funciones específicas.

#### Las 7 Capas del Modelo OSI:

| Capa | Nombre | Función | Amenazas | Protección en Debian |
|------|--------|---------|----------|----------------------|
| **7** | Aplicación | Interfaz con el usuario y aplicaciones | Malware, inyección SQL, XSS | WAF, actualizaciones de software |
| **6** | Presentación | Formato y cifrado de datos | Ataques a cifrado débil | TLS/SSL correctamente configurado |
| **5** | Sesión | Gestión de conexiones | Secuestro de sesión | Tokens seguros, timeouts |
| **4** | Transporte | Entrega confiable de datos (TCP/UDP) | SYN flood, escaneo de puertos | nftables, limitación de conexiones |
| **3** | Red | Enrutamiento de paquetes (IP) | IP spoofing, ataques ICMP | Filtrado de paquetes, VPN |
| **2** | Enlace de datos | Tramas y direcciones MAC | ARP spoofing, MAC flooding | 802.1X, segmentación VLAN |
| **1** | Física | Transmisión de bits | Interceptación física, jamming | Seguridad física, blindaje |

> **Glosario de términos:**
> - **SQL Injection:** Técnica que inserta código SQL malicioso en consultas de bases de datos.
> - **XSS (Cross-Site Scripting):** Ataque que inyecta scripts maliciosos en páginas web.
> - **SYN flood:** Ataque de denegación de servicio que satura con peticiones de conexión.
> - **IP spoofing:** Falsificación de la dirección IP de origen.
> - **ARP spoofing:** Ataque que asocia la MAC del atacante con la IP de otro dispositivo.

#### Protección por capas en Debian 13:

```bash
# Capa 7 - Aplicación: Actualizar software
sudo apt update && sudo apt upgrade

# Capa 4 - Transporte: Configurar firewall nftables
sudo nft add rule inet filter input tcp dport 22 accept
sudo nft add rule inet filter input tcp dport 80 accept
sudo nft add rule inet filter input drop

# Capa 3 - Red: Deshabilitar respuestas ICMP redirect
echo "net.ipv4.conf.all.accept_redirects = 0" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Capa 2 - Enlace: Verificar interfaces de red
ip link show
```

---

## 2.3. Clasificación de Información

La clasificación de información es el proceso de categorizar datos según su sensibilidad y el impacto que tendría su divulgación no autorizada.

### 2.3.1. Niveles de Clasificación

#### Esquema de cuatro niveles:

| Nivel | Etiqueta | Descripción | Ejemplos | Controles en Debian |
|-------|----------|-------------|----------|---------------------|
| **1** | **Público** | Información de libre acceso | Sitio web corporativo, folletos | Permisos 644, acceso anónimo permitido |
| **2** | **Interno** | Solo para personal interno | Procedimientos operativos, organigramas | Permisos 640, autenticación requerida |
| **3** | **Confidencial** | Acceso limitado por necesidad | Datos financieros, contratos | Permisos 600, cifrado en reposo |
| **4** | **Restringido** | Máxima protección | Claves criptográficas, datos personales sensibles | Permisos 400, cifrado + auditoría |

### 2.3.2. Implementación de clasificación en Debian 13

#### Estructura de directorios por clasificación:

```bash
# Crear estructura de directorios clasificados
sudo mkdir -p /datos/{publico,interno,confidencial,restringido}

# Crear grupos para cada nivel
sudo groupadd nivel_interno
sudo groupadd nivel_confidencial
sudo groupadd nivel_restringido

# Asignar permisos por nivel
sudo chmod 755 /datos/publico        # Lectura para todos
sudo chmod 750 /datos/interno        # Lectura para grupo
sudo chmod 700 /datos/confidencial   # Solo propietario
sudo chmod 700 /datos/restringido    # Solo propietario

# Asignar grupos
sudo chgrp nivel_interno /datos/interno
sudo chgrp nivel_confidencial /datos/confidencial
sudo chgrp nivel_restringido /datos/restringido
```

#### Etiquetado con atributos extendidos:

```bash
# Instalar herramientas de atributos extendidos
sudo apt install attr

# Etiquetar archivos con clasificación
sudo setfattr -n user.clasificacion -v "CONFIDENCIAL" /datos/confidencial/documento.pdf

# Verificar etiqueta
getfattr -n user.clasificacion /datos/confidencial/documento.pdf
```

### 2.3.3. Matriz de Controles por Clasificación

| Control | Público | Interno | Confidencial | Restringido |
|---------|---------|---------|--------------|-------------|
| Autenticación | No | Sí | Sí + MFA | Sí + MFA |
| Cifrado en tránsito | Opcional | Recomendado | Obligatorio | Obligatorio |
| Cifrado en reposo | No | No | Recomendado | Obligatorio |
| Registro de accesos | No | Básico | Detallado | Completo |
| Respaldo | Semanal | Diario | Diario cifrado | Tiempo real cifrado |
| Retención | 1 año | 3 años | 5 años | 7 años |

> **MFA (Multi-Factor Authentication):** Autenticación que requiere dos o más factores de verificación (algo que sabes, algo que tienes, algo que eres).

---

## 2.4. Controles de Seguridad

Los controles de seguridad son salvaguardas o contramedidas implementadas para proteger la confidencialidad, integridad y disponibilidad de la información.

### 2.4.1. Controles Preventivos

**Definición:** Los **controles preventivos** son medidas diseñadas para evitar que ocurran incidentes de seguridad antes de que sucedan.

#### Ejemplos en Debian 13:

| Control | Descripción | Implementación |
|---------|-------------|----------------|
| **Firewall** | Bloquea tráfico no autorizado | nftables, ufw |
| **Cifrado de disco** | Protege datos si el equipo es robado | LUKS |
| **Política de contraseñas** | Previene contraseñas débiles | PAM + pwquality |
| **Actualizaciones automáticas** | Corrige vulnerabilidades conocidas | unattended-upgrades |
| **Hardening del sistema** | Reduce superficie de ataque | CIS Benchmarks |

#### Configuración de controles preventivos:

```bash
# 1. Firewall con UFW (Uncomplicated Firewall)
sudo apt install ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable

# 2. Actualizaciones automáticas de seguridad
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# 3. Política de contraseñas robusta
sudo nano /etc/security/pwquality.conf
# Contenido recomendado:
# minlen = 12
# dcredit = -1
# ucredit = -1
# lcredit = -1
# ocredit = -1

# 4. Deshabilitar servicios innecesarios
sudo systemctl disable bluetooth.service
sudo systemctl disable cups.service
```

### 2.4.2. Controles Detectivos

**Definición:** Los **controles detectivos** son mecanismos que identifican y alertan sobre incidentes de seguridad mientras ocurren o poco después.

#### Ejemplos en Debian 13:

| Control | Descripción | Herramienta |
|---------|-------------|-------------|
| **IDS/IPS** | Detecta intrusiones en red | Suricata, Snort |
| **Análisis de logs** | Identifica patrones sospechosos | rsyslog, journalctl |
| **Monitoreo de integridad** | Detecta cambios no autorizados | AIDE, Tripwire |
| **Auditoría del sistema** | Registra eventos de seguridad | auditd |
| **Escaneo de vulnerabilidades** | Identifica debilidades | OpenVAS, Lynis |

> **IDS (Intrusion Detection System):** Sistema que monitorea el tráfico de red buscando actividades sospechosas.
> **IPS (Intrusion Prevention System):** IDS con capacidad de bloquear amenazas automáticamente.

#### Configuración de controles detectivos:

```bash
# 1. Sistema de auditoría auditd
sudo apt install auditd audispd-plugins
sudo systemctl enable auditd

# Regla: Monitorear cambios en /etc/passwd
sudo auditctl -w /etc/passwd -p wa -k passwd_changes

# Verificar logs de auditoría
sudo ausearch -k passwd_changes

# 2. Monitoreo de integridad con AIDE
sudo apt install aide
sudo aideinit
sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# Verificar integridad
sudo aide --check

# 3. Análisis de logs con journalctl
# Ver intentos de autenticación fallidos
sudo journalctl -u ssh --since "1 hour ago" | grep "Failed"

# 4. Escaneo de seguridad con Lynis
sudo apt install lynis
sudo lynis audit system
```

### 2.4.3. Controles Correctivos

**Definición:** Los **controles correctivos** son acciones que se ejecutan después de un incidente para restaurar sistemas, minimizar daños y prevenir recurrencias.

#### Ejemplos en Debian 13:

| Control | Descripción | Implementación |
|---------|-------------|----------------|
| **Respaldos** | Restauración de datos perdidos | rsync, Bacula, BorgBackup |
| **Plan de recuperación** | Procedimientos post-incidente | Documentación + scripts |
| **Parches de emergencia** | Corrección urgente de vulnerabilidades | apt upgrade específico |
| **Aislamiento de red** | Contención de amenazas | nftables, desconexión |
| **Forense digital** | Análisis post-incidente | Sleuth Kit, Autopsy |

#### Configuración de controles correctivos:

```bash
# 1. Sistema de respaldos con BorgBackup
sudo apt install borgbackup

# Inicializar repositorio de respaldos
borg init --encryption=repokey /ruta/respaldos

# Crear respaldo
borg create /ruta/respaldos::backup-{now} /datos/confidencial

# Restaurar respaldo
borg extract /ruta/respaldos::backup-2026-02-13

# 2. Script de aislamiento de emergencia
cat << 'EOF' | sudo tee /usr/local/bin/aislamiento_emergencia.sh
#!/bin/bash
# Script de aislamiento de red de emergencia
echo "ALERTA: Iniciando aislamiento de red..."
nft flush ruleset
nft add table inet emergency
nft add chain inet emergency input { type filter hook input priority 0 \; policy drop \; }
nft add chain inet emergency output { type filter hook output priority 0 \; policy drop \; }
nft add rule inet emergency input iif lo accept
nft add rule inet emergency output oif lo accept
echo "Sistema aislado. Solo conexiones locales permitidas."
EOF
sudo chmod 700 /usr/local/bin/aislamiento_emergencia.sh

# 3. Procedimiento de parche de emergencia
sudo apt update
sudo apt install --only-upgrade paquete_vulnerable
sudo systemctl restart servicio_afectado
```

### 2.4.4. Comparativa de Controles

| Aspecto | Preventivo | Detectivo | Correctivo |
|---------|------------|-----------|------------|
| **Momento** | Antes del incidente | Durante/después | Después del incidente |
| **Objetivo** | Evitar amenazas | Identificar amenazas | Recuperarse de amenazas |
| **Costo** | Medio-Alto inicial | Medio continuo | Variable (según daño) |
| **Ejemplo físico** | Cerradura | Alarma | Seguro de robo |
| **Ejemplo lógico** | Firewall | IDS | Respaldo |

---

## 2.5. Marco Normativo

El marco normativo proporciona las directrices, estándares y mejores prácticas reconocidas internacionalmente para implementar seguridad informática.

### 2.5.1. ISO/IEC 27001

**Definición:** **ISO/IEC 27001** es un estándar internacional publicado por la Organización Internacional de Normalización (ISO) y la Comisión Electrotécnica Internacional (IEC) que especifica los requisitos para establecer, implementar, mantener y mejorar continuamente un Sistema de Gestión de Seguridad de la Información (SGSI).

#### Estructura de ISO 27001:2022

| Cláusula | Título | Descripción |
|----------|--------|-------------|
| 4 | Contexto de la organización | Entender la organización y sus necesidades |
| 5 | Liderazgo | Compromiso de la alta dirección |
| 6 | Planificación | Gestión de riesgos y oportunidades |
| 7 | Apoyo | Recursos, competencia, comunicación |
| 8 | Operación | Implementación de controles |
| 9 | Evaluación del desempeño | Monitoreo y auditorías internas |
| 10 | Mejora | Acciones correctivas y mejora continua |

#### Anexo A - Controles de Seguridad (93 controles en 4 temas):

| Tema | Controles | Ejemplos |
|------|-----------|----------|
| Organizativos | 37 | Políticas, roles, gestión de activos |
| Personas | 8 | Selección, formación, terminación |
| Físicos | 14 | Perímetros, equipos, servicios |
| Tecnológicos | 34 | Acceso, criptografía, redes |

#### Aplicación a Debian 13:

```bash
# Control A.8.9 - Gestión de la configuración
# Documentar configuración del sistema
sudo apt install debsums
debsums --all --changed  # Verificar integridad de paquetes

# Control A.8.15 - Registro de actividades
# Configurar logging centralizado
sudo apt install rsyslog
sudo systemctl enable rsyslog

# Control A.8.24 - Uso de criptografía
# Verificar soporte de cifrado
openssl version
cat /proc/crypto | grep -E "^name"
```

### 2.5.2. CIS Benchmarks para Debian

**Definición:** Los **CIS Benchmarks** (Puntos de Referencia del Centro para la Seguridad de Internet) son guías de configuración segura desarrolladas por consenso de expertos en seguridad. Proporcionan recomendaciones específicas y detalladas para fortificar sistemas operativos.

#### Niveles de CIS Benchmarks:

| Nivel | Descripción | Uso recomendado |
|-------|-------------|-----------------|
| **Nivel 1** | Configuraciones básicas de seguridad con mínimo impacto operativo | Todos los sistemas |
| **Nivel 2** | Configuraciones avanzadas que pueden afectar funcionalidad | Sistemas de alta seguridad |

#### Categorías del CIS Benchmark para Debian 12/13:

| Sección | Área | Ejemplos de controles |
|---------|------|----------------------|
| 1 | Configuración inicial | Particiones, actualizaciones, bootloader |
| 2 | Servicios | Deshabilitar servicios innecesarios |
| 3 | Configuración de red | Parámetros de kernel, firewall |
| 4 | Auditoría y logging | auditd, rsyslog, journald |
| 5 | Acceso y autenticación | SSH, PAM, sudo |
| 6 | Mantenimiento del sistema | Permisos de archivos, integridad |

#### Implementación de controles CIS en Debian 13:

```bash
# === SECCIÓN 1: Configuración Inicial ===

# 1.1.1 - Verificar partición separada para /tmp
mount | grep " /tmp "

# 1.4.1 - Proteger bootloader GRUB con contraseña
sudo grub-mkpasswd-pbkdf2
# Agregar hash a /etc/grub.d/40_custom

# === SECCIÓN 2: Servicios ===

# 2.1.1 - Deshabilitar servicios innecesarios
sudo systemctl --now disable avahi-daemon
sudo systemctl --now disable cups

# === SECCIÓN 3: Configuración de Red ===

# 3.1.1 - Deshabilitar IPv6 si no se usa
echo "net.ipv6.conf.all.disable_ipv6 = 1" | sudo tee -a /etc/sysctl.d/99-sysctl.conf
sudo sysctl -p /etc/sysctl.d/99-sysctl.conf

# 3.2.1 - Deshabilitar reenvío de paquetes
echo "net.ipv4.ip_forward = 0" | sudo tee -a /etc/sysctl.d/99-sysctl.conf

# === SECCIÓN 4: Auditoría ===

# 4.1.1 - Instalar y habilitar auditd
sudo apt install auditd
sudo systemctl enable auditd

# === SECCIÓN 5: Acceso y Autenticación ===

# 5.2.1 - Configurar SSH seguro
sudo nano /etc/ssh/sshd_config
# Configuraciones recomendadas:
# PermitRootLogin no
# MaxAuthTries 4
# ClientAliveInterval 300
# ClientAliveCountMax 0
# AllowUsers usuario_autorizado

# 5.3.1 - Configurar política de contraseñas
sudo apt install libpam-pwquality

# === SECCIÓN 6: Mantenimiento ===

# 6.1.1 - Verificar permisos de archivos críticos
sudo chmod 644 /etc/passwd
sudo chmod 600 /etc/shadow
sudo chmod 644 /etc/group
sudo chmod 600 /etc/gshadow
```

#### Herramientas de auditoría CIS:

```bash
# Lynis - Auditoría de seguridad open source
sudo apt install lynis
sudo lynis audit system --quick

# Ver resultados
sudo cat /var/log/lynis-report.dat | grep warning
sudo cat /var/log/lynis-report.dat | grep suggestion
```

### 2.5.3. Comparativa de Marcos Normativos

| Aspecto | ISO 27001 | CIS Benchmarks |
|---------|-----------|----------------|
| **Tipo** | Estándar internacional certificable | Guía técnica de mejores prácticas |
| **Enfoque** | Gestión de seguridad (qué hacer) | Configuración técnica (cómo hacerlo) |
| **Alcance** | Organización completa | Sistema operativo específico |
| **Actualización** | Cada 5-7 años | Continua (con cada versión de SO) |
| **Certificación** | Sí (auditoría externa) | No (autoevaluación) |
| **Costo** | Alto (certificación) | Gratuito |
| **Complementariedad** | Marco de gestión | Implementación técnica |

> **Recomendación:** ISO 27001 y CIS Benchmarks son complementarios. ISO 27001 define QUÉ controles implementar; CIS Benchmarks especifica CÓMO implementarlos técnicamente en Debian.

---

## Checklist Nivel 1: Tipos y Clasificación de Seguridad

Este checklist permite verificar la comprensión e implementación de los conceptos del Nivel 1. Marque cada elemento completado.

### Seguridad Física

- [ ] Verificar que el servidor/equipo está en ubicación segura con acceso restringido
- [ ] Comprobar existencia de sistema de alimentación ininterrumpida (UPS)
- [ ] Instalar sensores de temperatura: `sudo apt install lm-sensors && sensors-detect`
- [ ] Documentar ubicación física y controles de acceso al hardware
- [ ] Verificar redundancia de almacenamiento (RAID si aplica)

### Seguridad Lógica

- [ ] Configurar firewall nftables o UFW:
  ```bash
  sudo apt install ufw
  sudo ufw enable
  sudo ufw default deny incoming
  ```
- [ ] Habilitar cifrado de disco LUKS en particiones sensibles
- [ ] Configurar política de contraseñas robusta en `/etc/security/pwquality.conf`
- [ ] Instalar y configurar AppArmor:
  ```bash
  sudo apt install apparmor apparmor-utils
  sudo aa-status
  ```
- [ ] Deshabilitar inicio de sesión root por SSH

### Seguridad Organizativa

- [ ] Documentar política de seguridad de la información
- [ ] Crear procedimiento de gestión de incidentes
- [ ] Definir roles y responsabilidades de seguridad
- [ ] Establecer proceso de gestión de cambios
- [ ] Planificar auditorías de seguridad periódicas

### Seguridad Personal

- [ ] Implementar principio de mínimo privilegio en cuentas de usuario
- [ ] Crear usuarios con permisos específicos (no usar root):
  ```bash
  sudo adduser --disabled-password usuario_limitado
  ```
- [ ] Configurar expiración de cuentas temporales: `sudo chage -E YYYY-MM-DD usuario`
- [ ] Documentar procedimiento de baja de usuarios
- [ ] Planificar formación en concienciación de seguridad

### Clasificación de Información

- [ ] Crear estructura de directorios por nivel de clasificación:
  ```bash
  sudo mkdir -p /datos/{publico,interno,confidencial,restringido}
  ```
- [ ] Asignar permisos según clasificación (755/750/700/700)
- [ ] Crear grupos para cada nivel de clasificación
- [ ] Implementar etiquetado de archivos con atributos extendidos
- [ ] Documentar matriz de controles por nivel de clasificación

### Controles Preventivos

- [ ] Configurar actualizaciones automáticas de seguridad:
  ```bash
  sudo apt install unattended-upgrades
  sudo dpkg-reconfigure -plow unattended-upgrades
  ```
- [ ] Deshabilitar servicios innecesarios: `sudo systemctl disable servicio`
- [ ] Aplicar hardening básico según CIS Benchmarks Nivel 1
- [ ] Configurar banners de advertencia legal en `/etc/issue` y `/etc/issue.net`
- [ ] Verificar configuración segura de SSH

### Controles Detectivos

- [ ] Instalar y configurar auditd:
  ```bash
  sudo apt install auditd
  sudo systemctl enable auditd
  ```
- [ ] Configurar monitoreo de integridad con AIDE:
  ```bash
  sudo apt install aide
  sudo aideinit
  ```
- [ ] Configurar análisis de logs con journalctl
- [ ] Ejecutar escaneo de seguridad con Lynis: `sudo lynis audit system`
- [ ] Revisar logs de autenticación periódicamente

### Controles Correctivos

- [ ] Configurar sistema de respaldos automatizado:
  ```bash
  sudo apt install borgbackup
  ```
- [ ] Documentar procedimiento de restauración de respaldos
- [ ] Crear script de aislamiento de emergencia
- [ ] Documentar plan de respuesta a incidentes
- [ ] Probar restauración de respaldos periódicamente

### Marco Normativo

- [ ] Revisar requisitos aplicables de ISO 27001
- [ ] Descargar CIS Benchmark para Debian 12/13 desde cisecurity.org
- [ ] Ejecutar auditoría CIS con herramienta automatizada
- [ ] Documentar desviaciones justificadas de los benchmarks
- [ ] Planificar revisiones periódicas de cumplimiento

### Verificación Final del Nivel 1

```bash
# Script de verificación rápida del Nivel 1
echo "=== Verificación Nivel 1 - Debian 13 Trixie ==="

echo -e "\n[1] Estado del firewall:"
sudo ufw status || sudo nft list ruleset | head -10

echo -e "\n[2] Estado de AppArmor:"
sudo aa-status | head -5

echo -e "\n[3] Política de contraseñas:"
grep -E "^(minlen|dcredit|ucredit)" /etc/security/pwquality.conf 2>/dev/null || echo "No configurado"

echo -e "\n[4] Servicios en escucha:"
ss -tlnp | grep LISTEN

echo -e "\n[5] Usuarios con shell de login:"
grep -v "nologin\|false" /etc/passwd | cut -d: -f1

echo -e "\n[6] Estado de auditd:"
sudo systemctl is-active auditd

echo -e "\n[7] Última actualización del sistema:"
stat /var/cache/apt/pkgcache.bin | grep Modify

echo -e "\n=== Fin de verificación ==="
```

---

## Resumen del Nivel 1

Este nivel ha cubierto los fundamentos conceptuales de la seguridad informática aplicados a Debian 13 "Trixie":

| Tema | Conceptos Clave |
|------|-----------------|
| **Tipos de seguridad** | Física, lógica, organizativa, personal |
| **Modelos multinivel** | TCSEC (D a A1), OSI (7 capas) |
| **Clasificación** | Público, interno, confidencial, restringido |
| **Controles** | Preventivos, detectivos, correctivos |
| **Marco normativo** | ISO 27001 (gestión), CIS Benchmarks (técnico) |

### Próximos pasos

Con los fundamentos del Nivel 1 comprendidos, el siguiente nivel abordará la **implementación práctica de controles de acceso y autenticación** en Debian 13, incluyendo:

- Configuración avanzada de PAM
- Gestión de usuarios y grupos
- Implementación de sudo y políticas de privilegios
- Autenticación multifactor (MFA)

---

## Glosario Completo

| Término | Definición |
|---------|------------|
| **AppArmor** | Sistema de control de acceso obligatorio (MAC) para Linux |
| **ARP spoofing** | Ataque que asocia la MAC del atacante con la IP de otro dispositivo |
| **Auditoría** | Revisión sistemática del cumplimiento de políticas y controles |
| **Autenticación** | Proceso de verificar la identidad de un usuario o sistema |
| **Autorización** | Determinar qué acciones puede realizar un usuario autenticado |
| **Benchmark** | Punto de referencia o estándar de comparación |
| **Canal encubierto** | Método no previsto para transmitir información eludiendo controles |
| **Cifrado** | Proceso de convertir información legible en código ilegible |
| **CIS** | Center for Internet Security (Centro para la Seguridad de Internet) |
| **Control correctivo** | Acción que restaura sistemas después de un incidente |
| **Control detectivo** | Mecanismo que identifica incidentes de seguridad |
| **Control preventivo** | Medida que evita incidentes antes de que ocurran |
| **DAC** | Control de Acceso Discrecional (permisos gestionados por usuarios) |
| **Firewall** | Sistema que filtra el tráfico de red según reglas predefinidas |
| **Hardening** | Proceso de fortificar un sistema reduciendo su superficie de ataque |
| **IDS** | Sistema de Detección de Intrusiones |
| **IPS** | Sistema de Prevención de Intrusiones |
| **ISO** | Organización Internacional de Normalización |
| **LUKS** | Estándar de cifrado de disco en Linux |
| **MAC** | Control de Acceso Obligatorio (permisos impuestos por el sistema) |
| **Malware** | Software malicioso (virus, ransomware, troyanos, etc.) |
| **MFA** | Autenticación Multifactor |
| **Monitor de referencia** | Componente que media todos los accesos a objetos del sistema |
| **OSI** | Modelo de Interconexión de Sistemas Abiertos |
| **PAM** | Módulos de Autenticación Conectables |
| **Phishing** | Técnica de engaño para obtener información confidencial |
| **RAID** | Conjunto Redundante de Discos Independientes |
| **SGSI** | Sistema de Gestión de Seguridad de la Información |
| **SQL Injection** | Técnica que inserta código SQL malicioso |
| **SYN flood** | Ataque de denegación de servicio con peticiones de conexión |
| **TCSEC** | Criterios de Evaluación de Sistemas Informáticos de Confianza |
| **UPS** | Sistema de Alimentación Ininterrumpida |
| **XSS** | Cross-Site Scripting (inyección de scripts maliciosos) |

---

**Documento:** Manual de Seguridad Informática para Debian 13 "Trixie"
**Nivel:** 1 - Tipos y Clasificación de Seguridad
**Versión:** 1.0
**Fecha:** Febrero 2026
**Autor:** MiniMax Agent
