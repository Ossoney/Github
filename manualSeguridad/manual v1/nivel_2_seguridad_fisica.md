# Nivel 2: Seguridad Física y Arranque Confiable

## Manual de Seguridad Informática para Debian 13 "Trixie"

---

## Introducción

La seguridad informática no comienza con el software: comienza con el acceso físico al hardware. Un atacante con acceso físico a un equipo puede eludir la mayoría de las protecciones lógicas. Este nivel del manual aborda las medidas de seguridad física y los mecanismos de arranque confiable necesarios para proteger sistemas Debian 13 "Trixie".

---

## 3.1. Protección de Instalaciones (CCTV, Cerraduras, Alarmas)

### Conceptos Fundamentales

La primera línea de defensa en seguridad informática es la **seguridad perimetral**: las barreras físicas que impiden el acceso no autorizado a las instalaciones donde se encuentran los equipos informáticos.

### Componentes Clave

#### CCTV (Circuito Cerrado de Televisión)

El **CCTV** es un sistema de videovigilancia que transmite señales a un conjunto específico de monitores, a diferencia de la televisión convencional que transmite abiertamente. Sus características esenciales incluyen:

- **Cobertura 24/7**: Grabación continua de áreas críticas
- **Almacenamiento seguro**: Los registros deben guardarse en ubicaciones separadas del área vigilada
- **Retención mínima**: Se recomienda conservar grabaciones durante al menos 30 días
- **Resolución adecuada**: Mínimo 1080p para identificación facial

#### Cerraduras de Alta Seguridad

| Tipo | Descripción | Nivel de Seguridad |
|------|-------------|-------------------|
| Mecánicas de alta seguridad | Cilindros con protección anti-ganzúa | Medio |
| Electrónicas con código | Requieren PIN numérico | Medio-Alto |
| Electromagnéticas | Controladas por sistema centralizado | Alto |
| Biométricas | Requieren huella dactilar o reconocimiento facial | Muy Alto |

#### Sistemas de Alarma

Los sistemas de alarma deben incluir:

- **Sensores de movimiento PIR** (Infrarrojo Pasivo)
- **Sensores de apertura** en puertas y ventanas
- **Sirenas audibles** y alertas silenciosas
- **Conexión con central de monitoreo**
- **Respaldo de energía** (UPS o baterías)

### Recomendaciones para Centros de Datos

```
Zona de Servidores:
├── Acceso restringido únicamente a personal autorizado
├── Registro de entrada/salida obligatorio
├── Cámaras en todos los puntos de acceso
├── Sensores de temperatura y humedad
└── Detección y extinción de incendios
```

---

## 3.2. Control Físico de Acceso (Tarjetas RFID, Biometría)

### Definiciones Técnicas

**RFID (Radio Frequency Identification)**: Tecnología de identificación por radiofrecuencia que permite la lectura de información almacenada en etiquetas o tarjetas mediante ondas de radio, sin necesidad de contacto físico ni línea de visión directa.

**Biometría**: Método de identificación basado en características físicas únicas de una persona, como huellas dactilares, iris, rostro o voz.

### Sistemas de Control de Acceso

#### Tarjetas RFID

Las tarjetas RFID funcionan mediante un chip que almacena un identificador único. Cuando se acerca al lector, este emite una señal de radio que energiza el chip y lee su información.

**Tipos de tarjetas RFID:**

| Frecuencia | Rango | Uso Común | Seguridad |
|------------|-------|-----------|-----------|
| 125 kHz (LF) | < 10 cm | Acceso básico | Baja (clonables) |
| 13.56 MHz (HF) | < 1 m | Tarjetas inteligentes | Media-Alta |
| 860-960 MHz (UHF) | Hasta 12 m | Logística | Variable |

**Recomendación**: Utilizar tarjetas HF con cifrado (como MIFARE DESFire EV3) para control de acceso a áreas con equipos informáticos.

#### Sistemas Biométricos

```
Métodos Biométricos por Nivel de Seguridad:
┌─────────────────────────────────────────────────┐
│ Muy Alto │ Reconocimiento de iris              │
│          │ Reconocimiento vascular             │
├──────────┼─────────────────────────────────────┤
│ Alto     │ Huella dactilar multiespectral      │
│          │ Reconocimiento facial 3D            │
├──────────┼─────────────────────────────────────┤
│ Medio    │ Huella dactilar capacitiva          │
│          │ Reconocimiento facial 2D            │
├──────────┼─────────────────────────────────────┤
│ Básico   │ Reconocimiento de voz               │
│          │ Geometría de la mano                │
└──────────┴─────────────────────────────────────┘
```

### Autenticación Multifactor Física

La mejor práctica es combinar múltiples factores:

1. **Algo que tienes**: Tarjeta RFID o token físico
2. **Algo que sabes**: PIN o contraseña
3. **Algo que eres**: Característica biométrica

**Ejemplo de configuración recomendada:**
```
Acceso a sala de servidores:
    Factor 1: Tarjeta RFID cifrada
    Factor 2: PIN de 6 dígitos
    Factor 3: Huella dactilar

    → Los tres factores deben validarse en menos de 30 segundos
```

---

## 3.3. Seguridad del Hardware y Firmware

### Definición de Firmware

**Firmware**: Software permanente programado en la memoria de solo lectura del hardware. Es el código de bajo nivel que controla el funcionamiento básico de un dispositivo, actuando como intermediario entre el hardware y el sistema operativo.

---

### 3.3.1. BIOS/UEFI: Password, Secure Boot y TPM 2.0

#### Definiciones Fundamentales

**BIOS (Basic Input/Output System)**: Sistema básico de entrada/salida. Es el firmware tradicional que inicializa el hardware del computador y carga el sistema operativo. Funciona en modo de 16 bits y tiene limitaciones significativas en sistemas modernos.

**UEFI (Unified Extensible Firmware Interface)**: Interfaz de firmware extensible unificada. Es el sucesor moderno del BIOS que ofrece una interfaz gráfica, soporte para discos grandes (más de 2 TB), arranque más rápido y características de seguridad avanzadas como Secure Boot.

**Secure Boot**: Característica de seguridad de UEFI que verifica que cada componente de software cargado durante el arranque esté firmado digitalmente por un editor de confianza. Esto previene la ejecución de código malicioso antes de que el sistema operativo tome control.

**TPM (Trusted Platform Module)**: Módulo de plataforma confiable. Es un chip criptográfico dedicado, soldado a la placa base, que proporciona funciones de seguridad basadas en hardware como generación de claves, cifrado y medición de integridad del sistema.

#### Configuración de Contraseña UEFI

La contraseña de UEFI/BIOS previene cambios no autorizados en la configuración del firmware:

1. **Contraseña de administrador**: Protege el acceso a la configuración UEFI
2. **Contraseña de usuario**: Requerida para arrancar el sistema
3. **Contraseña de disco duro**: Cifra el acceso al almacenamiento (ATA Security)

**Acceso a la configuración UEFI en Debian:**
```bash
# Reiniciar y acceder a UEFI (generalmente F2, F12, DEL o ESC durante el arranque)
sudo systemctl reboot --firmware-setup
```

#### Habilitación de Secure Boot en Debian 13

Debian 13 "Trixie" soporta Secure Boot de forma nativa. Para verificar y gestionar su estado:

```bash
# Verificar si Secure Boot está activo
mokutil --sb-state

# Salida esperada si está habilitado:
# SecureBoot enabled

# Verificar el modo de arranque (UEFI o BIOS)
[ -d /sys/firmware/efi ] && echo "UEFI" || echo "BIOS/Legacy"

# Listar las claves de Secure Boot enrolladas
mokutil --list-enrolled
```

**Gestión de Secure Boot con sbctl:**

`sbctl` es una herramienta para gestionar Secure Boot con claves propias:

```bash
# Instalar sbctl
sudo apt update
sudo apt install sbctl

# Verificar estado de Secure Boot
sudo sbctl status

# Crear claves propias (requiere Secure Boot en modo Setup)
sudo sbctl create-keys

# Enrollar claves en el firmware
sudo sbctl enroll-keys

# Firmar el kernel y bootloader
sudo sbctl sign -s /boot/efi/EFI/debian/shimx64.efi
sudo sbctl sign -s /boot/efi/EFI/debian/grubx64.efi
sudo sbctl sign -s /boot/vmlinuz-$(uname -r)

# Verificar archivos firmados
sudo sbctl verify
```

#### Configuración y Uso de TPM 2.0

El TPM 2.0 almacena mediciones criptográficas del proceso de arranque en registros llamados **PCRs (Platform Configuration Registers)**:

```bash
# Instalar herramientas de TPM
sudo apt install tpm2-tools

# Verificar presencia del TPM
sudo tpm2_getcap properties-fixed | grep -i "TPM2_PT_FAMILY_INDICATOR"

# Verificar que el TPM está operativo
sudo systemctl status tpm2-abrmd

# Mostrar información del TPM
sudo tpm2_getcap properties-variable

# Analizar los PCRs (Registros de Configuración de Plataforma)
sudo systemd-analyze pcrs
```

**Significado de los PCRs principales:**

| PCR | Contenido Medido |
|-----|------------------|
| PCR 0 | Código del firmware (UEFI) |
| PCR 1 | Configuración del firmware |
| PCR 2 | Código de terceros (Option ROMs) |
| PCR 4 | Gestor de arranque (bootloader) |
| PCR 5 | Configuración del gestor de arranque |
| PCR 7 | Estado de Secure Boot |
| PCR 8-9 | Línea de comandos del kernel |
| PCR 11 | Mediciones de systemd-stub |

```bash
# Ver valores actuales de todos los PCRs
sudo tpm2_pcrread

# Ver PCRs específicos (0, 4 y 7)
sudo tpm2_pcrread sha256:0,4,7

# Usar systemd para análisis detallado de PCRs
sudo systemd-analyze pcrs
```

---

### 3.3.2. Control de Puertos USB (USBGuard) y BadUSB

#### Definición de BadUSB

**BadUSB**: Ataque que explota vulnerabilidades en el firmware de dispositivos USB. Un dispositivo aparentemente inofensivo (como una memoria USB) puede reprogramarse para actuar como un teclado que ejecuta comandos maliciosos automáticamente, eludiendo antivirus y otras protecciones de software.

**Ejemplos de ataques BadUSB:**
- Rubber Ducky: Dispositivo que emula un teclado y escribe comandos predefinidos
- Cable O.MG: Cable de carga con hardware malicioso oculto
- USBNinja: Dispositivos que combinan funcionalidad legítima con payloads maliciosos

#### Instalación y Configuración de USBGuard

USBGuard es un framework de autorización de dispositivos USB que implementa listas blancas/negras:

```bash
# Instalar USBGuard
sudo apt update
sudo apt install usbguard

# Habilitar el servicio
sudo systemctl enable usbguard
sudo systemctl start usbguard

# Verificar estado
sudo systemctl status usbguard
```

**Generación de política inicial:**

```bash
# Generar política basada en dispositivos actualmente conectados
# IMPORTANTE: Conectar solo dispositivos de confianza antes de ejecutar
sudo usbguard generate-policy > /etc/usbguard/rules.conf

# Reiniciar el servicio para aplicar la política
sudo systemctl restart usbguard
```

**Gestión de dispositivos USB:**

```bash
# Listar dispositivos USB actuales
sudo usbguard list-devices

# Ejemplo de salida:
# 1: allow id 1d6b:0002 serial "0000:00:14.0" name "xHCI Host Controller"
# 5: block id 0951:1666 serial "E0D55EA573E5B0A159A90256" name "DataTraveler 3.0"

# Permitir un dispositivo bloqueado (temporal, hasta reinicio)
sudo usbguard allow-device 5

# Permitir un dispositivo permanentemente
sudo usbguard allow-device 5 --permanent

# Bloquear un dispositivo específico
sudo usbguard block-device 5

# Rechazar (desconectar eléctricamente) un dispositivo
sudo usbguard reject-device 5
```

**Archivo de reglas (/etc/usbguard/rules.conf):**

```bash
# Sintaxis básica de reglas USBGuard
# allow|block|reject [condiciones]

# Permitir todos los hubs USB del sistema
allow with-interface equals { 09:*:* }

# Permitir teclados y ratones HID
allow with-interface one-of { 03:00:01 03:01:01 03:01:02 }

# Permitir un dispositivo específico por ID de fabricante/producto
allow id 0781:5567 # SanDisk Cruzer Blade

# Bloquear dispositivos que se presentan como múltiples interfaces
block with-interface count-of > 2

# Bloquear dispositivos que emulan teclados excepto los permitidos
block with-interface equals { 03:01:01 }

# Política por defecto: bloquear todo lo no especificado
block
```

**Configuración avanzada (/etc/usbguard/usbguard-daemon.conf):**

```bash
# Ver configuración actual
sudo cat /etc/usbguard/usbguard-daemon.conf

# Opciones importantes:
# RuleFile=/etc/usbguard/rules.conf
# ImplicitPolicyTarget=block  # Acción por defecto
# PresentDevicePolicy=apply-policy
# InsertedDevicePolicy=apply-policy
# AuthorizedDefault=none  # Ningún dispositivo autorizado por defecto
# IPCAllowedUsers=root
# IPCAllowedGroups=wheel
```

**Monitoreo de eventos USB:**

```bash
# Ver log de eventos USB en tiempo real
sudo journalctl -f -u usbguard

# Auditar dispositivos conectados recientemente
sudo usbguard list-rules

# Exportar reglas actuales
sudo usbguard export-rules > reglas_backup.conf
```

---

### 3.3.3. Protección contra Manipulación de Arranque (Evil Maid)

#### Definición de Evil Maid Attack

**Evil Maid Attack (Ataque de la Criada Malvada)**: Ataque que requiere acceso físico temporal al equipo objetivo. El atacante modifica el gestor de arranque o instala un keylogger de hardware para capturar contraseñas de cifrado de disco. El nombre proviene del escenario donde un atacante (como personal de limpieza de hotel) tiene acceso breve al equipo desatendido.

**Escenario típico:**
1. El atacante accede físicamente al equipo apagado
2. Arranca desde un medio externo
3. Modifica GRUB o instala malware en el sector de arranque
4. El usuario arranca normalmente e ingresa su contraseña
5. El malware captura la contraseña y la almacena o transmite

#### Medidas de Protección

**1. Secure Boot (Primera línea de defensa):**

Ya configurado en la sección anterior, previene la carga de bootloaders no firmados.

**2. Cifrado completo de disco con LUKS:**

```bash
# Verificar que el disco está cifrado con LUKS
sudo cryptsetup status /dev/mapper/debian-root

# Ver información de la partición cifrada
sudo cryptsetup luksDump /dev/sda3  # Ajustar partición según sistema
```

**3. Medición de arranque con TPM:**

Vincular el descifrado de LUKS al estado del TPM:

```bash
# Instalar systemd-cryptenroll para gestión de LUKS con TPM
sudo apt install systemd-cryptsetup

# Vincular LUKS al TPM (PCRs 0,4,7)
sudo systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=0+4+7 /dev/sda3

# Esto permite que el disco solo se descifre si:
# - El firmware no ha sido modificado (PCR 0)
# - El bootloader no ha sido modificado (PCR 4)
# - Secure Boot mantiene su configuración (PCR 7)
```

**4. Verificación de integridad del bootloader:**

```bash
# Verificar firma del bootloader GRUB
sudo sbctl verify /boot/efi/EFI/debian/grubx64.efi

# Verificar integridad de archivos críticos de arranque
sha256sum /boot/vmlinuz-$(uname -r) > /root/kernel_hash.txt
sha256sum /boot/initrd.img-$(uname -r) >> /root/kernel_hash.txt
sha256sum /boot/efi/EFI/debian/grubx64.efi >> /root/kernel_hash.txt

# Comparar en cada arranque (puede automatizarse)
sha256sum -c /root/kernel_hash.txt
```

**5. Sellos de seguridad físicos:**

Aplicar sellos de seguridad **tamper-evident** en:
- Tornillos de la carcasa del equipo
- Puertos USB no utilizados
- Bahías de disco duro

**6. Contraseña de GRUB:**

```bash
# Generar hash de contraseña para GRUB
grub-mkpasswd-pbkdf2

# Agregar a /etc/grub.d/40_custom:
cat << 'EOF' | sudo tee -a /etc/grub.d/40_custom
set superusers="admin"
password_pbkdf2 admin grub.pbkdf2.sha512.10000.HASH_GENERADO
EOF

# Actualizar GRUB
sudo update-grub
```

---

## 3.4. Cableado Estructurado Seguro

### Principios de Seguridad en Cableado

El cableado de red representa un punto vulnerable frecuentemente ignorado. Un atacante con acceso al cableado puede interceptar tráfico o inyectar datos maliciosos.

### Medidas de Protección

#### Clasificación de Zonas de Cableado

```
Zona de Seguridad Alta (Restringida):
├── Cableado de backbone entre centros de datos
├── Conexiones a servidores críticos
├── Enlaces de fibra óptica principales
└── Cableado de sistemas de seguridad

Zona de Seguridad Media (Controlada):
├── Cableado horizontal a estaciones de trabajo
├── Conexiones a switches de acceso
└── Cableado de VoIP

Zona de Seguridad Baja (General):
├── Puntos de red en áreas públicas
├── Conexiones para invitados
└── Cableado temporal
```

#### Recomendaciones Técnicas

| Aspecto | Recomendación |
|---------|---------------|
| Tipo de cable | Cat6A o superior para nuevas instalaciones |
| Fibra óptica | Preferida para enlaces entre edificios (inmune a interferencias) |
| Bandejas y canaletas | Cerradas con tapa y cerradura |
| Patch panels | En armarios con llave |
| Etiquetado | Sistema estandarizado (TIA-606) |
| Documentación | Planos actualizados y acceso restringido |

#### Protección contra Interceptación

**1. Detección de intrusiones en el cableado:**

```bash
# Monitorear cambios en la topología de red
sudo apt install lldpd
sudo systemctl enable lldpd
sudo systemctl start lldpd

# Ver dispositivos descubiertos
lldpcli show neighbors

# Detectar cambios inesperados en direcciones MAC
sudo apt install arpwatch
sudo systemctl enable arpwatch
sudo systemctl start arpwatch

# Ver alertas de arpwatch
sudo journalctl -u arpwatch -f
```

**2. Cifrado de capa 2 (MACsec):**

```bash
# MACsec proporciona cifrado punto a punto en Ethernet
# Verificar soporte de hardware
ethtool -k eth0 | grep macsec

# Configurar MACsec con NetworkManager
nmcli connection add type macsec \
  con-name macsec-link \
  ifname macsec0 \
  connection.autoconnect yes \
  macsec.parent eth0 \
  macsec.mode psk \
  macsec.mka-cak 1234567890abcdef1234567890abcdef \
  macsec.mka-ckn 00112233445566778899aabbccddeeff
```

---

## 3.5. Routers/Switches: Tamper-evident y Etiquetado

### Definición de Tamper-evident

**Tamper-evident (Evidencia de manipulación)**: Característica de un dispositivo o embalaje que revela visualmente cualquier intento de acceso no autorizado. Incluye sellos, etiquetas holográficas, tornillos especiales o materiales que se rompen o decoloran al ser manipulados.

### Seguridad Física de Equipos de Red

#### Ubicación y Montaje

```
Requisitos de Instalación Segura:
┌─────────────────────────────────────────────────────────┐
│ RACK/GABINETE                                           │
├─────────────────────────────────────────────────────────┤
│ - Puertas con cerradura (frontal y trasera)            │
│ - Paneles laterales fijos con tornillos de seguridad   │
│ - Anclaje al piso o pared                              │
│ - Ventilación adecuada con filtros                     │
│ - Sensor de apertura de puerta                         │
└─────────────────────────────────────────────────────────┘
```

#### Sistema de Etiquetado

**Estándar TIA-606-C para etiquetado:**

```
Formato de etiqueta: EDIFICIO-PISO-RACK-PUERTO
Ejemplo: ED1-P3-RK02-SW01-P24

Código de colores recomendado:
- Azul: Conexiones de datos estándar
- Naranja: Fibra óptica multimodo
- Amarillo: Fibra óptica monomodo
- Verde: Conexiones de red demilitarizada (DMZ)
- Rojo: Conexiones críticas/seguridad
- Blanco: Conexiones de telefonía
```

#### Sellos Tamper-evident

**Tipos de sellos recomendados:**

| Tipo | Aplicación | Características |
|------|------------|-----------------|
| Etiquetas holográficas | Tornillos de acceso | Se destruyen al despegar |
| Sellos numerados | Puertas de rack | Secuencia verificable |
| Cinta de seguridad | Cables y conectores | Deja residuo "VOID" |
| Esmalte de uñas/pintura | Tornillos | Método económico, visible |

#### Verificación y Auditoría

```bash
# Crear inventario de equipos de red
cat << 'EOF' > /root/inventario_red.sh
#!/bin/bash
echo "=== Inventario de Equipos de Red ==="
echo "Fecha: $(date)"
echo ""
echo "--- Interfaces de Red ---"
ip link show
echo ""
echo "--- Vecinos LLDP ---"
lldpcli show neighbors
echo ""
echo "--- Tabla ARP ---"
ip neigh show
echo ""
echo "--- Rutas ---"
ip route show
EOF

chmod +x /root/inventario_red.sh

# Verificar cambios en la configuración de interfaces
sudo apt install ethtool
for iface in $(ls /sys/class/net/); do
    echo "=== $iface ==="
    ethtool $iface 2>/dev/null | grep -E "Speed|Duplex|Link detected"
done
```

**Registro de verificación de sellos:**

```bash
# Crear registro de verificación de sellos de seguridad
cat << 'EOF' > /root/verificacion_sellos.sh
#!/bin/bash
FECHA=$(date +%Y-%m-%d)
HORA=$(date +%H:%M)
ARCHIVO="/var/log/sellos_$FECHA.log"

echo "Verificación de Sellos - $FECHA $HORA" >> $ARCHIVO
echo "Inspector: $1" >> $ARCHIVO
echo "---" >> $ARCHIVO

# Lista de equipos a verificar
EQUIPOS=("SW-CORE-01" "SW-ACC-01" "SW-ACC-02" "RT-BORDE-01")

for equipo in "${EQUIPOS[@]}"; do
    read -p "Estado del sello $equipo (OK/ROTO/FALTANTE): " estado
    echo "$equipo: $estado" >> $ARCHIVO
done

echo "---" >> $ARCHIVO
echo "Verificación completada" >> $ARCHIVO
EOF

chmod +x /root/verificacion_sellos.sh
```

---

## Checklist Nivel 2: Seguridad Física y Arranque Confiable

### Lista de Verificación con Comandos

Ejecute los siguientes comandos para verificar el estado de seguridad de su sistema Debian 13:

#### A. Verificación de Firmware y Arranque

```bash
# 1. Verificar modo de arranque (UEFI requerido)
[ -d /sys/firmware/efi ] && echo "[OK] Sistema arrancado en modo UEFI" || echo "[FALLO] Sistema en modo BIOS Legacy"

# 2. Verificar estado de Secure Boot
mokutil --sb-state

# 3. Verificar estado con sbctl
sudo sbctl status

# 4. Verificar archivos de arranque firmados
sudo sbctl verify

# 5. Verificar presencia y estado del TPM
sudo systemctl status tpm2-abrmd

# 6. Analizar PCRs del TPM
sudo systemd-analyze pcrs

# 7. Leer valores de PCRs críticos
sudo tpm2_pcrread sha256:0,4,7

# 8. Verificar cifrado de disco LUKS
sudo cryptsetup status /dev/mapper/*-root 2>/dev/null || echo "[INFO] Verificar partición cifrada manualmente"
```

#### B. Verificación de Control USB (USBGuard)

```bash
# 9. Verificar que USBGuard está instalado y activo
sudo systemctl is-active usbguard && echo "[OK] USBGuard activo" || echo "[FALLO] USBGuard no activo"

# 10. Verificar política de dispositivos USB
sudo usbguard list-rules | head -20

# 11. Listar dispositivos USB actuales y su estado
sudo usbguard list-devices

# 12. Verificar configuración de USBGuard
grep -E "^(ImplicitPolicyTarget|PresentDevicePolicy)" /etc/usbguard/usbguard-daemon.conf
```

#### C. Verificación de Red y Monitoreo

```bash
# 13. Verificar servicio LLDP para detección de topología
sudo systemctl is-active lldpd && echo "[OK] LLDP activo" || echo "[ADVERTENCIA] LLDP no instalado"

# 14. Verificar servicio arpwatch para detección de cambios MAC
sudo systemctl is-active arpwatch 2>/dev/null && echo "[OK] arpwatch activo" || echo "[ADVERTENCIA] arpwatch no instalado"

# 15. Listar interfaces de red
ip link show | grep -E "^[0-9]+:" | awk '{print $2}'
```

#### D. Script Completo de Auditoría

```bash
#!/bin/bash
# Script de auditoría de seguridad física - Nivel 2
# Guardar como: /root/auditoria_nivel2.sh

echo "=============================================="
echo " Auditoría de Seguridad Física - Nivel 2"
echo " Debian 13 Trixie"
echo " Fecha: $(date)"
echo "=============================================="
echo ""

# Función para mostrar resultado
check() {
    if [ $? -eq 0 ]; then
        echo "[OK] $1"
    else
        echo "[FALLO] $1"
    fi
}

echo "=== A. FIRMWARE Y ARRANQUE ==="
echo ""

# UEFI
echo -n "1. Modo UEFI: "
[ -d /sys/firmware/efi ] && echo "OK" || echo "FALLO (BIOS Legacy)"

# Secure Boot
echo -n "2. Secure Boot: "
mokutil --sb-state 2>/dev/null | grep -q "enabled" && echo "OK (Habilitado)" || echo "ADVERTENCIA (Deshabilitado)"

# sbctl status
echo "3. Estado sbctl:"
sudo sbctl status 2>/dev/null || echo "   sbctl no instalado"

# TPM
echo -n "4. TPM 2.0: "
sudo systemctl is-active tpm2-abrmd &>/dev/null && echo "OK (Activo)" || echo "ADVERTENCIA (No activo)"

# PCRs
echo "5. Análisis de PCRs:"
sudo systemd-analyze pcrs 2>/dev/null | head -15 || echo "   No se pueden leer PCRs"

echo ""
echo "=== B. CONTROL USB ==="
echo ""

# USBGuard
echo -n "6. USBGuard: "
sudo systemctl is-active usbguard &>/dev/null && echo "OK (Activo)" || echo "FALLO (No activo)"

# Política USB
echo "7. Reglas USBGuard activas:"
sudo usbguard list-rules 2>/dev/null | wc -l | xargs echo "   Número de reglas:"

# Dispositivos bloqueados
echo "8. Dispositivos USB bloqueados:"
sudo usbguard list-devices 2>/dev/null | grep -c "block" | xargs echo "   Cantidad:"

echo ""
echo "=== C. INTEGRIDAD DE ARRANQUE ==="
echo ""

# Verificar firmas
echo "9. Verificación de firmas sbctl:"
sudo sbctl verify 2>/dev/null || echo "   sbctl no configurado"

# LUKS
echo "10. Cifrado de disco:"
sudo cryptsetup status $(ls /dev/mapper/ | grep -v control | head -1) 2>/dev/null | grep -q "LUKS" && echo "   OK (LUKS activo)" || echo "   ADVERTENCIA (Verificar manualmente)"

echo ""
echo "=== D. MONITOREO DE RED ==="
echo ""

# LLDP
echo -n "11. LLDP: "
sudo systemctl is-active lldpd &>/dev/null && echo "OK" || echo "No instalado"

# arpwatch
echo -n "12. arpwatch: "
sudo systemctl is-active arpwatch &>/dev/null && echo "OK" || echo "No instalado"

echo ""
echo "=============================================="
echo " Auditoría completada"
echo "=============================================="
```

### Resumen de Comandos de Verificación Rápida

| Verificación | Comando |
|--------------|---------|
| Modo UEFI | `[ -d /sys/firmware/efi ] && echo UEFI` |
| Secure Boot | `mokutil --sb-state` |
| Estado sbctl | `sudo sbctl status` |
| Verificar firmas | `sudo sbctl verify` |
| Estado TPM | `sudo systemctl status tpm2-abrmd` |
| Analizar PCRs | `sudo systemd-analyze pcrs` |
| Leer PCRs | `sudo tpm2_pcrread sha256:0,4,7` |
| USBGuard activo | `sudo systemctl is-active usbguard` |
| Listar USB | `sudo usbguard list-devices` |
| Reglas USB | `sudo usbguard list-rules` |
| LUKS status | `sudo cryptsetup status /dev/mapper/root` |

### Acciones Correctivas

Si alguna verificación falla, consulte la sección correspondiente de este manual:

- **UEFI no detectado** → Reinstalar Debian en modo UEFI
- **Secure Boot deshabilitado** → Sección 3.3.1
- **TPM no funcional** → Verificar en UEFI que esté habilitado
- **USBGuard inactivo** → Sección 3.3.2
- **Firmas no válidas** → Ejecutar `sudo sbctl sign-all`

---

## Referencias

- Debian Security Manual: https://www.debian.org/doc/manuals/securing-debian-manual/
- USBGuard Documentation: https://usbguard.github.io/
- TPM 2.0 Tools: https://github.com/tpm2-software/tpm2-tools
- UEFI Specification: https://uefi.org/specifications
- TIA-606 Labeling Standard: https://www.tiaonline.org/

---

*Documento generado para el Manual de Seguridad Informática de Debian 13 "Trixie"*
*Nivel 2: Seguridad Física y Arranque Confiable*
*Autor: MiniMax Agent*
