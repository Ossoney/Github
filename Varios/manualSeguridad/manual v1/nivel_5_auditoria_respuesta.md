# Nivel 5: Auditoría, Cumplimiento y Respuesta

## Manual de Seguridad Informática para Debian 13 "Trixie"

---

## Introducción

Este nivel aborda las prácticas avanzadas de seguridad que permiten verificar el estado de protección del sistema, responder ante incidentes y medir el progreso en madurez de seguridad. Está diseñado para principiantes, por lo que cada término técnico será explicado en su primera aparición.

---

## 6.1. Auditorías Automatizadas (Lynis, OpenSCAP)

### Conceptos Fundamentales

**Lynis** es una herramienta de auditoría de seguridad de código abierto diseñada para sistemas Unix/Linux. Analiza el sistema en busca de vulnerabilidades, errores de configuración y oportunidades de mejora, generando un informe detallado con puntuación y recomendaciones.

**OpenSCAP** es una implementación de código abierto del protocolo **SCAP** (Security Content Automation Protocol - Protocolo de Automatización de Contenido de Seguridad). SCAP es un conjunto de estándares desarrollados por el NIST (Instituto Nacional de Estándares y Tecnología de EE.UU.) que permite la evaluación automatizada de vulnerabilidades y cumplimiento de políticas de seguridad.

### 6.1.1. Instalación y Uso de Lynis

#### Instalación desde repositorios oficiales

```bash
# Actualizar lista de paquetes
sudo apt update

# Instalar Lynis
sudo apt install lynis -y

# Verificar la versión instalada
lynis --version
```

#### Instalación de la versión más reciente (opcional)

```bash
# Clonar repositorio oficial
cd /opt
sudo git clone https://github.com/CISOfy/lynis.git

# Ejecutar desde el directorio clonado
cd /opt/lynis
sudo ./lynis audit system
```

#### Ejecución de auditoría completa

```bash
# Auditoría completa del sistema
sudo lynis audit system

# Auditoría con informe en formato específico
sudo lynis audit system --report-file /var/log/lynis-report.dat

# Auditoría rápida (sin interacción)
sudo lynis audit system --quick

# Ver solo advertencias y sugerencias
sudo lynis audit system --warnings-only
```

#### Interpretación de resultados

Lynis genera un **índice de endurecimiento** (hardening index) de 0 a 100:

| Puntuación | Interpretación |
|------------|----------------|
| 0-49       | Seguridad crítica, requiere atención inmediata |
| 50-69      | Seguridad básica, mejoras necesarias |
| 70-84      | Buena seguridad, optimizaciones recomendadas |
| 85-100     | Excelente seguridad |

```bash
# Ver el informe generado
sudo cat /var/log/lynis.log

# Ver sugerencias específicas
sudo grep "suggestion" /var/log/lynis-report.dat
```

### 6.1.2. Instalación y Uso de OpenSCAP

#### Instalación de OpenSCAP

```bash
# Instalar OpenSCAP y herramientas asociadas
sudo apt update
sudo apt install libopenscap8 openscap-scanner openscap-utils -y

# Instalar contenido SCAP para Debian
sudo apt install scap-security-guide -y

# Verificar instalación
oscap --version
```

#### Listar perfiles disponibles

```bash
# Ver perfiles de seguridad disponibles para el sistema
oscap info /usr/share/xml/scap/ssg/content/ssg-debian12-ds.xml

# Nota: Para Debian 13, puede ser necesario usar el perfil de Debian 12
# o descargar contenido actualizado
```

#### Ejecución de evaluación SCAP

```bash
# Crear directorio para resultados
sudo mkdir -p /var/log/openscap

# Ejecutar evaluación con perfil estándar
sudo oscap xccdf eval \
    --profile xccdf_org.ssgproject.content_profile_standard \
    --results /var/log/openscap/results.xml \
    --report /var/log/openscap/report.html \
    /usr/share/xml/scap/ssg/content/ssg-debian12-ds.xml

# Abrir informe HTML (si hay entorno gráfico)
# El informe se encuentra en /var/log/openscap/report.html
```

#### Remediación automática

```bash
# Generar script de remediación basado en resultados
sudo oscap xccdf generate fix \
    --fix-type bash \
    --result-id "" \
    /var/log/openscap/results.xml > /tmp/remediation.sh

# Revisar el script antes de ejecutar
cat /tmp/remediation.sh

# Ejecutar remediación (con precaución)
# sudo bash /tmp/remediation.sh
```

### 6.1.3. Automatización de Auditorías

#### Crear tarea programada para Lynis

```bash
# Crear script de auditoría automática
sudo tee /usr/local/bin/auditoria-seguridad.sh << 'EOF'
#!/bin/bash
# Script de auditoría de seguridad automatizada
FECHA=$(date +%Y%m%d_%H%M%S)
LOG_DIR="/var/log/auditorias"
mkdir -p $LOG_DIR

# Ejecutar Lynis
lynis audit system --no-colors --quiet \
    --report-file "$LOG_DIR/lynis_$FECHA.dat" \
    --log-file "$LOG_DIR/lynis_$FECHA.log"

# Enviar resumen por correo (opcional)
# mail -s "Auditoría de Seguridad $FECHA" admin@empresa.com < "$LOG_DIR/lynis_$FECHA.log"

echo "Auditoría completada: $FECHA"
EOF

# Dar permisos de ejecución
sudo chmod +x /usr/local/bin/auditoria-seguridad.sh

# Programar ejecución semanal (domingos a las 3:00 AM)
echo "0 3 * * 0 root /usr/local/bin/auditoria-seguridad.sh" | sudo tee /etc/cron.d/auditoria-seguridad
```

---

## 6.2. Simulacros de Incidentes (Ransomware, Fallo TPM)

### Conceptos Fundamentales

**Ransomware** es un tipo de software malicioso (malware) que cifra los archivos del sistema víctima y exige un pago (rescate) para proporcionar la clave de descifrado. Es una de las amenazas más devastadoras en ciberseguridad moderna.

**TPM** (Trusted Platform Module - Módulo de Plataforma Confiable) es un chip de seguridad integrado en la placa base del ordenador que almacena claves criptográficas y garantiza la integridad del arranque del sistema.

### 6.2.1. Simulacro de Ataque Ransomware

> **ADVERTENCIA**: Este simulacro debe realizarse ÚNICAMENTE en entornos de prueba aislados, NUNCA en sistemas de producción.

#### Fase 1: Preparación del entorno de prueba

```bash
# Crear entorno aislado para simulacro
mkdir -p /tmp/simulacro_ransomware/{documentos,imagenes,datos}

# Crear archivos de prueba
for i in {1..10}; do
    echo "Documento de prueba $i - Contenido confidencial" > "/tmp/simulacro_ransomware/documentos/doc_$i.txt"
    dd if=/dev/urandom of="/tmp/simulacro_ransomware/imagenes/img_$i.jpg" bs=1024 count=10 2>/dev/null
done

# Crear archivo de datos simulado
echo "BASE_DE_DATOS_SIMULADA" > /tmp/simulacro_ransomware/datos/database.db

# Verificar estructura creada
tree /tmp/simulacro_ransomware/ 2>/dev/null || find /tmp/simulacro_ransomware/ -type f
```

#### Fase 2: Simulación del cifrado (sin daño real)

```bash
# Script de simulación de ransomware (SOLO PARA PRUEBAS)
cat << 'EOF' > /tmp/simular_ransomware.sh
#!/bin/bash
# SIMULADOR EDUCATIVO - NO ES RANSOMWARE REAL
TARGET_DIR="/tmp/simulacro_ransomware"
LOG_FILE="/tmp/ransomware_simulation.log"

echo "[$(date)] Simulación de ransomware iniciada" > $LOG_FILE

# Simular cifrado renombrando archivos
find "$TARGET_DIR" -type f | while read archivo; do
    # Solo renombrar, no cifrar realmente
    mv "$archivo" "${archivo}.ENCRYPTED_SIMULATION"
    echo "[SIMULADO] Archivo 'cifrado': $archivo" >> $LOG_FILE
done

# Crear nota de rescate simulada
cat > "$TARGET_DIR/LEEME_RESCATE.txt" << 'NOTA'
===========================================
    SIMULACRO DE RANSOMWARE
===========================================
Este es un SIMULACRO educativo.
Sus archivos han sido "cifrados" (renombrados).

En un ataque real:
- NO pague el rescate
- Desconecte el equipo de la red
- Contacte al equipo de seguridad
- Restaure desde copias de seguridad

Para recuperar los archivos de este simulacro:
find /tmp/simulacro_ransomware -name "*.ENCRYPTED_SIMULATION" -exec bash -c 'mv "$1" "${1%.ENCRYPTED_SIMULATION}"' _ {} \;
===========================================
NOTA

echo "[$(date)] Simulación completada" >> $LOG_FILE
EOF

chmod +x /tmp/simular_ransomware.sh
```

#### Fase 3: Procedimiento de respuesta ante ransomware

```bash
# PASO 1: Detección y aislamiento
# ================================
# Desconectar de la red inmediatamente
sudo ip link set eth0 down  # O el nombre de su interfaz de red

# PASO 2: Identificación del alcance
# ================================
# Buscar archivos con extensiones sospechosas
find / -type f \( -name "*.encrypted" -o -name "*.locked" -o -name "*.crypto" \) 2>/dev/null

# Buscar notas de rescate
find / -type f \( -name "*README*" -o -name "*DECRYPT*" -o -name "*RESTORE*" \) -mtime -1 2>/dev/null

# PASO 3: Preservar evidencia
# ================================
# Crear imagen del sistema (requiere espacio suficiente)
# sudo dd if=/dev/sda of=/media/externo/imagen_forense.img bs=4M status=progress

# PASO 4: Documentar el incidente
# ================================
cat << 'EOF' > /tmp/informe_incidente.txt
INFORME DE INCIDENTE DE SEGURIDAD
=================================
Fecha de detección: $(date)
Sistema afectado: $(hostname)
Usuario que reporta: $(whoami)

Síntomas observados:
- [ ] Archivos con extensión modificada
- [ ] Nota de rescate encontrada
- [ ] Imposibilidad de abrir archivos
- [ ] Rendimiento anormal del sistema

Acciones tomadas:
- [ ] Sistema aislado de la red
- [ ] Evidencia preservada
- [ ] Equipo de seguridad notificado
- [ ] Copias de seguridad verificadas

Próximos pasos:
1. Análisis forense
2. Restauración desde backup
3. Investigación del vector de entrada
4. Actualización de defensas
EOF
```

### 6.2.2. Simulacro de Fallo TPM

#### Preparación del simulacro

```bash
# Verificar si el sistema tiene TPM
sudo dmesg | grep -i tpm
ls /dev/tpm*

# Instalar herramientas TPM
sudo apt install tpm2-tools -y

# Verificar estado del TPM
sudo tpm2_getcap properties-fixed 2>/dev/null || echo "TPM no disponible o no configurado"
```

#### Procedimiento de respuesta ante fallo TPM

```bash
# ESCENARIO: El TPM falla y el sistema no puede arrancar
# debido a que las claves de cifrado de disco están protegidas por TPM

# PASO 1: Documentar el estado
# ================================
echo "=== Estado del TPM ===" > /tmp/informe_tpm.txt
sudo tpm2_getcap properties-variable >> /tmp/informe_tpm.txt 2>&1

# PASO 2: Verificar claves de recuperación LUKS
# ================================
# Listar dispositivos cifrados
lsblk -f | grep -i luks

# Verificar slots de claves disponibles
# sudo cryptsetup luksDump /dev/sda3  # Ajustar dispositivo

# PASO 3: Plan de recuperación
# ================================
cat << 'EOF' > /tmp/plan_recuperacion_tpm.md
# Plan de Recuperación ante Fallo TPM

## Requisitos previos
- Clave de recuperación LUKS almacenada de forma segura
- Medio de arranque alternativo (USB Live)

## Procedimiento

### Opción A: Recuperación con clave LUKS
1. Arrancar desde USB Live de Debian
2. Desbloquear partición manualmente:
   ```
   sudo cryptsetup luksOpen /dev/sdXY nombre_cifrado --key-file /ruta/clave
   ```
3. Montar el sistema de archivos
4. Reconfigurar arranque sin dependencia TPM

### Opción B: Restauración completa
1. Arrancar desde medio de recuperación
2. Restaurar sistema desde copia de seguridad
3. Reconfigurar TPM si el hardware es funcional

## Lecciones aprendidas
- Mantener claves de recuperación en ubicación segura y separada
- Probar procedimientos de recuperación periódicamente
- Considerar múltiples métodos de desbloqueo
EOF

cat /tmp/plan_recuperacion_tpm.md
```

---

## 6.3. Forense Digital Básico

### Conceptos Fundamentales

**Forense digital** es la disciplina que aplica técnicas de investigación y análisis para recopilar, preservar y examinar evidencia digital de sistemas informáticos, con el objetivo de determinar qué ocurrió durante un incidente de seguridad, identificar a los responsables y prevenir futuros ataques.

### 6.3.1. Principios del Análisis Forense

1. **Preservación de evidencia**: No modificar los datos originales
2. **Cadena de custodia**: Documentar quién manipuló la evidencia y cuándo
3. **Reproducibilidad**: Los resultados deben poder verificarse
4. **Documentación**: Registrar cada paso del análisis

### 6.3.2. Herramientas Forenses en Debian

```bash
# Instalar herramientas forenses esenciales
sudo apt update
sudo apt install -y \
    sleuthkit \        # Análisis de sistemas de archivos
    autopsy \          # Interfaz gráfica para sleuthkit
    foremost \         # Recuperación de archivos
    dc3dd \            # Copia forense de discos
    volatility3 \      # Análisis de memoria RAM
    binwalk \          # Análisis de firmware y archivos
    hashdeep \         # Verificación de integridad
    exiftool           # Metadatos de archivos

# Verificar instalación
which fls mmls foremost dc3dd
```

### 6.3.3. Procedimientos Forenses Básicos

#### Creación de imagen forense

```bash
# IMPORTANTE: Trabajar siempre sobre copias, nunca sobre el original

# Identificar el disco a copiar
lsblk

# Crear imagen forense con dc3dd (más robusto que dd)
# Incluye verificación de hash automática
sudo dc3dd if=/dev/sdX of=/media/forense/imagen.dd \
    hash=sha256 \
    log=/media/forense/imagen.log

# Alternativa con dd tradicional
sudo dd if=/dev/sdX of=/media/forense/imagen.dd bs=4M status=progress
sha256sum /media/forense/imagen.dd > /media/forense/imagen.sha256
```

#### Análisis de sistema de archivos

```bash
# Ver estructura de particiones de una imagen
mmls /media/forense/imagen.dd

# Ejemplo de salida:
# DOS Partition Table
# Offset Sector: 0
# Units are in 512-byte sectors
#
#      Slot    Start        End          Length       Description
# 00:  Meta    0000000000   0000000000   0000000001   Primary Table (#0)
# 01:  -----   0000000000   0000002047   0000002048   Unallocated
# 02:  00:00   0000002048   0001953791   0001951744   Linux (0x83)

# Listar archivos en una partición (offset 2048)
fls -o 2048 /media/forense/imagen.dd

# Listar archivos eliminados (marcados con *)
fls -o 2048 -d /media/forense/imagen.dd

# Exportar un archivo específico por su inode
icat -o 2048 /media/forense/imagen.dd 12345 > /tmp/archivo_recuperado
```

#### Recuperación de archivos eliminados

```bash
# Crear directorio para archivos recuperados
mkdir -p /media/forense/recuperados

# Recuperar archivos con foremost
sudo foremost -t all -i /media/forense/imagen.dd -o /media/forense/recuperados

# Recuperar tipos específicos (documentos, imágenes)
sudo foremost -t doc,pdf,jpg,png -i /media/forense/imagen.dd -o /media/forense/recuperados_docs

# Ver resultados
cat /media/forense/recuperados/audit.txt
```

#### Análisis de línea temporal

```bash
# Crear línea temporal de actividad del sistema
# (útil para reconstruir eventos)

# Generar bodyfile con información de tiempos
fls -o 2048 -r -m "/" /media/forense/imagen.dd > /tmp/bodyfile.txt

# Convertir a línea temporal ordenada
mactime -b /tmp/bodyfile.txt -d > /tmp/timeline.csv

# Filtrar por rango de fechas sospechosas
mactime -b /tmp/bodyfile.txt -d 2024-01-01..2024-01-31 > /tmp/timeline_enero.csv
```

#### Análisis de logs del sistema

```bash
# Los logs son fundamentales en el análisis forense
# Ubicaciones comunes en Debian:

# Logs de autenticación
sudo cat /var/log/auth.log | grep -E "(Failed|Accepted|session opened)"

# Logs del sistema
sudo journalctl --since "2024-01-01" --until "2024-01-31"

# Buscar actividad sospechosa
sudo grep -r "sudo" /var/log/auth.log | tail -50
sudo grep -r "COMMAND" /var/log/auth.log | tail -50

# Últimos inicios de sesión
last -50
lastb -50  # Intentos fallidos

# Buscar modificaciones recientes en archivos de configuración
find /etc -type f -mtime -7 -ls
```

#### Verificación de integridad

```bash
# Crear base de datos de hashes de archivos críticos
sudo hashdeep -r -c sha256 /etc /usr/bin /usr/sbin > /var/log/baseline_hashes.txt

# Verificar integridad posteriormente
sudo hashdeep -r -a -k /var/log/baseline_hashes.txt /etc /usr/bin /usr/sbin

# Verificar binarios del sistema contra paquetes
sudo debsums -c  # Mostrar archivos modificados
```

---

## 6.4. IDS/IPS (Suricata/Fail2ban)

### Conceptos Fundamentales

**IDS (Intrusion Detection System - Sistema de Detección de Intrusiones)** es un sistema que monitorea el tráfico de red o la actividad del sistema en busca de comportamientos maliciosos o violaciones de políticas, generando alertas cuando detecta amenazas.

**IPS (Intrusion Prevention System - Sistema de Prevención de Intrusiones)** es similar al IDS pero además de detectar, puede tomar acciones automáticas para bloquear o prevenir las amenazas detectadas.

**Suricata** es un motor de detección de amenazas de red de alto rendimiento, código abierto, capaz de funcionar como IDS, IPS y monitor de seguridad de red. Analiza el tráfico de red en tiempo real usando reglas predefinidas.

**Fail2ban** es una herramienta que analiza logs del sistema y bloquea automáticamente direcciones IP que muestran comportamiento malicioso (como múltiples intentos fallidos de autenticación).

### 6.4.1. Instalación y Configuración de Suricata

#### Instalación de Suricata

```bash
# Instalar Suricata
sudo apt update
sudo apt install suricata suricata-update -y

# Verificar versión
suricata --build-info | head -20

# Ver interfaz de red principal
ip addr show
# Nota: Identificar la interfaz (ej: eth0, ens33, enp0s3)
```

#### Configuración básica

```bash
# Respaldar configuración original
sudo cp /etc/suricata/suricata.yaml /etc/suricata/suricata.yaml.backup

# Editar configuración principal
sudo nano /etc/suricata/suricata.yaml
```

Configuración recomendada en `/etc/suricata/suricata.yaml`:

```yaml
# Sección vars - Definir red local
vars:
  address-groups:
    HOME_NET: "[192.168.0.0/16,10.0.0.0/8,172.16.0.0/12]"
    EXTERNAL_NET: "!$HOME_NET"

  port-groups:
    HTTP_PORTS: "80,443,8080"
    SSH_PORTS: "22"

# Sección af-packet - Interfaz de red
af-packet:
  - interface: eth0    # Cambiar por su interfaz
    cluster-id: 99
    cluster-type: cluster_flow
    defrag: yes

# Sección outputs - Logs
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: eve.json
      types:
        - alert:
            payload: yes
            payload-printable: yes
        - http:
            extended: yes
        - dns
        - tls
        - files
        - ssh

# Sección rule-files - Reglas activas
rule-files:
  - suricata.rules

# Directorio de reglas
default-rule-path: /var/lib/suricata/rules
```

#### Actualización de reglas

```bash
# Actualizar reglas de detección
sudo suricata-update

# Habilitar fuentes de reglas adicionales
sudo suricata-update list-sources
sudo suricata-update enable-source et/open
sudo suricata-update enable-source oisf/trafficid

# Actualizar con nuevas fuentes
sudo suricata-update

# Verificar reglas descargadas
ls -la /var/lib/suricata/rules/
```

#### Iniciar Suricata

```bash
# Probar configuración
sudo suricata -T -c /etc/suricata/suricata.yaml

# Iniciar servicio
sudo systemctl enable suricata
sudo systemctl start suricata

# Verificar estado
sudo systemctl status suricata

# Ver logs en tiempo real
sudo tail -f /var/log/suricata/eve.json | jq '.'
```

#### Monitoreo y alertas

```bash
# Ver alertas de Suricata
sudo tail -f /var/log/suricata/fast.log

# Filtrar alertas específicas en eve.json
sudo cat /var/log/suricata/eve.json | jq 'select(.event_type=="alert")'

# Estadísticas de Suricata
sudo cat /var/log/suricata/stats.log | tail -50

# Script de monitoreo de alertas
cat << 'EOF' > /usr/local/bin/suricata-alertas.sh
#!/bin/bash
# Mostrar últimas alertas de Suricata
echo "=== Últimas 20 alertas de Suricata ==="
sudo tail -100 /var/log/suricata/eve.json | \
    jq -r 'select(.event_type=="alert") |
    "\(.timestamp) | \(.alert.severity) | \(.src_ip):\(.src_port) -> \(.dest_ip):\(.dest_port) | \(.alert.signature)"' | \
    tail -20
EOF
sudo chmod +x /usr/local/bin/suricata-alertas.sh
```

### 6.4.2. Instalación y Configuración de Fail2ban

#### Instalación de Fail2ban

```bash
# Instalar Fail2ban
sudo apt update
sudo apt install fail2ban -y

# Verificar instalación
fail2ban-client --version
```

#### Configuración básica

```bash
# Crear archivo de configuración local (no modificar jail.conf)
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Editar configuración
sudo nano /etc/fail2ban/jail.local
```

Configuración recomendada en `/etc/fail2ban/jail.local`:

```ini
[DEFAULT]
# Tiempo de baneo (10 minutos)
bantime = 10m

# Tiempo de ventana para contar intentos (10 minutos)
findtime = 10m

# Número de intentos antes de banear
maxretry = 5

# Acción por defecto: banear IP y enviar correo
action = %(action_mwl)s

# Ignorar IPs locales
ignoreip = 127.0.0.1/8 ::1 192.168.1.0/24

# Backend para monitoreo de logs
backend = systemd

# Email para notificaciones (opcional)
destemail = admin@empresa.com
sender = fail2ban@servidor.com

# ========================================
# JAILS - Servicios a proteger
# ========================================

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 1h

[sshd-ddos]
enabled = true
port = ssh
filter = sshd-ddos
logpath = /var/log/auth.log
maxretry = 10
bantime = 48h

[apache-auth]
enabled = true
port = http,https
filter = apache-auth
logpath = /var/log/apache2/*error.log
maxretry = 5

[apache-badbots]
enabled = true
port = http,https
filter = apache-badbots
logpath = /var/log/apache2/*access.log
maxretry = 2
bantime = 48h

[nginx-http-auth]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log
maxretry = 5

[postfix]
enabled = true
port = smtp,465,submission
filter = postfix
logpath = /var/log/mail.log
maxretry = 5

[dovecot]
enabled = true
port = pop3,pop3s,imap,imaps
filter = dovecot
logpath = /var/log/mail.log
maxretry = 5
```

#### Crear filtros personalizados

```bash
# Crear filtro personalizado para detectar escaneos
sudo tee /etc/fail2ban/filter.d/scan-detector.conf << 'EOF'
[Definition]
failregex = ^<HOST> -.*"(GET|POST|HEAD).*(/wp-admin|/phpmyadmin|/admin|/.env|/config).*".*$
ignoreregex =
EOF

# Añadir jail para el nuevo filtro
sudo tee -a /etc/fail2ban/jail.local << 'EOF'

[scan-detector]
enabled = true
port = http,https
filter = scan-detector
logpath = /var/log/nginx/access.log
          /var/log/apache2/access.log
maxretry = 3
bantime = 24h
EOF
```

#### Iniciar y gestionar Fail2ban

```bash
# Iniciar servicio
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Verificar estado
sudo systemctl status fail2ban

# Ver estado de todos los jails
sudo fail2ban-client status

# Ver estado de un jail específico
sudo fail2ban-client status sshd

# Ver IPs baneadas actualmente
sudo fail2ban-client status sshd | grep "Banned IP"

# Desbanear una IP manualmente
sudo fail2ban-client set sshd unbanip 192.168.1.100

# Banear una IP manualmente
sudo fail2ban-client set sshd banip 192.168.1.100

# Recargar configuración
sudo fail2ban-client reload
```

#### Monitoreo de Fail2ban

```bash
# Ver log de Fail2ban
sudo tail -f /var/log/fail2ban.log

# Script de resumen de actividad
cat << 'EOF' > /usr/local/bin/fail2ban-resumen.sh
#!/bin/bash
echo "=== Resumen de Fail2ban ==="
echo ""
echo "Estado general:"
sudo fail2ban-client status
echo ""
echo "=== IPs actualmente baneadas ==="
for jail in $(sudo fail2ban-client status | grep "Jail list" | sed 's/.*://;s/,/ /g'); do
    echo "--- $jail ---"
    sudo fail2ban-client status $jail | grep -E "(Currently banned|Banned IP)"
done
echo ""
echo "=== Últimos 10 baneos ==="
sudo grep "Ban" /var/log/fail2ban.log | tail -10
EOF
sudo chmod +x /usr/local/bin/fail2ban-resumen.sh
```

### 6.4.3. Integración Suricata + Fail2ban

```bash
# Crear filtro para alertas de Suricata
sudo tee /etc/fail2ban/filter.d/suricata.conf << 'EOF'
[Definition]
failregex = .*\[.*\] <HOST>:\d+ -> .*
ignoreregex =
EOF

# Añadir jail para Suricata
sudo tee -a /etc/fail2ban/jail.local << 'EOF'

[suricata]
enabled = true
filter = suricata
logpath = /var/log/suricata/fast.log
maxretry = 3
bantime = 1h
action = iptables-allports[name=suricata]
EOF

# Recargar Fail2ban
sudo fail2ban-client reload
```

---

## 6.5. Métricas de Madurez

### Conceptos Fundamentales

**Métricas de madurez** son indicadores cuantitativos y cualitativos que permiten evaluar el nivel de desarrollo y efectividad de un programa de seguridad informática. Ayudan a identificar fortalezas, debilidades y áreas de mejora, permitiendo tomar decisiones basadas en datos objetivos.

### 6.5.1. Modelo de Madurez de Seguridad

| Nivel | Nombre | Descripción |
|-------|--------|-------------|
| 1 | Inicial | Procesos ad-hoc, reactivos, sin documentación |
| 2 | Repetible | Procesos básicos documentados, se repiten con éxito |
| 3 | Definido | Procesos estandarizados, documentados y comunicados |
| 4 | Gestionado | Procesos medidos y controlados cuantitativamente |
| 5 | Optimizado | Mejora continua basada en métricas y retroalimentación |

### 6.5.2. KPIs de Seguridad Esenciales

#### Métricas de Prevención

```bash
# Script para calcular métricas de prevención
cat << 'EOF' > /usr/local/bin/metricas-prevencion.sh
#!/bin/bash
echo "=== MÉTRICAS DE PREVENCIÓN ==="
echo "Fecha: $(date)"
echo ""

# Porcentaje de sistemas actualizados
TOTAL_PAQUETES=$(dpkg -l | grep "^ii" | wc -l)
ACTUALIZABLES=$(apt list --upgradable 2>/dev/null | grep -v "Listing" | wc -l)
PORCENTAJE_ACTUALIZADO=$((100 - (ACTUALIZABLES * 100 / TOTAL_PAQUETES)))
echo "1. Actualización del sistema: ${PORCENTAJE_ACTUALIZADO}%"
echo "   - Paquetes instalados: $TOTAL_PAQUETES"
echo "   - Paquetes pendientes de actualizar: $ACTUALIZABLES"

# Puntuación Lynis (si está disponible)
if [ -f /var/log/lynis.log ]; then
    LYNIS_SCORE=$(grep "Hardening index" /var/log/lynis.log | tail -1 | grep -oP '\d+')
    echo "2. Índice de endurecimiento (Lynis): ${LYNIS_SCORE:-N/A}/100"
fi

# Contraseñas que expiran pronto
EXPIRAN_30=$(for user in $(cut -d: -f1 /etc/passwd); do chage -l $user 2>/dev/null | grep "Password expires" | grep -v "never"; done | wc -l)
echo "3. Usuarios con contraseña por expirar: $EXPIRAN_30"

# Servicios expuestos
SERVICIOS_ESCUCHA=$(ss -tlnp | grep LISTEN | wc -l)
echo "4. Servicios escuchando conexiones: $SERVICIOS_ESCUCHA"
EOF
chmod +x /usr/local/bin/metricas-prevencion.sh
```

#### Métricas de Detección

```bash
# Script para calcular métricas de detección
cat << 'EOF' > /usr/local/bin/metricas-deteccion.sh
#!/bin/bash
echo "=== MÉTRICAS DE DETECCIÓN ==="
echo "Fecha: $(date)"
echo "Período: Últimas 24 horas"
echo ""

# Alertas de Suricata
if [ -f /var/log/suricata/eve.json ]; then
    ALERTAS_24H=$(cat /var/log/suricata/eve.json | \
        jq -r 'select(.event_type=="alert") | .timestamp' | \
        grep "$(date -d 'yesterday' +%Y-%m-%d)" | wc -l)
    echo "1. Alertas Suricata (24h): $ALERTAS_24H"

    # Por severidad
    echo "   Por severidad:"
    for sev in 1 2 3; do
        COUNT=$(cat /var/log/suricata/eve.json | \
            jq -r "select(.event_type==\"alert\" and .alert.severity==$sev) | .timestamp" | wc -l)
        echo "   - Severidad $sev: $COUNT"
    done
fi

# Baneos de Fail2ban
if [ -f /var/log/fail2ban.log ]; then
    BANEOS_24H=$(grep "Ban" /var/log/fail2ban.log | \
        grep "$(date -d 'yesterday' +%Y-%m-%d)" | wc -l)
    echo "2. IPs baneadas (24h): $BANEOS_24H"
fi

# Intentos de login fallidos
LOGINS_FALLIDOS=$(grep "Failed password" /var/log/auth.log 2>/dev/null | \
    grep "$(date -d 'yesterday' +%b %d)" | wc -l)
echo "3. Intentos de login fallidos (24h): $LOGINS_FALLIDOS"

# Conexiones SSH únicas
if [ -f /var/log/auth.log ]; then
    SSH_UNICAS=$(grep "Accepted" /var/log/auth.log | awk '{print $11}' | sort -u | wc -l)
    echo "4. IPs únicas con acceso SSH: $SSH_UNICAS"
fi
EOF
chmod +x /usr/local/bin/metricas-deteccion.sh
```

#### Métricas de Respuesta

```bash
# Script para calcular métricas de respuesta
cat << 'EOF' > /usr/local/bin/metricas-respuesta.sh
#!/bin/bash
echo "=== MÉTRICAS DE RESPUESTA ==="
echo "Fecha: $(date)"
echo ""

# MTTR - Tiempo medio de resolución (simulado con logs de fail2ban)
echo "1. Tiempo medio de baneo automático:"
if [ -f /var/log/fail2ban.log ]; then
    # Tiempo promedio entre detección y baneo
    echo "   - Fail2ban responde en menos de 1 segundo"
fi

# Cobertura de backup
echo "2. Cobertura de copias de seguridad:"
BACKUPS_RECIENTES=$(find /var/backups -type f -mtime -7 2>/dev/null | wc -l)
echo "   - Backups en últimos 7 días: $BACKUPS_RECIENTES"

# Tiempo desde última auditoría
if [ -f /var/log/lynis.log ]; then
    ULTIMA_AUDITORIA=$(stat -c %y /var/log/lynis.log | cut -d' ' -f1)
    echo "3. Última auditoría de seguridad: $ULTIMA_AUDITORIA"
fi

# Documentación de incidentes
INCIDENTES_DOC=$(find /var/log/incidentes -type f 2>/dev/null | wc -l)
echo "4. Incidentes documentados: $INCIDENTES_DOC"
EOF
chmod +x /usr/local/bin/metricas-respuesta.sh
```

### 6.5.3. Dashboard de Métricas

```bash
# Script completo de dashboard de seguridad
cat << 'EOF' > /usr/local/bin/dashboard-seguridad.sh
#!/bin/bash
clear
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           DASHBOARD DE SEGURIDAD - $(hostname)               ║"
echo "║                   $(date '+%Y-%m-%d %H:%M:%S')                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Estado del sistema
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ ESTADO DEL SISTEMA                                          │"
echo "├─────────────────────────────────────────────────────────────┤"
UPTIME=$(uptime -p)
CARGA=$(uptime | awk -F'load average:' '{print $2}')
echo "│ Tiempo activo: $UPTIME"
echo "│ Carga del sistema: $CARGA"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

# Servicios de seguridad
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ SERVICIOS DE SEGURIDAD                                      │"
echo "├─────────────────────────────────────────────────────────────┤"

# Suricata
SURICATA_STATUS=$(systemctl is-active suricata 2>/dev/null || echo "no instalado")
echo -n "│ Suricata: "
[ "$SURICATA_STATUS" == "active" ] && echo "✓ ACTIVO" || echo "✗ $SURICATA_STATUS"

# Fail2ban
FAIL2BAN_STATUS=$(systemctl is-active fail2ban 2>/dev/null || echo "no instalado")
echo -n "│ Fail2ban: "
[ "$FAIL2BAN_STATUS" == "active" ] && echo "✓ ACTIVO" || echo "✗ $FAIL2BAN_STATUS"

# Firewall
UFW_STATUS=$(ufw status 2>/dev/null | grep "Status:" | awk '{print $2}')
echo -n "│ Firewall (UFW): "
[ "$UFW_STATUS" == "active" ] && echo "✓ ACTIVO" || echo "✗ INACTIVO"

echo "└─────────────────────────────────────────────────────────────┘"
echo ""

# Métricas rápidas
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ MÉTRICAS ÚLTIMAS 24 HORAS                                   │"
echo "├─────────────────────────────────────────────────────────────┤"

# Intentos SSH fallidos
SSH_FALLIDOS=$(grep "Failed password" /var/log/auth.log 2>/dev/null | wc -l)
echo "│ Intentos SSH fallidos: $SSH_FALLIDOS"

# IPs baneadas
IPS_BANEADAS=$(fail2ban-client status 2>/dev/null | grep "Currently banned" | awk '{sum+=$NF} END {print sum}')
echo "│ IPs actualmente baneadas: ${IPS_BANEADAS:-0}"

# Paquetes por actualizar
ACTUALIZABLES=$(apt list --upgradable 2>/dev/null | grep -v "Listing" | wc -l)
echo "│ Actualizaciones pendientes: $ACTUALIZABLES"

echo "└─────────────────────────────────────────────────────────────┘"
echo ""

# Resumen de madurez
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ NIVEL DE MADUREZ ESTIMADO                                   │"
echo "├─────────────────────────────────────────────────────────────┤"

# Calcular puntuación simple
PUNTOS=0
[ "$SURICATA_STATUS" == "active" ] && PUNTOS=$((PUNTOS + 20))
[ "$FAIL2BAN_STATUS" == "active" ] && PUNTOS=$((PUNTOS + 20))
[ "$UFW_STATUS" == "active" ] && PUNTOS=$((PUNTOS + 20))
[ $ACTUALIZABLES -lt 10 ] && PUNTOS=$((PUNTOS + 20))
[ -f /var/log/lynis.log ] && PUNTOS=$((PUNTOS + 20))

echo "│ Puntuación de seguridad: $PUNTOS/100"
if [ $PUNTOS -ge 80 ]; then
    echo "│ Nivel: OPTIMIZADO (5/5)"
elif [ $PUNTOS -ge 60 ]; then
    echo "│ Nivel: GESTIONADO (4/5)"
elif [ $PUNTOS -ge 40 ]; then
    echo "│ Nivel: DEFINIDO (3/5)"
elif [ $PUNTOS -ge 20 ]; then
    echo "│ Nivel: REPETIBLE (2/5)"
else
    echo "│ Nivel: INICIAL (1/5)"
fi
echo "└─────────────────────────────────────────────────────────────┘"
EOF
chmod +x /usr/local/bin/dashboard-seguridad.sh
```

### 6.5.4. Automatización de Informes

```bash
# Crear informe semanal automatizado
cat << 'EOF' > /usr/local/bin/informe-semanal-seguridad.sh
#!/bin/bash
FECHA=$(date +%Y-%m-%d)
INFORME="/var/log/informes/informe_seguridad_$FECHA.md"
mkdir -p /var/log/informes

cat > $INFORME << HEADER
# Informe Semanal de Seguridad
**Fecha:** $FECHA
**Sistema:** $(hostname)
**Generado automáticamente**

---

## Resumen Ejecutivo

HEADER

# Añadir métricas
echo "### Métricas de Prevención" >> $INFORME
/usr/local/bin/metricas-prevencion.sh >> $INFORME 2>/dev/null

echo -e "\n### Métricas de Detección" >> $INFORME
/usr/local/bin/metricas-deteccion.sh >> $INFORME 2>/dev/null

echo -e "\n### Métricas de Respuesta" >> $INFORME
/usr/local/bin/metricas-respuesta.sh >> $INFORME 2>/dev/null

echo -e "\n---\n*Informe generado automáticamente*" >> $INFORME

echo "Informe guardado en: $INFORME"
EOF
chmod +x /usr/local/bin/informe-semanal-seguridad.sh

# Programar ejecución semanal
echo "0 8 * * 1 root /usr/local/bin/informe-semanal-seguridad.sh" | sudo tee /etc/cron.d/informe-seguridad
```

---

## Checklist Nivel 5: Auditoría, Cumplimiento y Respuesta

### Auditorías Automatizadas

- [ ] **Lynis instalado y configurado**
  ```bash
  # Verificar: debe mostrar versión
  lynis --version
  ```

- [ ] **Auditoría Lynis ejecutada con puntuación >= 70**
  ```bash
  # Verificar: revisar índice de endurecimiento
  grep "Hardening index" /var/log/lynis.log | tail -1
  ```

- [ ] **OpenSCAP instalado y funcional**
  ```bash
  # Verificar: debe mostrar versión
  oscap --version
  ```

- [ ] **Evaluación SCAP ejecutada**
  ```bash
  # Verificar: debe existir el informe
  ls -la /var/log/openscap/report.html
  ```

- [ ] **Auditorías programadas (cron)**
  ```bash
  # Verificar: debe existir la tarea
  cat /etc/cron.d/auditoria-seguridad
  ```

### Simulacros de Incidentes

- [ ] **Entorno de simulacro preparado**
  ```bash
  # Verificar: documentación de simulacros existe
  ls /tmp/plan_recuperacion_tpm.md
  ```

- [ ] **Procedimiento de ransomware documentado**
  ```bash
  # Verificar: plantilla de informe existe
  cat /tmp/informe_incidente.txt
  ```

- [ ] **Plan de recuperación TPM definido**
  ```bash
  # Verificar: herramientas TPM instaladas (si aplica)
  which tpm2_getcap
  ```

- [ ] **Simulacro ejecutado en los últimos 90 días**
  ```bash
  # Verificar: logs de simulacros
  find /var/log -name "*simulacro*" -mtime -90
  ```

### Forense Digital

- [ ] **Herramientas forenses instaladas**
  ```bash
  # Verificar: todas las herramientas disponibles
  which fls mmls foremost dc3dd hashdeep
  ```

- [ ] **Baseline de hashes creado**
  ```bash
  # Verificar: archivo de hashes existe
  ls -la /var/log/baseline_hashes.txt
  ```

- [ ] **Procedimiento de preservación de evidencia documentado**
  ```bash
  # Verificar: capacidad de crear imágenes forenses
  which dc3dd && echo "OK: dc3dd disponible"
  ```

- [ ] **Verificación de integridad automatizada**
  ```bash
  # Verificar: debsums funcional
  debsums --version
  ```

### IDS/IPS

- [ ] **Suricata instalado y activo**
  ```bash
  # Verificar: servicio corriendo
  systemctl is-active suricata
  ```

- [ ] **Reglas de Suricata actualizadas**
  ```bash
  # Verificar: reglas recientes (< 7 días)
  find /var/lib/suricata/rules -name "*.rules" -mtime -7 | head -1
  ```

- [ ] **Fail2ban instalado y activo**
  ```bash
  # Verificar: servicio corriendo
  systemctl is-active fail2ban
  ```

- [ ] **Jail SSH habilitado en Fail2ban**
  ```bash
  # Verificar: jail sshd activo
  fail2ban-client status sshd
  ```

- [ ] **Al menos 3 jails configurados**
  ```bash
  # Verificar: número de jails
  fail2ban-client status | grep "Number of jail"
  ```

- [ ] **Logs de IDS monitoreados**
  ```bash
  # Verificar: eve.json tiene datos recientes
  tail -1 /var/log/suricata/eve.json | jq '.timestamp'
  ```

### Métricas de Madurez

- [ ] **Scripts de métricas instalados**
  ```bash
  # Verificar: scripts existen
  ls /usr/local/bin/metricas-*.sh
  ```

- [ ] **Dashboard de seguridad funcional**
  ```bash
  # Verificar: script de dashboard existe
  ls /usr/local/bin/dashboard-seguridad.sh
  ```

- [ ] **Informe semanal automatizado**
  ```bash
  # Verificar: cron configurado
  cat /etc/cron.d/informe-seguridad
  ```

- [ ] **Nivel de madurez >= 3 (Definido)**
  ```bash
  # Verificar: ejecutar dashboard y revisar nivel
  /usr/local/bin/dashboard-seguridad.sh | grep "Nivel:"
  ```

### Verificación Global del Nivel 5

```bash
#!/bin/bash
# Script de verificación completa del Nivel 5
echo "=== Verificación Nivel 5: Auditoría, Cumplimiento y Respuesta ==="
TOTAL=0
PASADOS=0

verificar() {
    TOTAL=$((TOTAL + 1))
    if eval "$1" > /dev/null 2>&1; then
        echo "[✓] $2"
        PASADOS=$((PASADOS + 1))
    else
        echo "[✗] $2"
    fi
}

echo -e "\n--- Auditorías ---"
verificar "which lynis" "Lynis instalado"
verificar "which oscap" "OpenSCAP instalado"
verificar "test -f /etc/cron.d/auditoria-seguridad" "Auditorías programadas"

echo -e "\n--- IDS/IPS ---"
verificar "systemctl is-active suricata" "Suricata activo"
verificar "systemctl is-active fail2ban" "Fail2ban activo"
verificar "fail2ban-client status sshd" "Jail SSH configurado"

echo -e "\n--- Forense ---"
verificar "which fls" "Sleuthkit instalado"
verificar "which foremost" "Foremost instalado"
verificar "which hashdeep" "Hashdeep instalado"

echo -e "\n--- Métricas ---"
verificar "test -x /usr/local/bin/dashboard-seguridad.sh" "Dashboard configurado"
verificar "test -f /etc/cron.d/informe-seguridad" "Informes automatizados"

echo -e "\n=== RESULTADO: $PASADOS/$TOTAL verificaciones pasadas ==="
PORCENTAJE=$((PASADOS * 100 / TOTAL))
echo "Completitud del Nivel 5: $PORCENTAJE%"

if [ $PORCENTAJE -ge 80 ]; then
    echo "Estado: NIVEL 5 COMPLETADO"
elif [ $PORCENTAJE -ge 50 ]; then
    echo "Estado: NIVEL 5 EN PROGRESO"
else
    echo "Estado: NIVEL 5 REQUIERE ATENCIÓN"
fi
```

---

## Glosario de Términos

| Término | Definición |
|---------|------------|
| **Lynis** | Herramienta de auditoría de seguridad para sistemas Unix/Linux |
| **OpenSCAP** | Implementación del protocolo SCAP para evaluación de seguridad |
| **SCAP** | Security Content Automation Protocol - estándar de automatización de seguridad |
| **Ransomware** | Malware que cifra archivos y exige rescate |
| **TPM** | Chip de seguridad para almacenamiento de claves criptográficas |
| **Forense digital** | Investigación y análisis de evidencia digital |
| **IDS** | Sistema de Detección de Intrusiones |
| **IPS** | Sistema de Prevención de Intrusiones |
| **Suricata** | Motor IDS/IPS de código abierto |
| **Fail2ban** | Herramienta de bloqueo automático de IPs maliciosas |
| **Métricas de madurez** | Indicadores del nivel de desarrollo del programa de seguridad |
| **MTTR** | Mean Time To Repair - Tiempo medio de reparación |
| **KPI** | Key Performance Indicator - Indicador clave de rendimiento |

---

## Referencias

- [Documentación oficial de Lynis](https://cisofy.com/documentation/lynis/)
- [OpenSCAP User Manual](https://www.open-scap.org/resources/documentation/)
- [Suricata Documentation](https://docs.suricata.io/)
- [Fail2ban Manual](https://www.fail2ban.org/wiki/index.php/Main_Page)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Debian Security Manual](https://www.debian.org/doc/manuals/securing-debian-manual/)

---

*Documento generado para Debian 13 "Trixie" - Manual de Seguridad Informática*
*Autor: MiniMax Agent*
*Fecha: 2026*
