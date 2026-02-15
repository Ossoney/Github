# Nivel 3: Seguridad Lógica - Sistema Base (Debian 13)

---

## Introducción

Este nivel aborda la configuración segura del hardware de red y la instalación y endurecimiento de Debian 13 "Trixie" como sistema operativo base. Aquí se establecen los cimientos de seguridad sobre los cuales se construirán las capas superiores de protección.

---

## Glosario de Términos Técnicos

Antes de comenzar, es importante familiarizarse con los conceptos clave que se utilizarán a lo largo de este documento:

| Término | Definición |
|---------|------------|
| **VLAN** | *Virtual Local Area Network* (Red de Área Local Virtual). Tecnología que permite dividir una red física en múltiples redes lógicas aisladas, mejorando la seguridad y el rendimiento al separar el tráfico de diferentes grupos de dispositivos. |
| **MAC Spoofing** | Técnica de ataque donde un atacante falsifica la dirección MAC (identificador único del hardware de red) de su dispositivo para hacerse pasar por otro equipo autorizado en la red. |
| **Hardening** | Proceso de endurecimiento o fortificación de un sistema mediante la reducción de su superficie de ataque, eliminando servicios innecesarios y aplicando configuraciones de seguridad estrictas. |
| **LUKS2** | *Linux Unified Key Setup versión 2*. Estándar de cifrado de disco completo en Linux que protege los datos almacenados mediante algoritmos criptográficos robustos. |
| **tmpfs** | Sistema de archivos temporal que reside completamente en la memoria RAM, ofreciendo alta velocidad y la garantía de que los datos se eliminan al reiniciar. |
| **netinst** | *Network Installation*. Imagen de instalación mínima de Debian que descarga únicamente los paquetes necesarios desde Internet, reduciendo la superficie de ataque inicial. |
| **Bootloader** | Programa que se ejecuta al encender el ordenador, responsable de cargar el sistema operativo. Es el primer software que se ejecuta y, por tanto, un punto crítico de seguridad. |
| **GRUB** | *GRand Unified Bootloader*. El bootloader más utilizado en sistemas Linux, capaz de arrancar múltiples sistemas operativos. |
| **UKI** | *Unified Kernel Image* (Imagen de Kernel Unificada). Archivo único que combina el kernel de Linux, el initramfs y los parámetros de arranque, facilitando el arranque seguro. |
| **PAM** | *Pluggable Authentication Modules*. Sistema modular de autenticación en Linux que permite configurar diferentes métodos de verificación de identidad. |
| **2FA** | *Two-Factor Authentication* (Autenticación de Dos Factores). Método de seguridad que requiere dos formas distintas de verificación: algo que sabes (contraseña) y algo que tienes (código temporal). |
| **setuid** | Permiso especial en sistemas Unix que permite ejecutar un programa con los privilegios del propietario del archivo, generalmente root. Potencialmente peligroso si se abusa de él. |
| **AppArmor** | Sistema de control de acceso obligatorio (MAC) que restringe las capacidades de los programas mediante perfiles de seguridad predefinidos. |
| **nftables** | Framework moderno de filtrado de paquetes en el kernel de Linux que reemplaza a iptables. Proporciona un firewall más eficiente y con sintaxis unificada. |
| **UFW** | *Uncomplicated Firewall*. Interfaz simplificada para gestionar reglas de firewall, ideal para usuarios que prefieren comandos más intuitivos. |

---

## 4.1. Hardware de Red Seguro

La seguridad comienza en la capa física y de enlace de datos. Un hardware de red mal configurado puede invalidar todas las medidas de seguridad implementadas en capas superiores.

### 4.1.1. Configuración de Switches (VLANs, Port Security)

Los switches gestionables permiten implementar controles de seguridad a nivel de red local.

#### Creación de VLANs para Segmentación de Red

La segmentación mediante VLANs aísla diferentes tipos de tráfico y limita la propagación de amenazas.

**Esquema de VLANs recomendado:**

| VLAN ID | Nombre | Propósito | Rango IP |
|---------|--------|-----------|----------|
| 1 | Default | No usar (deshabilitar) | - |
| 10 | Gestión | Administración de equipos | 192.168.10.0/24 |
| 20 | Servidores | Servicios internos | 192.168.20.0/24 |
| 30 | Usuarios | Estaciones de trabajo | 192.168.30.0/24 |
| 40 | IoT | Dispositivos inteligentes | 192.168.40.0/24 |
| 99 | Cuarentena | Dispositivos no confiables | 192.168.99.0/24 |

**Configuración en switch gestionable (ejemplo con Open vSwitch en Debian 13):**

```bash
# Instalar Open vSwitch
sudo apt update
sudo apt install -y openvswitch-switch

# Crear bridge virtual
sudo ovs-vsctl add-br br0

# Añadir puerto físico al bridge
sudo ovs-vsctl add-port br0 enp1s0

# Crear VLANs
sudo ovs-vsctl set port enp1s0 tag=10          # Puerto de acceso VLAN 10
sudo ovs-vsctl set port enp2s0 trunks=10,20,30 # Puerto trunk

# Verificar configuración
sudo ovs-vsctl show
```

#### Port Security (Seguridad de Puerto)

Limita qué dispositivos pueden conectarse a cada puerto del switch.

```bash
# Configuración de port security con Open vSwitch
# Limitar a una MAC por puerto
sudo ovs-vsctl set port enp1s0 other_config:max-mac-addresses=1

# Habilitar aprendizaje de MAC seguro
sudo ovs-vsctl set bridge br0 other-config:mac-aging-time=300
```

**Archivo de configuración persistente `/etc/network/interfaces.d/vlans`:**

```bash
# Interfaz VLAN 10 - Gestión
auto enp1s0.10
iface enp1s0.10 inet static
    address 192.168.10.1
    netmask 255.255.255.0
    vlan-raw-device enp1s0

# Interfaz VLAN 20 - Servidores
auto enp1s0.20
iface enp1s0.20 inet static
    address 192.168.20.1
    netmask 255.255.255.0
    vlan-raw-device enp1s0
```

### 4.1.2. Router Hardening (OpenWRT/Debian)

El router es el punto de entrada a la red y debe configurarse con especial cuidado.

#### Opción A: Debian 13 como Router

**Habilitar enrutamiento IP:**

```bash
# Habilitar IP forwarding de forma persistente
echo 'net.ipv4.ip_forward = 1' | sudo tee /etc/sysctl.d/90-router.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/90-router.conf

# Aplicar cambios
sudo sysctl --system
```

**Deshabilitar servicios innecesarios:**

```bash
# Listar servicios activos
systemctl list-units --type=service --state=running

# Deshabilitar servicios no esenciales para un router
sudo systemctl disable --now avahi-daemon.service
sudo systemctl disable --now cups.service
sudo systemctl disable --now bluetooth.service
sudo systemctl mask avahi-daemon.service cups.service bluetooth.service
```

**Configuración de seguridad del kernel (`/etc/sysctl.d/91-hardening.conf`):**

```bash
# Protección contra ataques de red
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1
net.ipv4.tcp_syncookies = 1

# Protección IPv6
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0
```

#### Opción B: OpenWRT Hardening

Para routers dedicados con OpenWRT:

```bash
# Acceder via SSH (cambiar contraseña por defecto primero)
ssh root@192.168.1.1

# Cambiar contraseña de root
passwd

# Deshabilitar acceso HTTP (usar solo HTTPS)
uci set uhttpd.main.listen_http=''
uci set uhttpd.main.listen_https='0.0.0.0:443'
uci commit uhttpd
/etc/init.d/uhttpd restart

# Cambiar puerto SSH y deshabilitar acceso desde WAN
uci set dropbear.@dropbear[0].Port='2222'
uci set dropbear.@dropbear[0].Interface='lan'
uci commit dropbear
/etc/init.d/dropbear restart

# Habilitar actualizaciones automáticas de listas de bloqueo
opkg update
opkg install banip
```

### 4.1.3. Control de MAC Spoofing

El MAC spoofing permite a atacantes evadir controles basados en direcciones MAC.

**Detección de MAC spoofing con arpwatch:**

```bash
# Instalar arpwatch
sudo apt install -y arpwatch

# Configurar para cada interfaz
sudo nano /etc/default/arpwatch
```

**Contenido de `/etc/default/arpwatch`:**

```bash
# Interfaces a monitorizar
INTERFACES="enp1s0 enp2s0"

# Opciones adicionales
ARGS="-N -p"
```

**Habilitar y verificar:**

```bash
# Iniciar servicio
sudo systemctl enable --now arpwatch

# Verificar detecciones
sudo tail -f /var/log/syslog | grep arpwatch
```

**Implementar 802.1X para autenticación de puerto:**

```bash
# Instalar hostapd para autenticación 802.1X
sudo apt install -y hostapd freeradius

# Configuración básica de hostapd para 802.1X cableado
sudo nano /etc/hostapd/wired.conf
```

**Contenido de `/etc/hostapd/wired.conf`:**

```bash
interface=enp1s0
driver=wired
ieee8021x=1
eap_server=0
auth_server_addr=127.0.0.1
auth_server_port=1812
auth_server_shared_secret=ClaveSecretaRADIUS
```

---

## 4.2. Instalación Segura de Debian 13 "Trixie"

Debian 13 "Trixie" introduce mejoras significativas en seguridad. Una instalación cuidadosa establece las bases para un sistema robusto.

### 4.2.1. Particionado Moderno: LUKS2 con systemd-cryptenroll

LUKS2 proporciona cifrado de disco con mejoras respecto a su predecesor, incluyendo mejor resistencia a ataques de fuerza bruta y soporte para tokens de seguridad.

#### Esquema de Particionado Recomendado

| Partición | Tamaño | Sistema de Archivos | Punto de Montaje | Cifrado |
|-----------|--------|---------------------|------------------|---------|
| EFI | 512 MB | FAT32 | /boot/efi | No |
| Boot | 1 GB | ext4 | /boot | No* |
| Sistema | Resto | LUKS2 + LVM | / | Sí |

*Con UKI, /boot puede integrarse en la partición EFI.

#### Creación de Particiones Cifradas Durante la Instalación

Durante el instalador de Debian:

1. Seleccionar "Particionado manual"
2. Crear partición EFI (512 MB, FAT32)
3. Crear partición boot (1 GB, ext4)
4. Crear partición para LUKS con el resto del espacio

#### Configuración Post-Instalación con systemd-cryptenroll

`systemd-cryptenroll` permite agregar métodos adicionales de desbloqueo.

```bash
# Verificar estado actual de LUKS
sudo cryptsetup luksDump /dev/sda3

# Agregar clave de recuperación imprimible
sudo systemd-cryptenroll --recovery-key /dev/sda3

# IMPORTANTE: Guardar la clave de recuperación en lugar seguro
```

**Agregar desbloqueo mediante TPM 2.0 (si está disponible):**

```bash
# Verificar disponibilidad de TPM
sudo systemd-cryptenroll --tpm2-device=list

# Registrar TPM para desbloqueo automático
sudo systemd-cryptenroll --tpm2-device=auto \
    --tpm2-pcrs=0+7 \
    /dev/sda3
```

**Agregar token FIDO2 (llave de seguridad USB):**

```bash
# Instalar soporte FIDO2
sudo apt install -y libfido2-1

# Registrar token FIDO2
sudo systemd-cryptenroll --fido2-device=auto /dev/sda3
```

**Configuración de `/etc/crypttab` para arranque:**

```bash
# Ejemplo de crypttab con múltiples métodos
sda3_crypt UUID=xxxx-xxxx-xxxx none luks,discard,tpm2-device=auto,fido2-device=auto
```

### 4.2.2. Sistema de Archivos: /tmp en tmpfs (RAM)

Montar `/tmp` en memoria RAM tiene múltiples beneficios de seguridad:
- Los archivos temporales se eliminan automáticamente al reiniciar
- Mayor velocidad de acceso
- Reduce el desgaste de discos SSD
- Los archivos temporales nunca tocan el disco (importantes para datos sensibles)

**Configurar /tmp en tmpfs:**

```bash
# Verificar si ya está configurado
mount | grep /tmp

# Añadir a /etc/fstab
echo 'tmpfs /tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=2G 0 0' | sudo tee -a /etc/fstab

# Montar inmediatamente
sudo systemctl daemon-reload
sudo mount /tmp
```

**Opciones de seguridad explicadas:**

| Opción | Función |
|--------|---------|
| `nosuid` | Ignora bits setuid/setgid (previene escalada de privilegios) |
| `nodev` | No permite dispositivos especiales (previene ataques mediante dispositivos) |
| `noexec` | Prohíbe ejecución de binarios (previene ejecución de malware en /tmp) |
| `mode=1777` | Sticky bit activo (usuarios solo pueden borrar sus propios archivos) |
| `size=2G` | Limita el tamaño máximo en RAM |

**Configurar también /var/tmp:**

```bash
# /var/tmp también debe ser seguro (pero persiste entre reinicios por diseño)
echo 'tmpfs /var/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=1G 0 0' | sudo tee -a /etc/fstab
```

### 4.2.3. Selección Mínima de Paquetes (netinst)

Una instalación mínima reduce drásticamente la superficie de ataque.

#### Durante la Instalación

1. Descargar imagen netinst de Debian 13 desde `https://www.debian.org/devel/debian-installer/`
2. En la selección de software, desmarcar **todas** las opciones excepto:
   - "Utilidades del sistema estándar"
3. NO seleccionar ningún entorno de escritorio

#### Post-Instalación: Instalar Solo lo Necesario

```bash
# Actualizar sistema base
sudo apt update && sudo apt upgrade -y

# Instalar herramientas esenciales de seguridad únicamente
sudo apt install -y \
    sudo \
    openssh-server \
    ufw \
    fail2ban \
    unattended-upgrades \
    apt-listbugs \
    apt-listchanges \
    needrestart \
    debsums

# Configurar actualizaciones automáticas de seguridad
sudo dpkg-reconfigure -plow unattended-upgrades
```

**Verificar paquetes instalados:**

```bash
# Listar paquetes instalados manualmente
apt-mark showmanual

# Contar paquetes totales (objetivo: menos de 300)
dpkg -l | grep '^ii' | wc -l
```

**Eliminar paquetes innecesarios:**

```bash
# Identificar paquetes huérfanos
sudo apt install -y deborphan
deborphan

# Eliminar paquetes huérfanos
sudo apt autoremove --purge $(deborphan)

# Limpiar caché
sudo apt clean
```

---

## 4.3. Hardening del Bootloader

El bootloader es el primer código que se ejecuta y un objetivo prioritario para atacantes que buscan persistencia.

### 4.3.1. Transición a systemd-boot o GRUB Firmado

Debian 13 soporta Secure Boot con GRUB firmado y ofrece systemd-boot como alternativa más simple.

#### Opción A: GRUB con Secure Boot (Recomendado para la mayoría)

```bash
# Verificar estado de Secure Boot
mokutil --sb-state

# Instalar GRUB firmado para UEFI
sudo apt install -y grub-efi-amd64-signed shim-signed

# Reinstalar GRUB con firma
sudo grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=debian --recheck

# Actualizar configuración
sudo update-grub
```

**Proteger GRUB con contraseña:**

```bash
# Generar hash de contraseña
grub-mkpasswd-pbkdf2

# Añadir a /etc/grub.d/40_custom
sudo nano /etc/grub.d/40_custom
```

**Contenido de `/etc/grub.d/40_custom`:**

```bash
#!/bin/sh
set superusers="admin"
password_pbkdf2 admin grub.pbkdf2.sha512.10000.HASH_GENERADO_AQUI
```

```bash
# Aplicar cambios
sudo chmod 755 /etc/grub.d/40_custom
sudo update-grub
```

#### Opción B: systemd-boot (Más simple, requiere UKI)

```bash
# Instalar systemd-boot
sudo apt install -y systemd-boot

# Instalar en la partición EFI
sudo bootctl install --path=/boot/efi

# Verificar instalación
sudo bootctl status
```

**Configuración de `/boot/efi/loader/loader.conf`:**

```bash
default debian.efi
timeout 3
console-mode max
editor no
```

### 4.3.2. Imágenes de Kernel Unificadas (UKI)

Las UKI combinan kernel, initramfs y cmdline en un único archivo firmado, mejorando la seguridad del arranque.

**Instalar herramientas necesarias:**

```bash
# Instalar ukify (herramienta para crear UKI)
sudo apt install -y systemd-ukify systemd-boot-efi

# Instalar herramientas de firma (opcional, para Secure Boot)
sudo apt install -y sbsigntool
```

**Crear UKI manualmente:**

```bash
# Crear directorio para UKI
sudo mkdir -p /boot/efi/EFI/Linux

# Generar UKI con ukify
sudo ukify build \
    --linux=/boot/vmlinuz-$(uname -r) \
    --initrd=/boot/initrd.img-$(uname -r) \
    --cmdline="root=UUID=$(blkid -s UUID -o value /dev/mapper/sda3_crypt) ro quiet" \
    --output=/boot/efi/EFI/Linux/debian-$(uname -r).efi
```

**Automatizar generación de UKI (`/etc/kernel/postinst.d/zz-ukify`):**

```bash
#!/bin/bash
# Script para generar UKI automáticamente tras actualización de kernel

KERNEL_VERSION=$1
KERNEL_IMAGE=$2

if [ -z "$KERNEL_VERSION" ]; then
    exit 0
fi

ukify build \
    --linux=/boot/vmlinuz-${KERNEL_VERSION} \
    --initrd=/boot/initrd.img-${KERNEL_VERSION} \
    --cmdline="$(cat /etc/kernel/cmdline)" \
    --output=/boot/efi/EFI/Linux/debian-${KERNEL_VERSION}.efi

# Eliminar UKI de kernels antiguos (mantener últimos 2)
ls -t /boot/efi/EFI/Linux/debian-*.efi | tail -n +3 | xargs -r rm
```

```bash
# Hacer ejecutable
sudo chmod +x /etc/kernel/postinst.d/zz-ukify

# Crear archivo de cmdline
echo "root=UUID=$(blkid -s UUID -o value /dev/mapper/sda3_crypt) ro quiet" | sudo tee /etc/kernel/cmdline
```

---

## 4.4. Hardening Básico del Sistema

Esta sección cubre las configuraciones fundamentales de seguridad del sistema operativo.

### 4.4.1. Usuarios y PAM: Desactivar Root, 2FA

#### Desactivar Acceso Directo como Root

```bash
# Bloquear contraseña de root (fuerza uso de sudo)
sudo passwd -l root

# Deshabilitar shell de root
sudo usermod -s /usr/sbin/nologin root

# Verificar
sudo grep root /etc/passwd
# Debe mostrar: root:x:0:0:root:/root:/usr/sbin/nologin
```

**Configurar sudo correctamente:**

```bash
# Crear usuario administrativo si no existe
sudo adduser adminuser
sudo usermod -aG sudo adminuser

# Configurar sudo con restricciones
sudo visudo
```

**Añadir a `/etc/sudoers` (via visudo):**

```bash
# Requerir contraseña siempre
Defaults    timestamp_timeout=5
Defaults    passwd_tries=3
Defaults    logfile="/var/log/sudo.log"
Defaults    log_input, log_output
Defaults    requiretty

# Usuarios administrativos
adminuser   ALL=(ALL:ALL) ALL
```

#### Implementar 2FA con Google Authenticator

```bash
# Instalar módulo PAM de Google Authenticator
sudo apt install -y libpam-google-authenticator

# Configurar para cada usuario (ejecutar como usuario, no root)
google-authenticator
```

**Responder a las preguntas de configuración:**
- `Do you want authentication tokens to be time-based?` → **y**
- `Do you want me to update your "~/.google_authenticator" file?` → **y**
- `Do you want to disallow multiple uses...?` → **y**
- `Do you want to enable rate-limiting?` → **y**

**Configurar PAM para requerir 2FA (`/etc/pam.d/sshd`):**

```bash
# Añadir al inicio del archivo (después de @include common-auth)
auth required pam_google_authenticator.so nullok

# nullok permite acceso sin 2FA si el usuario no lo ha configurado
# Eliminar nullok después de que todos los usuarios lo configuren
```

**Configurar SSH para usar 2FA (`/etc/ssh/sshd_config`):**

```bash
# Habilitar autenticación interactiva
KbdInteractiveAuthentication yes
ChallengeResponseAuthentication yes

# Requerir tanto clave como 2FA
AuthenticationMethods publickey,keyboard-interactive

# Reiniciar SSH
sudo systemctl restart sshd
```

### 4.4.2. Permisos Críticos y Limpieza de setuid

Los binarios con bit setuid ejecutan con privilegios elevados y son vectores de ataque comunes.

**Identificar binarios setuid/setgid:**

```bash
# Buscar todos los binarios setuid
sudo find / -type f -perm -4000 -ls 2>/dev/null

# Buscar todos los binarios setgid
sudo find / -type f -perm -2000 -ls 2>/dev/null

# Guardar lista para auditoría
sudo find / -type f \( -perm -4000 -o -perm -2000 \) -ls 2>/dev/null > /root/setuid_audit.txt
```

**Binarios setuid que generalmente pueden eliminarse:**

```bash
# Eliminar setuid de binarios no esenciales
sudo chmod u-s /usr/bin/newgrp
sudo chmod u-s /usr/bin/chsh
sudo chmod u-s /usr/bin/chfn
sudo chmod u-s /usr/bin/gpasswd
sudo chmod u-s /usr/bin/wall
sudo chmod u-s /usr/bin/write

# Si no se usa mount por usuarios normales
sudo chmod u-s /usr/bin/mount
sudo chmod u-s /usr/bin/umount
```

**Binarios setuid esenciales (NO eliminar):**

| Binario | Función |
|---------|---------|
| `/usr/bin/sudo` | Elevación de privilegios controlada |
| `/usr/bin/passwd` | Cambio de contraseñas |
| `/usr/bin/su` | Cambio de usuario (puede eliminarse si solo se usa sudo) |
| `/usr/lib/openssh/ssh-keysign` | Autenticación SSH basada en host |

**Monitorear cambios en binarios setuid:**

```bash
# Instalar AIDE para detección de intrusiones
sudo apt install -y aide

# Inicializar base de datos
sudo aideinit

# Programar verificación diaria
echo '0 5 * * * root /usr/bin/aide --check' | sudo tee /etc/cron.d/aide-check
```

### 4.4.3. AppArmor: Auditoría y Perfiles en Modo 'Enforce'

AppArmor restringe lo que cada programa puede hacer, limitando el daño de vulnerabilidades.

**Verificar estado de AppArmor:**

```bash
# Instalar herramientas de AppArmor
sudo apt install -y apparmor apparmor-utils apparmor-profiles apparmor-profiles-extra

# Verificar estado
sudo aa-status
```

**Estados de los perfiles:**
- **enforce**: El perfil se aplica activamente (objetivo de seguridad)
- **complain**: Solo registra violaciones sin bloquear (modo auditoría)
- **unconfined**: Sin restricciones (inseguro)

**Habilitar AppArmor si no está activo:**

```bash
# Añadir a parámetros del kernel
sudo nano /etc/default/grub
# Añadir a GRUB_CMDLINE_LINUX: apparmor=1 security=apparmor

# Actualizar GRUB
sudo update-grub
sudo reboot
```

**Poner perfiles en modo enforce:**

```bash
# Ver perfiles en modo complain
sudo aa-complain --list

# Pasar todos los perfiles a modo enforce
sudo aa-enforce /etc/apparmor.d/*

# Pasar perfil específico a enforce
sudo aa-enforce /etc/apparmor.d/usr.sbin.sshd
```

**Crear perfil básico para una aplicación:**

```bash
# Generar perfil automáticamente (modo aprendizaje)
sudo aa-genprof /usr/bin/mi_aplicacion

# En otra terminal, ejecutar la aplicación con todos sus usos normales
# Volver a la terminal de aa-genprof y pulsar 'S' para escanear logs

# Después de ajustar, pasar a enforce
sudo aa-enforce /etc/apparmor.d/usr.bin.mi_aplicacion
```

**Ejemplo de perfil personalizado (`/etc/apparmor.d/usr.local.bin.miapp`):**

```bash
#include <tunables/global>

/usr/local/bin/miapp {
  #include <abstractions/base>
  #include <abstractions/nameservice>

  # Permitir lectura de su propio binario
  /usr/local/bin/miapp mr,

  # Permitir lectura de configuración
  /etc/miapp/** r,

  # Permitir escritura en directorio de logs
  /var/log/miapp/** w,

  # Permitir acceso a red
  network inet stream,
  network inet6 stream,

  # Denegar todo lo demás implícitamente
}
```

```bash
# Cargar perfil
sudo apparmor_parser -r /etc/apparmor.d/usr.local.bin.miapp
```

---

## 4.5. Firewall Base (nftables/UFW)

Un firewall correctamente configurado es esencial para controlar el tráfico de red.

### Opción A: UFW (Recomendado para Principiantes)

UFW proporciona una interfaz simplificada sobre nftables.

**Configuración básica:**

```bash
# Instalar UFW
sudo apt install -y ufw

# Configurar políticas por defecto
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Permitir SSH (¡IMPORTANTE antes de activar!)
sudo ufw allow ssh

# Activar firewall
sudo ufw enable

# Verificar estado
sudo ufw status verbose
```

**Reglas comunes:**

```bash
# Permitir SSH solo desde red local
sudo ufw allow from 192.168.1.0/24 to any port 22

# Permitir HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Permitir puerto específico desde IP específica
sudo ufw allow from 192.168.1.100 to any port 5432

# Denegar IP específica
sudo ufw deny from 10.0.0.5

# Limitar conexiones (protección contra fuerza bruta)
sudo ufw limit ssh

# Ver reglas numeradas (para eliminar)
sudo ufw status numbered

# Eliminar regla
sudo ufw delete 3
```

### Opción B: nftables Directamente (Mayor Control)

Para usuarios avanzados que necesitan mayor flexibilidad.

**Configuración base (`/etc/nftables.conf`):**

```bash
#!/usr/sbin/nft -f

# Limpiar reglas existentes
flush ruleset

# Definir tabla para filtrado IPv4/IPv6
table inet filter {
    # Conjunto de IPs bloqueadas
    set blocklist {
        type ipv4_addr
        flags interval
        elements = { 10.0.0.0/8, 172.16.0.0/12 }
    }

    # Conjunto de puertos permitidos
    set tcp_allowed {
        type inet_service
        elements = { 22, 80, 443 }
    }

    # Cadena de entrada
    chain input {
        type filter hook input priority 0; policy drop;

        # Permitir tráfico de loopback
        iif "lo" accept

        # Permitir conexiones establecidas y relacionadas
        ct state established,related accept

        # Descartar inválidos
        ct state invalid drop

        # Bloquear IPs del blocklist
        ip saddr @blocklist drop

        # Protección contra escaneo de puertos
        tcp flags syn tcp dport != @tcp_allowed \
            limit rate 1/second burst 5 packets \
            log prefix "PORTSCAN: " drop

        # Permitir ICMP (ping) con límite
        ip protocol icmp icmp type echo-request \
            limit rate 5/second accept

        # Permitir puertos TCP configurados
        tcp dport @tcp_allowed accept

        # Registrar y descartar el resto
        log prefix "INPUT DROP: " drop
    }

    # Cadena de salida
    chain output {
        type filter hook output priority 0; policy accept;

        # Permitir todo el tráfico saliente
        # Añadir restricciones según necesidades
    }

    # Cadena de reenvío (para routers)
    chain forward {
        type filter hook forward priority 0; policy drop;

        # Permitir tráfico establecido
        ct state established,related accept

        # Añadir reglas de reenvío entre VLANs aquí
    }
}

# Tabla para NAT (si actúa como router)
table ip nat {
    chain postrouting {
        type nat hook postrouting priority 100;

        # Masquerade para red interna
        ip saddr 192.168.0.0/16 oifname "enp1s0" masquerade
    }
}
```

**Aplicar y habilitar:**

```bash
# Verificar sintaxis
sudo nft -c -f /etc/nftables.conf

# Aplicar reglas
sudo nft -f /etc/nftables.conf

# Habilitar servicio
sudo systemctl enable --now nftables

# Verificar reglas activas
sudo nft list ruleset
```

**Comandos útiles de nftables:**

```bash
# Añadir IP al blocklist dinámicamente
sudo nft add element inet filter blocklist { 203.0.113.50 }

# Eliminar IP del blocklist
sudo nft delete element inet filter blocklist { 203.0.113.50 }

# Ver contadores de reglas
sudo nft list ruleset -a

# Monitorear en tiempo real
sudo nft monitor
```

---

## Checklist Nivel 3: Verificación de Seguridad del Sistema Base

Este checklist permite verificar que todas las medidas de seguridad han sido implementadas correctamente.

### 4.1 Hardware de Red

| # | Verificación | Comando de Comprobación | Estado |
|---|-------------|------------------------|--------|
| 4.1.1a | VLANs configuradas y separadas | `sudo ovs-vsctl show` o `cat /proc/net/vlan/config` | [ ] |
| 4.1.1b | VLAN 1 (default) no en uso | `sudo ovs-vsctl list-ports br0` | [ ] |
| 4.1.1c | Port security habilitado | `sudo ovs-vsctl get port enp1s0 other_config` | [ ] |
| 4.1.2a | IP forwarding habilitado (router) | `sysctl net.ipv4.ip_forward` | [ ] |
| 4.1.2b | Protecciones de red en sysctl | `sysctl -a \| grep rp_filter` | [ ] |
| 4.1.2c | Servicios innecesarios deshabilitados | `systemctl list-units --state=running` | [ ] |
| 4.1.3a | arpwatch instalado y activo | `systemctl status arpwatch` | [ ] |
| 4.1.3b | Logs de MAC spoofing monitoreados | `grep -i flip /var/log/syslog` | [ ] |

### 4.2 Instalación Debian 13

| # | Verificación | Comando de Comprobación | Estado |
|---|-------------|------------------------|--------|
| 4.2.1a | Partición raíz cifrada con LUKS2 | `sudo cryptsetup luksDump /dev/sda3 \| grep Version` | [ ] |
| 4.2.1b | systemd-cryptenroll configurado | `sudo systemd-cryptenroll /dev/sda3 --list` | [ ] |
| 4.2.1c | Clave de recuperación generada y guardada | Verificar manualmente | [ ] |
| 4.2.2a | /tmp montado en tmpfs | `mount \| grep "tmpfs on /tmp"` | [ ] |
| 4.2.2b | /tmp con opciones nosuid,nodev,noexec | `mount \| grep /tmp` | [ ] |
| 4.2.3a | Instalación mínima (<300 paquetes) | `dpkg -l \| grep '^ii' \| wc -l` | [ ] |
| 4.2.3b | unattended-upgrades configurado | `systemctl status unattended-upgrades` | [ ] |
| 4.2.3c | No hay paquetes huérfanos | `deborphan \| wc -l` (debe ser 0) | [ ] |

### 4.3 Bootloader

| # | Verificación | Comando de Comprobación | Estado |
|---|-------------|------------------------|--------|
| 4.3.1a | Secure Boot habilitado | `mokutil --sb-state` | [ ] |
| 4.3.1b | GRUB firmado instalado | `dpkg -l \| grep grub-efi-amd64-signed` | [ ] |
| 4.3.1c | GRUB protegido con contraseña | `grep superusers /boot/grub/grub.cfg` | [ ] |
| 4.3.2a | UKI generada (si aplica) | `ls /boot/efi/EFI/Linux/*.efi` | [ ] |
| 4.3.2b | Script de auto-generación UKI | `test -x /etc/kernel/postinst.d/zz-ukify` | [ ] |

### 4.4 Hardening del Sistema

| # | Verificación | Comando de Comprobación | Estado |
|---|-------------|------------------------|--------|
| 4.4.1a | Root bloqueado | `sudo passwd -S root` (debe mostrar 'L') | [ ] |
| 4.4.1b | Shell de root deshabilitado | `grep root /etc/passwd \| grep nologin` | [ ] |
| 4.4.1c | sudo con logging habilitado | `grep logfile /etc/sudoers` | [ ] |
| 4.4.1d | 2FA configurado para SSH | `grep pam_google_authenticator /etc/pam.d/sshd` | [ ] |
| 4.4.1e | SSH requiere clave + 2FA | `grep AuthenticationMethods /etc/ssh/sshd_config` | [ ] |
| 4.4.2a | Auditoría setuid realizada | `test -f /root/setuid_audit.txt` | [ ] |
| 4.4.2b | Binarios setuid innecesarios eliminados | `find /usr -perm -4000 2>/dev/null \| wc -l` (<10) | [ ] |
| 4.4.2c | AIDE instalado y configurado | `systemctl status aide-check.timer` | [ ] |
| 4.4.3a | AppArmor habilitado | `sudo aa-status \| grep "apparmor module is loaded"` | [ ] |
| 4.4.3b | Perfiles en modo enforce | `sudo aa-status \| grep -c enforce` (>20) | [ ] |
| 4.4.3c | Sin perfiles en modo complain | `sudo aa-status \| grep -c complain` (=0) | [ ] |

### 4.5 Firewall

| # | Verificación | Comando de Comprobación | Estado |
|---|-------------|------------------------|--------|
| 4.5a | Firewall activo | `sudo ufw status` o `sudo nft list ruleset` | [ ] |
| 4.5b | Política por defecto: deny incoming | `sudo ufw status verbose \| grep "Default: deny"` | [ ] |
| 4.5c | Solo puertos necesarios abiertos | `sudo ss -tlnp` | [ ] |
| 4.5d | SSH limitado por IP o rate-limit | `sudo ufw status \| grep -E "22.*LIMIT\|Anywhere"` | [ ] |
| 4.5e | Logging de firewall habilitado | `sudo ufw logging status` o revisar nftables log | [ ] |

---

### Script de Verificación Automática

Guardar como `/usr/local/bin/check-nivel3.sh`:

```bash
#!/bin/bash
# Script de verificación de seguridad - Nivel 3
# Debian 13 "Trixie"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0
WARN=0

check() {
    local description="$1"
    local command="$2"
    local expected="$3"

    result=$(eval "$command" 2>/dev/null)

    if [[ "$result" == *"$expected"* ]]; then
        echo -e "${GREEN}[PASS]${NC} $description"
        ((PASS++))
    else
        echo -e "${RED}[FAIL]${NC} $description"
        ((FAIL++))
    fi
}

warn_check() {
    local description="$1"
    local command="$2"

    if eval "$command" &>/dev/null; then
        echo -e "${GREEN}[PASS]${NC} $description"
        ((PASS++))
    else
        echo -e "${YELLOW}[WARN]${NC} $description"
        ((WARN++))
    fi
}

echo "========================================"
echo " Verificación de Seguridad - Nivel 3"
echo " Debian 13 Sistema Base"
echo "========================================"
echo ""

echo "--- 4.2 Instalación Segura ---"
check "LUKS2 cifrado activo" "cryptsetup luksDump /dev/sda3 2>/dev/null | grep Version" "2"
check "/tmp en tmpfs" "mount | grep 'tmpfs on /tmp'" "tmpfs"
check "/tmp con noexec" "mount | grep /tmp" "noexec"
check "Instalación mínima" "test $(dpkg -l | grep '^ii' | wc -l) -lt 400 && echo 'ok'" "ok"

echo ""
echo "--- 4.3 Bootloader ---"
warn_check "Secure Boot habilitado" "mokutil --sb-state 2>/dev/null | grep -q 'enabled'"
check "GRUB firmado" "dpkg -l | grep grub-efi-amd64-signed" "ii"

echo ""
echo "--- 4.4 Hardening Sistema ---"
check "Root bloqueado" "passwd -S root" "L"
check "AppArmor cargado" "aa-status 2>/dev/null | head -1" "apparmor module is loaded"
check "Perfiles enforce > 15" "test $(aa-status 2>/dev/null | grep -c enforce) -gt 15 && echo 'ok'" "ok"

echo ""
echo "--- 4.5 Firewall ---"
check "UFW/nftables activo" "ufw status 2>/dev/null | head -1 || nft list ruleset | head -1" "active\|table"
check "Política deny incoming" "ufw status verbose 2>/dev/null | grep Default" "deny"

echo ""
echo "========================================"
echo -e "Resultados: ${GREEN}$PASS PASS${NC}, ${RED}$FAIL FAIL${NC}, ${YELLOW}$WARN WARN${NC}"
echo "========================================"

if [ $FAIL -gt 0 ]; then
    exit 1
fi
exit 0
```

```bash
# Hacer ejecutable
sudo chmod +x /usr/local/bin/check-nivel3.sh

# Ejecutar verificación
sudo /usr/local/bin/check-nivel3.sh
```

---

## Resumen

Este nivel ha cubierto los fundamentos de seguridad para un sistema Debian 13:

1. **Hardware de red**: Segmentación con VLANs, protección de puertos y detección de MAC spoofing
2. **Instalación segura**: Cifrado LUKS2, tmpfs para datos temporales e instalación mínima
3. **Bootloader**: Secure Boot, GRUB protegido y UKI para arranque verificable
4. **Hardening**: Desactivación de root, 2FA, limpieza de setuid y AppArmor en modo enforce
5. **Firewall**: Configuración restrictiva con UFW o nftables

El siguiente nivel abordará la seguridad de servicios y aplicaciones que se ejecutan sobre esta base segura.

---

*Documento generado para Manual de Seguridad Informática*
*Nivel 3: Seguridad Lógica - Sistema Base (Debian 13)*
*Autor: MiniMax Agent*
