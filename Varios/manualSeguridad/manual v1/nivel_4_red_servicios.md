# Nivel 4: Red, Servicios y Mantenimiento Avanzado

## Manual de Seguridad Informática para Debian 13 "Trixie"

---

## Glosario de Términos Esenciales

Antes de profundizar en los contenidos técnicos, es fundamental comprender los siguientes términos que aparecerán a lo largo de este nivel:

| Término | Definición |
|---------|------------|
| **DMZ** (Zona Desmilitarizada) | Subred aislada que actúa como zona intermedia entre la red interna (privada) y la red externa (Internet). Aloja servicios públicos como servidores web, minimizando el riesgo si son comprometidos. |
| **DNS** (Sistema de Nombres de Dominio) | Protocolo que traduce nombres de dominio legibles (ejemplo.com) a direcciones IP numéricas (192.168.1.1). |
| **DNSSEC** (Extensiones de Seguridad DNS) | Conjunto de extensiones que añaden firmas criptográficas a las respuestas DNS, permitiendo verificar su autenticidad y prevenir manipulaciones. |
| **DoT** (DNS over TLS) | Protocolo que cifra las consultas DNS mediante TLS, protegiendo la privacidad de las consultas contra espionaje en la red. |
| **VPN** (Red Privada Virtual) | Tecnología que crea un túnel cifrado entre dispositivos a través de Internet, permitiendo comunicaciones seguras como si estuvieran en la misma red local. |
| **WireGuard** | Protocolo VPN moderno, ligero y de alto rendimiento, integrado en el kernel de Linux desde la versión 5.6. |
| **SSH** (Secure Shell) | Protocolo de red que permite acceso remoto seguro a sistemas mediante comunicaciones cifradas. |
| **DSA** (Algoritmo de Firma Digital) | Algoritmo criptográfico antiguo para firmas digitales, actualmente considerado obsoleto e inseguro. |
| **Ed25519** | Algoritmo de firma digital moderno basado en curvas elípticas, ofrece alta seguridad con claves pequeñas y rendimiento excelente. |
| **FIDO2/U2F** | Estándares abiertos de autenticación que permiten usar dispositivos físicos (llaves de seguridad) como segundo factor de autenticación. |
| **CSP** (Política de Seguridad de Contenido) | Cabecera HTTP que define qué recursos puede cargar una página web, previniendo ataques de inyección de código (XSS). |
| **HSTS** (Seguridad de Transporte Estricta HTTP) | Cabecera HTTP que obliga a los navegadores a usar exclusivamente conexiones HTTPS con el servidor. |
| **TLS** (Seguridad de Capa de Transporte) | Protocolo criptográfico que proporciona comunicaciones seguras en Internet. TLS 1.3 es la versión más reciente y segura. |
| **deb822** | Formato moderno de configuración para repositorios APT en Debian, más estructurado y legible que el formato tradicional de una línea. |
| **journald** | Servicio de systemd que recopila y gestiona logs del sistema de forma estructurada, con soporte para firmado criptográfico. |
| **auditd** | Demonio de auditoría del kernel de Linux que registra eventos de seguridad del sistema según reglas configurables. |
| **Estrategia 3-2-1** | Metodología de copias de seguridad: mantener 3 copias de los datos, en 2 tipos de medios diferentes, con 1 copia fuera del sitio. |

---

## 5.1. Arquitectura de Red y DNS

### 5.1.1. Segmentación y DMZ

La **segmentación de red** consiste en dividir una red en subredes más pequeñas y aisladas. Esto limita el movimiento lateral de un atacante que comprometa un sistema, conteniendo el daño potencial.

#### Arquitectura Recomendada

```
┌─────────────────────────────────────────────────────────────────┐
│                         INTERNET                                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                    ┌─────▼─────┐
                    │  Firewall │ (nftables)
                    │  Externo  │
                    └─────┬─────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    ┌────▼────┐     ┌─────▼─────┐    ┌─────▼─────┐
    │   DMZ   │     │  Firewall │    │    LAN    │
    │         │     │  Interno  │    │  Interna  │
    │ - Web   │     └───────────┘    │           │
    │ - Mail  │                      │ - Equipos │
    │ - DNS   │                      │ - Servers │
    └─────────┘                      └───────────┘
   192.168.10.0/24                  192.168.20.0/24
```

#### Configuración de nftables para DMZ

Cree el archivo `/etc/nftables.conf`:

```bash
#!/usr/sbin/nft -f

flush ruleset

# Definición de variables
define LAN_NET = 192.168.20.0/24
define DMZ_NET = 192.168.10.0/24
define WAN_IF = "eth0"
define LAN_IF = "eth1"
define DMZ_IF = "eth2"

table inet filter {
    # Cadena de entrada: tráfico hacia el firewall
    chain input {
        type filter hook input priority 0; policy drop;

        # Permitir tráfico establecido y relacionado
        ct state established,related accept

        # Permitir loopback
        iif "lo" accept

        # Permitir ICMP (ping) limitado
        ip protocol icmp icmp type echo-request limit rate 5/second accept

        # Permitir SSH solo desde LAN
        iifname $LAN_IF tcp dport 22 accept

        # Registrar y descartar el resto
        log prefix "INPUT DROP: " drop
    }

    # Cadena de reenvío: tráfico entre interfaces
    chain forward {
        type filter hook forward priority 0; policy drop;

        # Permitir tráfico establecido
        ct state established,related accept

        # LAN puede acceder a DMZ e Internet
        iifname $LAN_IF oifname $DMZ_IF accept
        iifname $LAN_IF oifname $WAN_IF accept

        # DMZ puede salir a Internet (para actualizaciones)
        iifname $DMZ_IF oifname $WAN_IF accept

        # DMZ NO puede acceder a LAN (regla crítica de seguridad)
        iifname $DMZ_IF oifname $LAN_IF drop

        # Permitir acceso desde Internet a servicios DMZ
        iifname $WAN_IF oifname $DMZ_IF tcp dport { 80, 443 } accept

        log prefix "FORWARD DROP: " drop
    }

    # Cadena de salida: tráfico desde el firewall
    chain output {
        type filter hook output priority 0; policy accept;
    }
}

# Tabla NAT para traducción de direcciones
table inet nat {
    chain prerouting {
        type nat hook prerouting priority -100;

        # Redirigir tráfico web a servidor DMZ
        iifname $WAN_IF tcp dport { 80, 443 } dnat to 192.168.10.10
    }

    chain postrouting {
        type nat hook postrouting priority 100;

        # Enmascarar tráfico saliente
        oifname $WAN_IF masquerade
    }
}
```

#### Comandos de Verificación

```bash
# Verificar reglas cargadas
sudo nft list ruleset

# Habilitar reenvío de paquetes IP
sudo sysctl -w net.ipv4.ip_forward=1

# Hacer permanente el reenvío
echo "net.ipv4.ip_forward = 1" | sudo tee /etc/sysctl.d/99-ip-forward.conf

# Verificar estado del reenvío
cat /proc/sys/net/ipv4/ip_forward

# Habilitar y arrancar nftables
sudo systemctl enable nftables
sudo systemctl start nftables

# Verificar estado
sudo systemctl status nftables
```

---

### 5.1.2. DNS Seguro: DNSSEC y DoT con systemd-resolved

**systemd-resolved** es el servicio de resolución DNS integrado en systemd, que soporta tanto DNSSEC como DoT de forma nativa.

#### Configuración de systemd-resolved

Edite el archivo `/etc/systemd/resolved.conf`:

```ini
# /etc/systemd/resolved.conf
# Configuración de DNS seguro para Debian 13 Trixie

[Resolve]
# Servidores DNS primarios con soporte DoT
# Formato: IP#nombre_servidor (el nombre se usa para verificar TLS)
DNS=9.9.9.9#dns.quad9.net 149.112.112.112#dns.quad9.net
FallbackDNS=1.1.1.1#cloudflare-dns.com 8.8.8.8#dns.google

# Dominios de búsqueda (opcional)
#Domains=ejemplo.local

# Habilitar DNSSEC
# yes: rechaza respuestas no firmadas
# allow-downgrade: acepta si el dominio no soporta DNSSEC
DNSSEC=yes

# Habilitar DNS over TLS
# yes: solo conexiones cifradas
# opportunistic: intenta cifrar, pero acepta sin cifrar si falla
DNSOverTLS=yes

# Modo de caché
Cache=yes

# No usar DNS del archivo /etc/resolv.conf tradicional
ReadEtcHosts=yes

# Multicast DNS (mDNS) deshabilitado por seguridad
MulticastDNS=no

# Link-Local Multicast Name Resolution deshabilitado
LLMNR=no
```

#### Configuración del enlace simbólico de resolv.conf

```bash
# Enlazar resolv.conf a systemd-resolved
sudo ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf

# Reiniciar el servicio
sudo systemctl restart systemd-resolved

# Habilitar en el arranque
sudo systemctl enable systemd-resolved
```

#### Comandos de Verificación DNS

```bash
# Verificar estado del servicio
sudo systemctl status systemd-resolved

# Ver configuración actual de DNS
resolvectl status

# Verificar que DoT está funcionando
resolvectl query ejemplo.com

# Comprobar DNSSEC de un dominio
resolvectl query --type=DNSKEY ejemplo.com

# Estadísticas de caché y consultas
resolvectl statistics

# Verificar conectividad DNS con DoT
sudo tcpdump -i eth0 port 853 -c 5

# Prueba de resolución con DNSSEC
dig +dnssec ejemplo.com

# Verificar que no hay fugas DNS (debe mostrar los DNS configurados)
resolvectl dns
```

---

### 5.1.3. VPN con WireGuard

**WireGuard** es un protocolo VPN que destaca por su simplicidad, velocidad y seguridad. Utiliza criptografía moderna (Curve25519, ChaCha20, Poly1305) y tiene una base de código muy reducida.

#### Instalación

```bash
# Instalar WireGuard
sudo apt update
sudo apt install wireguard wireguard-tools

# Verificar que el módulo del kernel está cargado
lsmod | grep wireguard
```

#### Generación de Claves

```bash
# Crear directorio con permisos restrictivos
sudo mkdir -p /etc/wireguard
sudo chmod 700 /etc/wireguard

# Generar par de claves para el servidor
wg genkey | sudo tee /etc/wireguard/server_private.key | wg pubkey | sudo tee /etc/wireguard/server_public.key

# Establecer permisos seguros para la clave privada
sudo chmod 600 /etc/wireguard/server_private.key

# Generar claves para un cliente
wg genkey | tee client_private.key | wg pubkey > client_public.key
```

#### Configuración del Servidor

Cree el archivo `/etc/wireguard/wg0.conf`:

```ini
# /etc/wireguard/wg0.conf
# Configuración del servidor WireGuard

[Interface]
# Dirección IP del servidor en la VPN
Address = 10.200.200.1/24

# Puerto de escucha UDP
ListenPort = 51820

# Clave privada del servidor (insertar contenido de server_private.key)
PrivateKey = CLAVE_PRIVADA_SERVIDOR_AQUI

# Reglas de firewall automáticas (opcional)
PostUp = nft add rule inet filter input udp dport 51820 accept
PostUp = nft add rule inet filter forward iifname wg0 accept
PostDown = nft delete rule inet filter input udp dport 51820 accept
PostDown = nft delete rule inet filter forward iifname wg0 accept

# Guardar configuración al apagar
SaveConfig = false

# --- Clientes (Peers) ---

[Peer]
# Nombre descriptivo: Cliente-Laptop
# Clave pública del cliente
PublicKey = CLAVE_PUBLICA_CLIENTE_AQUI

# IP permitida para este cliente
AllowedIPs = 10.200.200.2/32

# Mantener conexión activa (útil para NAT)
PersistentKeepalive = 25
```

#### Configuración del Cliente

Cree el archivo en el dispositivo cliente:

```ini
# /etc/wireguard/wg0.conf (cliente)
# Configuración del cliente WireGuard

[Interface]
# Dirección IP del cliente en la VPN
Address = 10.200.200.2/24

# Clave privada del cliente
PrivateKey = CLAVE_PRIVADA_CLIENTE_AQUI

# DNS a usar cuando la VPN está activa
DNS = 10.200.200.1

[Peer]
# Clave pública del servidor
PublicKey = CLAVE_PUBLICA_SERVIDOR_AQUI

# Dirección pública del servidor
Endpoint = servidor.ejemplo.com:51820

# Rutas a enviar por la VPN
# 0.0.0.0/0 = todo el tráfico (full tunnel)
# 10.200.200.0/24 = solo tráfico de la VPN (split tunnel)
AllowedIPs = 10.200.200.0/24, 192.168.20.0/24

# Mantener conexión activa
PersistentKeepalive = 25
```

#### Comandos de Gestión y Verificación

```bash
# Iniciar la interfaz VPN
sudo wg-quick up wg0

# Detener la interfaz VPN
sudo wg-quick down wg0

# Habilitar inicio automático
sudo systemctl enable wg-quick@wg0

# Ver estado de la conexión
sudo wg show

# Ver estado detallado
sudo wg show wg0

# Verificar que la interfaz está activa
ip addr show wg0

# Probar conectividad
ping 10.200.200.1

# Ver tráfico en tiempo real
sudo wg show wg0 transfer

# Verificar rutas
ip route | grep wg0
```

---

## 5.2. SSH Hardening Moderno (OpenSSH 10+)

### 5.2.1. Eliminación de Claves DSA, Uso de Ed25519

Las claves **DSA** fueron deshabilitadas por defecto en OpenSSH 7.0 y eliminadas completamente en versiones recientes debido a vulnerabilidades conocidas. **Ed25519** es el algoritmo recomendado actualmente por ofrecer:

- Mayor seguridad con claves más pequeñas (256 bits vs 3072+ bits de RSA)
- Rendimiento superior en generación y verificación
- Resistencia a varios tipos de ataques de canal lateral

#### Generación de Claves Ed25519

```bash
# Generar nueva clave Ed25519 con comentario descriptivo
ssh-keygen -t ed25519 -C "usuario@hostname-$(date +%Y%m%d)" -f ~/.ssh/id_ed25519

# Opción con más rondas de derivación (más seguro, más lento)
ssh-keygen -t ed25519 -a 100 -C "usuario@servidor-produccion" -f ~/.ssh/id_ed25519_produccion

# Verificar la clave generada
ssh-keygen -l -f ~/.ssh/id_ed25519.pub

# Si necesita compatibilidad con sistemas antiguos, RSA 4096 es aceptable
ssh-keygen -t rsa -b 4096 -C "usuario@legacy-$(date +%Y%m%d)" -f ~/.ssh/id_rsa_legacy
```

#### Migración desde Claves Antiguas

```bash
# Listar claves existentes
ls -la ~/.ssh/

# Identificar y eliminar claves DSA (inseguras)
rm ~/.ssh/id_dsa ~/.ssh/id_dsa.pub 2>/dev/null

# Verificar algoritmos de claves existentes
for key in ~/.ssh/id_*; do
    [[ -f "$key" && ! "$key" =~ \.pub$ ]] && ssh-keygen -l -f "$key"
done

# Copiar nueva clave pública al servidor
ssh-copy-id -i ~/.ssh/id_ed25519.pub usuario@servidor
```

#### Configuración del Servidor SSH

Edite el archivo `/etc/ssh/sshd_config`:

```bash
# /etc/ssh/sshd_config
# Configuración de seguridad SSH para Debian 13 Trixie
# OpenSSH 10+

# === CONFIGURACIÓN DE RED ===
Port 22
AddressFamily inet
ListenAddress 0.0.0.0
# Para IPv6 también: ListenAddress ::

# === ALGORITMOS Y CLAVES ===
# Solo claves de host seguras (eliminar DSA y ECDSA débil)
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key

# Algoritmos de intercambio de claves (solo seguros)
KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org

# Cifrados permitidos (solo AEAD)
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com

# Algoritmos MAC (solo encrypt-then-mac)
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# Algoritmos de clave pública aceptados
PubkeyAcceptedAlgorithms ssh-ed25519,ssh-ed25519-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-256

# Algoritmos de firma de CA
CASignatureAlgorithms ssh-ed25519,rsa-sha2-512,rsa-sha2-256

# === AUTENTICACIÓN ===
# Deshabilitar autenticación por contraseña
PasswordAuthentication no
PermitEmptyPasswords no

# Habilitar autenticación por clave pública
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys

# Deshabilitar métodos inseguros
ChallengeResponseAuthentication no
KerberosAuthentication no
GSSAPIAuthentication no
HostbasedAuthentication no

# === RESTRICCIONES DE ACCESO ===
# Deshabilitar acceso root directo
PermitRootLogin no

# Limitar usuarios permitidos (ajustar según necesidad)
AllowUsers admin operador
# AllowGroups ssh-users

# Número máximo de intentos de autenticación
MaxAuthTries 3

# Tiempo máximo para autenticación
LoginGraceTime 30

# Máximo de sesiones simultáneas
MaxSessions 3

# Máximo de conexiones no autenticadas
MaxStartups 3:50:10

# === SEGURIDAD ADICIONAL ===
# Deshabilitar reenvío de agente SSH
AllowAgentForwarding no

# Deshabilitar reenvío TCP (habilitar solo si necesario)
AllowTcpForwarding no

# Deshabilitar reenvío X11
X11Forwarding no

# Deshabilitar túneles
PermitTunnel no

# No permitir variables de entorno del cliente
PermitUserEnvironment no

# Usar separación de privilegios
UsePrivilegeSeparation sandbox

# Mostrar banner antes de autenticación
Banner /etc/ssh/banner.txt

# Mensaje post-autenticación
PrintMotd no
PrintLastLog yes

# Verificar permisos de archivos del usuario
StrictModes yes

# Intervalo de verificación de conexión activa
ClientAliveInterval 300
ClientAliveCountMax 2

# === LOGGING ===
SyslogFacility AUTH
LogLevel VERBOSE

# === SFTP ===
Subsystem sftp internal-sftp -l INFO

# Configuración específica para grupo sftp-only
Match Group sftp-only
    ForceCommand internal-sftp -l INFO
    ChrootDirectory /home/%u
    AllowTcpForwarding no
    X11Forwarding no
    PermitTunnel no
```

#### Regenerar Claves de Host

```bash
# Eliminar claves de host antiguas
sudo rm /etc/ssh/ssh_host_*

# Regenerar solo claves seguras
sudo ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ""
sudo ssh-keygen -t rsa -b 4096 -f /etc/ssh/ssh_host_rsa_key -N ""

# Ajustar permisos
sudo chmod 600 /etc/ssh/ssh_host_*_key
sudo chmod 644 /etc/ssh/ssh_host_*_key.pub
```

#### Comandos de Verificación SSH

```bash
# Verificar sintaxis de configuración
sudo sshd -t

# Ver configuración efectiva
sudo sshd -T

# Reiniciar servicio (mantener sesión actual abierta como respaldo)
sudo systemctl restart sshd

# Verificar estado
sudo systemctl status sshd

# Ver conexiones activas
ss -tnlp | grep ssh

# Probar conexión con verbosidad
ssh -v usuario@servidor

# Verificar algoritmos soportados por el servidor
ssh -Q cipher
ssh -Q mac
ssh -Q kex
ssh -Q key

# Auditar configuración SSH
sudo ssh-audit localhost
```

---

### 5.2.2. Configuración FIDO2/U2F para Acceso SSH

**FIDO2** y **U2F** permiten usar llaves de seguridad físicas (como YubiKey, SoloKey, o Nitrokey) para autenticación SSH, proporcionando un segundo factor imposible de robar remotamente.

#### Instalación de Dependencias

```bash
# Instalar librerías necesarias
sudo apt install libfido2-1 libfido2-dev libfido2-tools

# Verificar que el dispositivo es detectado
fido2-token -L
```

#### Configurar Reglas udev

Cree el archivo `/etc/udev/rules.d/70-fido2.rules`:

```bash
# /etc/udev/rules.d/70-fido2.rules
# Reglas udev para dispositivos FIDO2

# YubiKey
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", ATTRS{idVendor}=="1050", MODE="0660", GROUP="plugdev", TAG+="uaccess"

# SoloKey
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", ATTRS{idVendor}=="0483", MODE="0660", GROUP="plugdev", TAG+="uaccess"

# Nitrokey
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", ATTRS{idVendor}=="20a0", MODE="0660", GROUP="plugdev", TAG+="uaccess"

# Google Titan
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", ATTRS{idVendor}=="18d1", MODE="0660", GROUP="plugdev", TAG+="uaccess"
```

Aplicar reglas:

```bash
# Recargar reglas udev
sudo udevadm control --reload-rules
sudo udevadm trigger

# Añadir usuario al grupo plugdev
sudo usermod -aG plugdev $USER
```

#### Generar Clave SSH Respaldada por FIDO2

```bash
# Clave residente (almacenada en el dispositivo)
# Requiere PIN y toque físico
ssh-keygen -t ed25519-sk -O resident -O verify-required -C "fido2-$(date +%Y%m%d)" -f ~/.ssh/id_ed25519_sk

# Clave no residente (handle almacenado en disco)
# Solo requiere toque físico
ssh-keygen -t ed25519-sk -O no-touch-required -C "fido2-notoque" -f ~/.ssh/id_ed25519_sk_notoque

# Para compatibilidad con dispositivos más antiguos (ECDSA)
ssh-keygen -t ecdsa-sk -C "fido2-ecdsa-$(date +%Y%m%d)" -f ~/.ssh/id_ecdsa_sk
```

Las opciones disponibles son:
- `-O resident`: Almacena la clave en el dispositivo (recuperable)
- `-O verify-required`: Requiere PIN del dispositivo
- `-O no-touch-required`: No requiere toque físico (menos seguro)

#### Exportar Clave Residente

```bash
# Listar claves residentes en el dispositivo
ssh-keygen -K

# Esto crea archivos id_ed25519_sk_rk* en el directorio actual
```

#### Configuración del Servidor para FIDO2

Añadir al archivo `/etc/ssh/sshd_config`:

```bash
# Añadir soporte para claves FIDO2
PubkeyAcceptedAlgorithms ssh-ed25519,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com
```

#### Configuración del Cliente SSH

Edite `~/.ssh/config`:

```bash
# ~/.ssh/config
# Configuración del cliente SSH con FIDO2

Host servidor-seguro
    HostName servidor.ejemplo.com
    User admin
    IdentityFile ~/.ssh/id_ed25519_sk
    IdentitiesOnly yes
    # Requerir confirmación de usuario para el agente
    AddKeysToAgent confirm

Host *
    # Preferir claves Ed25519
    IdentityFile ~/.ssh/id_ed25519
    IdentityFile ~/.ssh/id_ed25519_sk
    # Verificar huella del servidor
    VisualHostKey yes
    # Algoritmos preferidos
    KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org
    Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
    MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
```

#### Verificación de FIDO2

```bash
# Verificar que el dispositivo está conectado
fido2-token -L

# Ver información del dispositivo
fido2-token -I /dev/hidraw0

# Listar credenciales residentes
fido2-token -L -r /dev/hidraw0

# Probar conexión SSH con FIDO2
ssh -v -i ~/.ssh/id_ed25519_sk usuario@servidor

# El sistema solicitará tocar la llave física
```

---

## 5.3. Servicios Web Seguros (nginx)

### 5.3.1. Cabeceras de Seguridad (CSP, HSTS)

Las **cabeceras de seguridad HTTP** instruyen a los navegadores sobre cómo manejar el contenido de forma segura. Son una capa de defensa esencial contra ataques como XSS, clickjacking y MIME-sniffing.

#### Configuración Principal de nginx

Cree el archivo `/etc/nginx/conf.d/security-headers.conf`:

```nginx
# /etc/nginx/conf.d/security-headers.conf
# Cabeceras de seguridad globales para nginx

# HSTS - Forzar HTTPS durante 1 año
# includeSubDomains: aplica a todos los subdominios
# preload: permite inclusión en listas de precarga de navegadores
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

# CSP - Política de Seguridad de Contenido
# Esta es una política estricta; ajustar según necesidades de la aplicación
add_header Content-Security-Policy "
    default-src 'self';
    script-src 'self' 'unsafe-inline' https://cdn.ejemplo.com;
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    img-src 'self' data: https:;
    font-src 'self' https://fonts.gstatic.com;
    connect-src 'self' https://api.ejemplo.com;
    frame-ancestors 'self';
    form-action 'self';
    base-uri 'self';
    upgrade-insecure-requests;
" always;

# X-Content-Type-Options - Prevenir MIME-sniffing
add_header X-Content-Type-Options "nosniff" always;

# X-Frame-Options - Prevenir clickjacking (redundante con CSP frame-ancestors)
add_header X-Frame-Options "SAMEORIGIN" always;

# X-XSS-Protection - Filtro XSS del navegador (legacy, deshabilitado en navegadores modernos)
add_header X-XSS-Protection "0" always;

# Referrer-Policy - Controlar información de referencia enviada
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Permissions-Policy - Controlar APIs del navegador
add_header Permissions-Policy "
    accelerometer=(),
    camera=(),
    geolocation=(),
    gyroscope=(),
    magnetometer=(),
    microphone=(),
    payment=(),
    usb=()
" always;

# Cross-Origin-Embedder-Policy
add_header Cross-Origin-Embedder-Policy "require-corp" always;

# Cross-Origin-Opener-Policy
add_header Cross-Origin-Opener-Policy "same-origin" always;

# Cross-Origin-Resource-Policy
add_header Cross-Origin-Resource-Policy "same-origin" always;
```

#### Explicación de Directivas CSP Principales

| Directiva | Propósito |
|-----------|-----------|
| `default-src` | Política por defecto para todos los recursos |
| `script-src` | Orígenes permitidos para JavaScript |
| `style-src` | Orígenes permitidos para CSS |
| `img-src` | Orígenes permitidos para imágenes |
| `connect-src` | Orígenes para conexiones (fetch, WebSocket) |
| `frame-ancestors` | Quién puede incrustar la página en iframe |
| `form-action` | Destinos permitidos para formularios |
| `upgrade-insecure-requests` | Convertir HTTP a HTTPS automáticamente |

---

### 5.3.2. TLS 1.3 y Ocultación de Versión

**TLS 1.3** es la versión más reciente del protocolo, que elimina algoritmos obsoletos y reduce la latencia de conexión.

#### Configuración Completa del Servidor nginx

Cree el archivo `/etc/nginx/sites-available/ejemplo-seguro`:

```nginx
# /etc/nginx/sites-available/ejemplo-seguro
# Configuración de servidor nginx con TLS 1.3

# Redirigir HTTP a HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name ejemplo.com www.ejemplo.com;

    # Redirigir todo el tráfico a HTTPS
    return 301 https://$host$request_uri;
}

# Servidor HTTPS principal
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;

    server_name ejemplo.com www.ejemplo.com;

    # === OCULTAR INFORMACIÓN DEL SERVIDOR ===
    server_tokens off;

    # Eliminar cabecera Server (requiere módulo headers-more)
    # more_clear_headers Server;

    # === CERTIFICADOS TLS ===
    ssl_certificate /etc/letsencrypt/live/ejemplo.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ejemplo.com/privkey.pem;

    # Certificado de cadena para OCSP Stapling
    ssl_trusted_certificate /etc/letsencrypt/live/ejemplo.com/chain.pem;

    # === CONFIGURACIÓN TLS ===
    # Solo TLS 1.3 (o incluir 1.2 para compatibilidad)
    ssl_protocols TLSv1.3 TLSv1.2;

    # Preferir cifrados del servidor
    ssl_prefer_server_ciphers off;

    # Cifrados para TLS 1.2 (TLS 1.3 usa sus propios)
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;

    # Curvas elípticas permitidas
    ssl_ecdh_curve X25519:secp384r1;

    # Parámetros DH personalizados (generar con: openssl dhparam -out /etc/nginx/dhparam.pem 4096)
    ssl_dhparam /etc/nginx/dhparam.pem;

    # === SESIONES TLS ===
    # Caché de sesiones compartida
    ssl_session_cache shared:TLS:10m;
    ssl_session_timeout 1d;

    # Deshabilitar tickets de sesión (mejor seguridad)
    ssl_session_tickets off;

    # === OCSP STAPLING ===
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 9.9.9.9 149.112.112.112 valid=300s;
    resolver_timeout 5s;

    # === CABECERAS DE SEGURIDAD ===
    include /etc/nginx/conf.d/security-headers.conf;

    # === RAÍZ Y LOGS ===
    root /var/www/ejemplo.com/html;
    index index.html index.htm;

    access_log /var/log/nginx/ejemplo.com.access.log;
    error_log /var/log/nginx/ejemplo.com.error.log warn;

    # === UBICACIONES ===
    location / {
        try_files $uri $uri/ =404;
    }

    # Bloquear archivos ocultos
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    # Seguridad para archivos sensibles
    location ~* \.(git|env|htaccess|htpasswd|ini|log|sh|sql|conf)$ {
        deny all;
    }
}
```

#### Generar Parámetros DH Seguros

```bash
# Generar parámetros Diffie-Hellman (puede tardar varios minutos)
sudo openssl dhparam -out /etc/nginx/dhparam.pem 4096
sudo chmod 600 /etc/nginx/dhparam.pem
```

#### Comandos de Verificación nginx

```bash
# Verificar sintaxis de configuración
sudo nginx -t

# Recargar configuración
sudo systemctl reload nginx

# Ver estado del servicio
sudo systemctl status nginx

# Verificar módulos compilados
nginx -V 2>&1 | grep -o 'with-[^ ]*' | sort

# Verificar puertos en escucha
ss -tlnp | grep nginx

# Probar configuración TLS con OpenSSL
openssl s_client -connect ejemplo.com:443 -tls1_3

# Verificar certificado
openssl s_client -connect ejemplo.com:443 -servername ejemplo.com 2>/dev/null | openssl x509 -noout -dates

# Verificar OCSP Stapling
openssl s_client -connect ejemplo.com:443 -status 2>/dev/null | grep -A 10 "OCSP Response"

# Escanear con testssl.sh (herramienta externa)
# git clone --depth 1 https://github.com/drwetter/testssl.sh.git
# ./testssl.sh/testssl.sh https://ejemplo.com

# Verificar cabeceras de seguridad
curl -I https://ejemplo.com

# Comprobar HSTS
curl -sI https://ejemplo.com | grep -i strict

# Ver logs de acceso en tiempo real
sudo tail -f /var/log/nginx/ejemplo.com.access.log
```

---

## 5.4. Gestión de Paquetes y Vulnerabilidades

### 5.4.1. Formato deb822 (/etc/apt/sources.list.d/debian.sources)

El formato **deb822** es el nuevo estándar en Debian para configurar repositorios APT. Ofrece una sintaxis más clara y estructurada que el formato tradicional de una línea.

#### Migración al Formato deb822

```bash
# Respaldar configuración actual
sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup

# Crear nuevo archivo de fuentes
sudo touch /etc/apt/sources.list.d/debian.sources

# Vaciar el archivo antiguo (opcional, después de verificar)
# sudo truncate -s 0 /etc/apt/sources.list
```

#### Configuración de Repositorios

Cree el archivo `/etc/apt/sources.list.d/debian.sources`:

```yaml
# /etc/apt/sources.list.d/debian.sources
# Configuración de repositorios Debian 13 Trixie en formato deb822

# Repositorio principal de Debian
Types: deb deb-src
URIs: https://deb.debian.org/debian
Suites: trixie trixie-updates
Components: main contrib non-free non-free-firmware
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
Architectures: amd64

# Actualizaciones de seguridad
Types: deb deb-src
URIs: https://security.debian.org/debian-security
Suites: trixie-security
Components: main contrib non-free non-free-firmware
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
Architectures: amd64

# Repositorio Backports (versiones más recientes de software)
Types: deb deb-src
URIs: https://deb.debian.org/debian
Suites: trixie-backports
Components: main contrib non-free non-free-firmware
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
Architectures: amd64
```

#### Campos del Formato deb822

| Campo | Descripción |
|-------|-------------|
| `Types` | Tipo de paquetes: `deb` (binarios) y/o `deb-src` (fuentes) |
| `URIs` | URLs de los repositorios (puede incluir múltiples) |
| `Suites` | Nombres de las distribuciones o ramas |
| `Components` | Secciones del repositorio (main, contrib, non-free) |
| `Signed-By` | Ruta al archivo de clave GPG para verificación |
| `Architectures` | Arquitecturas de CPU (amd64, arm64, i386) |
| `Enabled` | `yes` o `no` para activar/desactivar el repositorio |

#### Añadir Repositorio de Terceros (Ejemplo)

```yaml
# /etc/apt/sources.list.d/docker.sources
# Repositorio oficial de Docker

Types: deb
URIs: https://download.docker.com/linux/debian
Suites: trixie
Components: stable
Signed-By: /usr/share/keyrings/docker-archive-keyring.gpg
Architectures: amd64
```

Descargar la clave GPG:

```bash
# Descargar y almacenar clave GPG
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Verificar permisos
sudo chmod 644 /usr/share/keyrings/docker-archive-keyring.gpg
```

#### Verificación de Repositorios

```bash
# Actualizar lista de paquetes
sudo apt update

# Verificar que no hay errores
apt-cache policy

# Ver repositorios configurados
apt-cache policy | grep -E '^\s*(release|origin)'

# Listar paquetes de un repositorio específico
apt list --upgradable 2>/dev/null

# Verificar firmas de paquetes
apt-key list 2>/dev/null  # Método legacy
gpg --list-keys --keyring /usr/share/keyrings/debian-archive-keyring.gpg
```

---

### 5.4.2. unattended-upgrades y apt-listbugs

**unattended-upgrades** automatiza la instalación de actualizaciones de seguridad, mientras que **apt-listbugs** advierte sobre bugs conocidos antes de instalar paquetes.

#### Instalación

```bash
# Instalar herramientas
sudo apt install unattended-upgrades apt-listbugs apt-listchanges needrestart

# Configurar automáticamente
sudo dpkg-reconfigure -plow unattended-upgrades
```

#### Configuración de unattended-upgrades

Edite el archivo `/etc/apt/apt.conf.d/50unattended-upgrades`:

```bash
# /etc/apt/apt.conf.d/50unattended-upgrades
# Configuración de actualizaciones automáticas

// Orígenes permitidos para actualizaciones automáticas
Unattended-Upgrade::Origins-Pattern {
    // Actualizaciones de seguridad de Debian
    "origin=Debian,codename=${distro_codename}-security,label=Debian-Security";

    // Actualizaciones estables de Debian
    "origin=Debian,codename=${distro_codename},label=Debian";

    // Actualizaciones del sistema
    "origin=Debian,codename=${distro_codename}-updates,label=Debian";
};

// Paquetes a NO actualizar automáticamente (lista negra)
Unattended-Upgrade::Package-Blacklist {
    // "linux-image";
    // "linux-headers";
    // "nginx";
};

// Opciones de correo electrónico
Unattended-Upgrade::Mail "admin@ejemplo.com";
Unattended-Upgrade::MailReport "on-change";

// Eliminar dependencias no utilizadas automáticamente
Unattended-Upgrade::Remove-Unused-Dependencies "true";

// Eliminar kernels no utilizados
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";

// Reiniciar automáticamente si es necesario (usar con precaución)
Unattended-Upgrade::Automatic-Reboot "false";

// Si se habilita reinicio automático, hora preferida
Unattended-Upgrade::Automatic-Reboot-Time "03:00";

// Limitar ancho de banda de descarga (KB/s, 0 = ilimitado)
Acquire::http::Dl-Limit "0";

// Registro detallado
Unattended-Upgrade::Verbose "true";

// Modo de prueba (solo simular, no instalar)
// Unattended-Upgrade::Dry-Run "true";

// No interrumpir aplicaciones dpkg en ejecución
Unattended-Upgrade::InstallOnShutdown "false";

// Solo actualizar si hay suficiente espacio en disco (MB)
Unattended-Upgrade::MinimalSteps "true";
```

#### Configuración de Periodicidad

Edite el archivo `/etc/apt/apt.conf.d/20auto-upgrades`:

```bash
# /etc/apt/apt.conf.d/20auto-upgrades
# Periodicidad de actualizaciones automáticas

// Actualizar lista de paquetes diariamente
APT::Periodic::Update-Package-Lists "1";

// Descargar paquetes actualizables diariamente
APT::Periodic::Download-Upgradeable-Packages "1";

// Ejecutar actualizaciones automáticas diariamente
APT::Periodic::Unattended-Upgrade "1";

// Limpiar caché de paquetes cada 7 días
APT::Periodic::AutocleanInterval "7";
```

#### Configuración de apt-listbugs

Edite el archivo `/etc/apt/apt.conf.d/10apt-listbugs`:

```bash
# /etc/apt/apt.conf.d/10apt-listbugs
# Configuración de apt-listbugs

// Severidad mínima para mostrar bugs
Apt::Listbugs::Severities "critical,grave,serious";

// Acción al encontrar bugs (ask, ignore, both)
Apt::Listbugs::Action "ask";
```

#### Comandos de Verificación y Gestión

```bash
# Verificar configuración de actualizaciones automáticas
apt-config dump | grep -i unattended

# Ejecutar actualización manual en modo prueba
sudo unattended-upgrade --dry-run --debug

# Ejecutar actualización real
sudo unattended-upgrade -v

# Ver logs de actualizaciones automáticas
sudo cat /var/log/unattended-upgrades/unattended-upgrades.log

# Verificar estado del servicio
sudo systemctl status unattended-upgrades

# Ver bugs conocidos para un paquete
apt-listbugs list nombre-paquete

# Verificar si hay reinicios pendientes
sudo needrestart -r l

# Listar servicios que necesitan reinicio
sudo needrestart -b

# Ver actualizaciones pendientes
apt list --upgradable
```

---

## 5.5. Monitorización y Logs

### 5.5.1. journald (Logs Firmados) y auditd

#### Configuración de journald con Logs Firmados

**journald** puede firmar criptográficamente los logs para detectar manipulaciones. Esta característica utiliza FSS (Forward Secure Sealing).

Edite el archivo `/etc/systemd/journald.conf`:

```ini
# /etc/systemd/journald.conf
# Configuración de journald con logs firmados

[Journal]
# Almacenamiento persistente de logs
Storage=persistent

# Comprimir logs
Compress=yes

# Habilitar sellado criptográfico (Forward Secure Sealing)
Seal=yes

# Dividir logs por usuario
SplitMode=uid

# Sincronizar al disco cada 5 minutos
SyncIntervalSec=5m

# Límites de tamaño
SystemMaxUse=2G
SystemKeepFree=1G
SystemMaxFileSize=128M
SystemMaxFiles=100

# Límites para logs de usuario
RuntimeMaxUse=256M
RuntimeKeepFree=128M
RuntimeMaxFileSize=32M

# Nivel mínimo de log
MaxLevelStore=debug
MaxLevelSyslog=debug
MaxLevelKMsg=warning
MaxLevelConsole=info

# Tasa de limitación de mensajes
RateLimitIntervalSec=30s
RateLimitBurst=10000

# Reenviar a syslog (si se usa rsyslog también)
ForwardToSyslog=no
ForwardToKMsg=no
ForwardToConsole=no
ForwardToWall=yes
```

#### Configurar Sellado FSS

```bash
# Generar claves de sellado FSS
sudo journalctl --setup-keys

# Esto genera:
# - Una clave de verificación (guardar fuera del sistema)
# - Las claves de sellado se rotan automáticamente

# Verificar integridad de logs
sudo journalctl --verify

# Ver clave de verificación
sudo journalctl --verify-key
```

#### Configuración de auditd

Instalar y configurar auditd:

```bash
# Instalar auditd
sudo apt install auditd audispd-plugins

# Habilitar servicio
sudo systemctl enable auditd
sudo systemctl start auditd
```

Edite el archivo `/etc/audit/auditd.conf`:

```ini
# /etc/audit/auditd.conf
# Configuración principal de auditd

# Archivo de log
log_file = /var/log/audit/audit.log
log_group = adm
log_format = ENRICHED

# Rotación de logs
max_log_file = 50
num_logs = 5
max_log_file_action = ROTATE

# Comportamiento cuando el disco está lleno
space_left = 100
space_left_action = SYSLOG
admin_space_left = 50
admin_space_left_action = SUSPEND
disk_full_action = SUSPEND
disk_error_action = SUSPEND

# Flush de escritura
flush = INCREMENTAL_ASYNC
freq = 50

# Prioridad del demonio
priority_boost = 4

# Tamaño del buffer
name_format = HOSTNAME
name = debian-server
```

#### Reglas de Auditoría

Cree el archivo `/etc/audit/rules.d/security.rules`:

```bash
# /etc/audit/rules.d/security.rules
# Reglas de auditoría de seguridad para Debian 13

# Eliminar reglas anteriores
-D

# Aumentar buffer de auditoría
-b 8192

# Hacer reglas inmutables (requiere reinicio para cambiar)
# Descomentar en producción:
# -e 2

# === MONITOREO DE ARCHIVOS CRÍTICOS ===

# Cambios en passwd, shadow, group
-w /etc/passwd -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/gshadow -p wa -k identity

# Cambios en sudoers
-w /etc/sudoers -p wa -k sudoers
-w /etc/sudoers.d/ -p wa -k sudoers

# Cambios en configuración SSH
-w /etc/ssh/sshd_config -p wa -k sshd_config
-w /etc/ssh/ssh_config -p wa -k ssh_config

# Cambios en PAM
-w /etc/pam.d/ -p wa -k pam

# Cambios en cron
-w /etc/crontab -p wa -k cron
-w /etc/cron.d/ -p wa -k cron
-w /var/spool/cron/ -p wa -k cron

# Cambios en systemd
-w /etc/systemd/ -p wa -k systemd

# Cambios en configuración de red
-w /etc/hosts -p wa -k network
-w /etc/network/ -p wa -k network
-w /etc/netplan/ -p wa -k network

# === LLAMADAS AL SISTEMA CRÍTICAS ===

# Cambios de tiempo del sistema
-a always,exit -F arch=b64 -S adjtimex -S settimeofday -S clock_settime -k time_change

# Creación y eliminación de usuarios/grupos
-a always,exit -F arch=b64 -S setuid -S setgid -S setreuid -S setregid -k identity_change

# Montaje de sistemas de archivos
-a always,exit -F arch=b64 -S mount -S umount2 -k mounts

# Eliminación de archivos
-a always,exit -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -k file_deletion

# Modificación de atributos de archivos
-a always,exit -F arch=b64 -S chmod -S fchmod -S fchmodat -k file_permission
-a always,exit -F arch=b64 -S chown -S fchown -S fchownat -S lchown -k file_ownership

# Uso de privilegios
-a always,exit -F arch=b64 -S execve -C uid!=euid -F key=privilege_escalation

# === ACCESO A ARCHIVOS SENSIBLES ===

# Acceso a claves privadas SSH
-w /etc/ssh/ -p r -k ssh_keys

# Acceso a certificados
-w /etc/ssl/private/ -p r -k ssl_keys

# === COMANDOS ESPECÍFICOS ===

# Uso de comandos de administración
-w /usr/bin/passwd -p x -k passwd_cmd
-w /usr/bin/sudo -p x -k sudo_cmd
-w /usr/bin/su -p x -k su_cmd
-w /usr/sbin/useradd -p x -k user_management
-w /usr/sbin/userdel -p x -k user_management
-w /usr/sbin/usermod -p x -k user_management
-w /usr/sbin/groupadd -p x -k group_management
-w /usr/sbin/groupdel -p x -k group_management
-w /usr/sbin/groupmod -p x -k group_management

# Herramientas de red
-w /usr/bin/ssh -p x -k network_tools
-w /usr/bin/scp -p x -k network_tools
-w /usr/bin/wget -p x -k network_tools
-w /usr/bin/curl -p x -k network_tools
```

Cargar las reglas:

```bash
# Cargar reglas
sudo augenrules --load

# Verificar reglas cargadas
sudo auditctl -l

# Ver estado de auditd
sudo auditctl -s
```

#### Comandos de Verificación de Logs

```bash
# === JOURNALD ===

# Ver logs del sistema
sudo journalctl -xe

# Ver logs de un servicio específico
sudo journalctl -u nginx.service

# Ver logs desde el último arranque
sudo journalctl -b

# Ver logs en tiempo real
sudo journalctl -f

# Filtrar por prioridad (0-7, 0=emergencia)
sudo journalctl -p err

# Filtrar por fecha
sudo journalctl --since "2024-01-01" --until "2024-01-02"

# Verificar integridad de logs firmados
sudo journalctl --verify

# Ver espacio usado por logs
sudo journalctl --disk-usage

# Limpiar logs antiguos
sudo journalctl --vacuum-time=30d
sudo journalctl --vacuum-size=1G

# === AUDITD ===

# Ver eventos de auditoría recientes
sudo ausearch -ts recent

# Buscar eventos por clave
sudo ausearch -k identity

# Buscar eventos de un usuario
sudo ausearch -ua root

# Buscar eventos de un comando
sudo ausearch -c sudo

# Generar reporte de auditoría
sudo aureport

# Reporte de autenticaciones
sudo aureport -au

# Reporte de comandos ejecutados
sudo aureport -x

# Reporte de anomalías
sudo aureport --anomaly

# Ver estado del servicio
sudo systemctl status auditd
```

---

### 5.5.2. Alertas Básicas

#### Sistema de Alertas con Logwatch

```bash
# Instalar logwatch
sudo apt install logwatch

# Configurar logwatch
sudo cp /usr/share/logwatch/default.conf/logwatch.conf /etc/logwatch/conf/

# Editar configuración
sudo nano /etc/logwatch/conf/logwatch.conf
```

Configuración de `/etc/logwatch/conf/logwatch.conf`:

```ini
# /etc/logwatch/conf/logwatch.conf
# Configuración de Logwatch

# Enviar por correo
Output = mail
MailTo = admin@ejemplo.com
MailFrom = logwatch@ejemplo.com

# Nivel de detalle (0-10)
Detail = Med

# Rango de logs a analizar
Range = yesterday

# Formato de salida
Format = html

# Servicios a monitorear
Service = All
Service = -zz-network
Service = -zz-sys
```

#### Script de Alertas Personalizadas

Cree el archivo `/usr/local/bin/alertas-seguridad.sh`:

```bash
#!/bin/bash
# /usr/local/bin/alertas-seguridad.sh
# Script de alertas de seguridad básicas

# Configuración
EMAIL="admin@ejemplo.com"
HOSTNAME=$(hostname)
LOG_FILE="/var/log/alertas-seguridad.log"

# Función de envío de alerta
enviar_alerta() {
    local asunto="$1"
    local mensaje="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    echo "[$timestamp] ALERTA: $asunto" >> "$LOG_FILE"

    # Enviar por correo (requiere mailutils o msmtp)
    echo -e "Servidor: $HOSTNAME\nFecha: $timestamp\n\n$mensaje" | \
        mail -s "[ALERTA] $asunto - $HOSTNAME" "$EMAIL"
}

# Verificar intentos de SSH fallidos
ssh_fallidos=$(journalctl -u ssh --since "1 hour ago" | grep -c "Failed password")
if [ "$ssh_fallidos" -gt 10 ]; then
    enviar_alerta "Múltiples intentos SSH fallidos" \
        "Se detectaron $ssh_fallidos intentos de acceso SSH fallidos en la última hora."
fi

# Verificar uso de disco
uso_disco=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$uso_disco" -gt 90 ]; then
    enviar_alerta "Disco casi lleno" \
        "El disco raíz está al ${uso_disco}% de capacidad."
fi

# Verificar carga del sistema
carga=$(uptime | awk -F'load average:' '{print $2}' | cut -d',' -f1 | tr -d ' ')
cpus=$(nproc)
umbral=$(echo "$cpus * 2" | bc)
if (( $(echo "$carga > $umbral" | bc -l) )); then
    enviar_alerta "Carga del sistema alta" \
        "La carga del sistema ($carga) supera el umbral ($umbral)."
fi

# Verificar servicios críticos
for servicio in ssh nginx; do
    if ! systemctl is-active --quiet "$servicio"; then
        enviar_alerta "Servicio $servicio caído" \
            "El servicio $servicio no está activo."
    fi
done

# Verificar cambios en archivos críticos (usando auditd)
cambios_passwd=$(ausearch -k identity --start recent 2>/dev/null | grep -c "type=SYSCALL")
if [ "$cambios_passwd" -gt 0 ]; then
    enviar_alerta "Cambios en archivos de identidad" \
        "Se detectaron $cambios_passwd cambios en archivos de identidad del sistema."
fi

# Verificar usuarios con UID 0 (además de root)
usuarios_uid0=$(awk -F: '$3 == 0 && $1 != "root" {print $1}' /etc/passwd)
if [ -n "$usuarios_uid0" ]; then
    enviar_alerta "Usuarios con UID 0 detectados" \
        "Usuarios con UID 0 además de root: $usuarios_uid0"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Verificación completada" >> "$LOG_FILE"
```

Configurar permisos y cron:

```bash
# Dar permisos de ejecución
sudo chmod +x /usr/local/bin/alertas-seguridad.sh

# Añadir a cron (cada hora)
echo "0 * * * * root /usr/local/bin/alertas-seguridad.sh" | sudo tee /etc/cron.d/alertas-seguridad

# Verificar cron
sudo crontab -l
```

---

## 5.6. Copias de Seguridad 3-2-1 Cifradas

La **estrategia 3-2-1** es una metodología probada para copias de seguridad:
- **3** copias de los datos importantes
- **2** tipos diferentes de medios de almacenamiento
- **1** copia almacenada fuera del sitio (offsite)

### Implementación con Restic

**Restic** es una herramienta de backup moderna que soporta cifrado, deduplicación y múltiples backends de almacenamiento.

#### Instalación

```bash
# Instalar restic
sudo apt install restic

# Verificar versión
restic version
```

#### Inicializar Repositorios

```bash
# Variables de entorno para la contraseña
export RESTIC_PASSWORD="contraseña-segura-compleja"

# 1. Repositorio local (disco externo)
sudo restic init --repo /mnt/backup-local

# 2. Repositorio remoto (servidor SSH)
sudo restic init --repo sftp:usuario@backup-server:/backups/$(hostname)

# 3. Repositorio en la nube (S3 compatible)
export AWS_ACCESS_KEY_ID="tu-access-key"
export AWS_SECRET_ACCESS_KEY="tu-secret-key"
sudo restic init --repo s3:s3.ejemplo.com/bucket-backup/$(hostname)
```

#### Script de Backup Automatizado

Cree el archivo `/usr/local/bin/backup-321.sh`:

```bash
#!/bin/bash
# /usr/local/bin/backup-321.sh
# Script de backup 3-2-1 cifrado con restic

set -e

# === CONFIGURACIÓN ===
HOSTNAME=$(hostname)
LOG_FILE="/var/log/backup-321.log"
EMAIL="admin@ejemplo.com"

# Repositorios (contraseña desde archivo seguro)
export RESTIC_PASSWORD_FILE="/root/.restic-password"
REPO_LOCAL="/mnt/backup-local"
REPO_REMOTO="sftp:backup@backup-server:/backups/$HOSTNAME"
REPO_CLOUD="s3:s3.amazonaws.com/mi-bucket-backup/$HOSTNAME"

# Directorios a respaldar
BACKUP_DIRS="/etc /home /var/www /var/lib/postgresql /root"

# Directorios a excluir
EXCLUDE_DIRS="
--exclude=/home/*/.cache
--exclude=/home/*/.local/share/Trash
--exclude=/var/www/*/node_modules
--exclude=/var/www/*/vendor
--exclude=*.tmp
--exclude=*.log
"

# Retención de snapshots
RETENTION="--keep-daily 7 --keep-weekly 4 --keep-monthly 12 --keep-yearly 3"

# === FUNCIONES ===

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

enviar_notificacion() {
    local estado="$1"
    local mensaje="$2"
    echo -e "Estado: $estado\nServidor: $HOSTNAME\n\n$mensaje" | \
        mail -s "[BACKUP] $estado - $HOSTNAME" "$EMAIL"
}

verificar_repositorio() {
    local repo="$1"
    local nombre="$2"

    if restic -r "$repo" snapshots &>/dev/null; then
        log "Repositorio $nombre: OK"
        return 0
    else
        log "ERROR: Repositorio $nombre no accesible"
        return 1
    fi
}

hacer_backup() {
    local repo="$1"
    local nombre="$2"

    log "Iniciando backup a $nombre..."

    if restic -r "$repo" backup $BACKUP_DIRS $EXCLUDE_DIRS \
        --tag "$(date +%Y%m%d)" --tag "automatico"; then
        log "Backup a $nombre completado"
        return 0
    else
        log "ERROR: Backup a $nombre falló"
        return 1
    fi
}

limpiar_snapshots() {
    local repo="$1"
    local nombre="$2"

    log "Limpiando snapshots antiguos en $nombre..."

    if restic -r "$repo" forget $RETENTION --prune; then
        log "Limpieza de $nombre completada"
        return 0
    else
        log "ERROR: Limpieza de $nombre falló"
        return 1
    fi
}

verificar_integridad() {
    local repo="$1"
    local nombre="$2"

    log "Verificando integridad de $nombre..."

    if restic -r "$repo" check; then
        log "Integridad de $nombre: OK"
        return 0
    else
        log "ERROR: Problemas de integridad en $nombre"
        return 1
    fi
}

# === EJECUCIÓN PRINCIPAL ===

log "========== INICIO BACKUP 3-2-1 =========="

errores=0
resumen=""

# Copia 1: Local
if verificar_repositorio "$REPO_LOCAL" "LOCAL"; then
    if hacer_backup "$REPO_LOCAL" "LOCAL"; then
        limpiar_snapshots "$REPO_LOCAL" "LOCAL"
        resumen+="LOCAL: OK\n"
    else
        ((errores++))
        resumen+="LOCAL: ERROR en backup\n"
    fi
else
    ((errores++))
    resumen+="LOCAL: NO DISPONIBLE\n"
fi

# Copia 2: Remoto (SSH)
if verificar_repositorio "$REPO_REMOTO" "REMOTO"; then
    if hacer_backup "$REPO_REMOTO" "REMOTO"; then
        limpiar_snapshots "$REPO_REMOTO" "REMOTO"
        resumen+="REMOTO: OK\n"
    else
        ((errores++))
        resumen+="REMOTO: ERROR en backup\n"
    fi
else
    ((errores++))
    resumen+="REMOTO: NO DISPONIBLE\n"
fi

# Copia 3: Cloud (offsite)
if verificar_repositorio "$REPO_CLOUD" "CLOUD"; then
    if hacer_backup "$REPO_CLOUD" "CLOUD"; then
        limpiar_snapshots "$REPO_CLOUD" "CLOUD"
        resumen+="CLOUD: OK\n"
    else
        ((errores++))
        resumen+="CLOUD: ERROR en backup\n"
    fi
else
    ((errores++))
    resumen+="CLOUD: NO DISPONIBLE\n"
fi

# Verificación semanal de integridad (solo domingos)
if [ "$(date +%u)" -eq 7 ]; then
    log "Verificación semanal de integridad..."
    verificar_integridad "$REPO_LOCAL" "LOCAL"
fi

log "========== FIN BACKUP 3-2-1 =========="

# Enviar notificación
if [ $errores -eq 0 ]; then
    enviar_notificacion "EXITOSO" "Todas las copias completadas:\n$resumen"
else
    enviar_notificacion "ERROR ($errores fallos)" "Resumen:\n$resumen\nRevisar $LOG_FILE"
fi

exit $errores
```

#### Configuración de Permisos y Cron

```bash
# Crear archivo de contraseña seguro
echo "contraseña-muy-segura-y-larga" | sudo tee /root/.restic-password
sudo chmod 600 /root/.restic-password

# Dar permisos al script
sudo chmod 700 /usr/local/bin/backup-321.sh

# Programar backup diario a las 2:00 AM
echo "0 2 * * * root /usr/local/bin/backup-321.sh" | sudo tee /etc/cron.d/backup-321
```

#### Comandos de Gestión de Backups

```bash
# Configurar contraseña
export RESTIC_PASSWORD_FILE="/root/.restic-password"

# Listar snapshots
sudo restic -r /mnt/backup-local snapshots

# Ver contenido de un snapshot
sudo restic -r /mnt/backup-local ls latest

# Restaurar archivos específicos
sudo restic -r /mnt/backup-local restore latest --target /tmp/restore --include "/etc/nginx"

# Restaurar snapshot completo
sudo restic -r /mnt/backup-local restore abc123 --target /

# Comparar dos snapshots
sudo restic -r /mnt/backup-local diff snapshot1 snapshot2

# Verificar integridad
sudo restic -r /mnt/backup-local check

# Ver estadísticas
sudo restic -r /mnt/backup-local stats

# Montar repositorio como sistema de archivos
sudo mkdir /mnt/restic-mount
sudo restic -r /mnt/backup-local mount /mnt/restic-mount
# Después de explorar:
sudo umount /mnt/restic-mount
```

---

## Checklist Nivel 4: Red, Servicios y Mantenimiento Avanzado

### 5.1 Arquitectura de Red y DNS

| # | Verificación | Comando | Estado Esperado |
|---|--------------|---------|-----------------|
| 1.1 | nftables está activo | `sudo systemctl is-active nftables` | `active` |
| 1.2 | Reenvío IP habilitado | `cat /proc/sys/net/ipv4/ip_forward` | `1` |
| 1.3 | Reglas de firewall cargadas | `sudo nft list ruleset \| grep -c "chain"` | `>= 3` |
| 1.4 | DMZ aislada de LAN | `sudo nft list ruleset \| grep "DMZ.*LAN.*drop"` | Regla presente |
| 1.5 | systemd-resolved activo | `sudo systemctl is-active systemd-resolved` | `active` |
| 1.6 | DNSSEC habilitado | `resolvectl status \| grep DNSSEC` | `DNSSEC setting: yes` |
| 1.7 | DoT habilitado | `resolvectl status \| grep DNSOverTLS` | `DNSOverTLS setting: yes` |
| 1.8 | Resolución DNS funciona | `resolvectl query google.com` | Respuesta exitosa |
| 1.9 | WireGuard instalado | `dpkg -l \| grep wireguard` | Paquete instalado |
| 1.10 | Clave privada WG con permisos | `stat -c %a /etc/wireguard/*.key` | `600` |
| 1.11 | Interfaz WG activa (si configurada) | `ip link show wg0` | Estado UP |

### 5.2 SSH Hardening

| # | Verificación | Comando | Estado Esperado |
|---|--------------|---------|-----------------|
| 2.1 | SSH escuchando | `ss -tlnp \| grep :22` | Puerto 22 activo |
| 2.2 | Sintaxis sshd válida | `sudo sshd -t` | Sin errores |
| 2.3 | Root login deshabilitado | `sudo sshd -T \| grep permitrootlogin` | `no` |
| 2.4 | Autenticación por contraseña deshabilitada | `sudo sshd -T \| grep passwordauthentication` | `no` |
| 2.5 | Solo claves Ed25519/RSA | `ls /etc/ssh/ssh_host_*_key` | Solo ed25519 y rsa |
| 2.6 | Sin claves DSA | `ls /etc/ssh/ssh_host_dsa_key 2>&1` | Archivo no existe |
| 2.7 | MaxAuthTries configurado | `sudo sshd -T \| grep maxauthtries` | `<= 3` |
| 2.8 | X11Forwarding deshabilitado | `sudo sshd -T \| grep x11forwarding` | `no` |
| 2.9 | Clave Ed25519 del usuario existe | `ls ~/.ssh/id_ed25519.pub` | Archivo existe |
| 2.10 | FIDO2 configurado (si aplica) | `ssh -Q key \| grep sk` | Algoritmos sk presentes |

### 5.3 Servicios Web (nginx)

| # | Verificación | Comando | Estado Esperado |
|---|--------------|---------|-----------------|
| 3.1 | nginx activo | `sudo systemctl is-active nginx` | `active` |
| 3.2 | Sintaxis nginx válida | `sudo nginx -t` | `syntax is ok` |
| 3.3 | TLS 1.3 habilitado | `nginx -T \| grep "ssl_protocols"` | Incluye `TLSv1.3` |
| 3.4 | server_tokens deshabilitado | `nginx -T \| grep "server_tokens"` | `off` |
| 3.5 | HSTS configurado | `curl -sI https://localhost \| grep -i strict` | Cabecera presente |
| 3.6 | CSP configurado | `curl -sI https://localhost \| grep -i content-security` | Cabecera presente |
| 3.7 | X-Content-Type-Options | `curl -sI https://localhost \| grep -i x-content-type` | `nosniff` |
| 3.8 | OCSP Stapling habilitado | `nginx -T \| grep ssl_stapling` | `on` |
| 3.9 | Parámetros DH existen | `ls /etc/nginx/dhparam.pem` | Archivo existe |
| 3.10 | Certificados válidos | `openssl s_client -connect localhost:443 2>/dev/null \| grep "Verify return code"` | `0 (ok)` |

### 5.4 Gestión de Paquetes

| # | Verificación | Comando | Estado Esperado |
|---|--------------|---------|-----------------|
| 4.1 | Formato deb822 configurado | `ls /etc/apt/sources.list.d/debian.sources` | Archivo existe |
| 4.2 | Repositorios accesibles | `sudo apt update 2>&1 \| grep -c "Err:"` | `0` |
| 4.3 | Claves GPG válidas | `apt-key list 2>&1 \| grep -c "expired"` | `0` |
| 4.4 | unattended-upgrades instalado | `dpkg -l \| grep unattended-upgrades` | Paquete instalado |
| 4.5 | Actualizaciones automáticas activas | `sudo systemctl is-enabled unattended-upgrades` | `enabled` |
| 4.6 | apt-listbugs instalado | `dpkg -l \| grep apt-listbugs` | Paquete instalado |
| 4.7 | Configuración de orígenes válida | `grep -c "Origins-Pattern" /etc/apt/apt.conf.d/50unattended-upgrades` | `>= 1` |
| 4.8 | Sin actualizaciones de seguridad pendientes | `sudo unattended-upgrade --dry-run 2>&1 \| grep -c "will be upgraded"` | `0` (idealmente) |

### 5.5 Monitorización y Logs

| # | Verificación | Comando | Estado Esperado |
|---|--------------|---------|-----------------|
| 5.1 | journald activo | `sudo systemctl is-active systemd-journald` | `active` |
| 5.2 | Almacenamiento persistente | `grep "^Storage" /etc/systemd/journald.conf` | `persistent` |
| 5.3 | FSS (sellado) habilitado | `grep "^Seal" /etc/systemd/journald.conf` | `yes` |
| 5.4 | Integridad de logs verificable | `sudo journalctl --verify 2>&1 \| grep -c "FAIL"` | `0` |
| 5.5 | auditd activo | `sudo systemctl is-active auditd` | `active` |
| 5.6 | Reglas de auditoría cargadas | `sudo auditctl -l \| grep -c "^-"` | `>= 10` |
| 5.7 | Monitoreo de /etc/passwd | `sudo auditctl -l \| grep passwd` | Regla presente |
| 5.8 | Monitoreo de sudo | `sudo auditctl -l \| grep sudo` | Regla presente |
| 5.9 | Logs de auditoría accesibles | `sudo ausearch -ts today \| head -1` | Sin errores |
| 5.10 | Script de alertas configurado | `ls /usr/local/bin/alertas-seguridad.sh` | Archivo existe |

### 5.6 Copias de Seguridad 3-2-1

| # | Verificación | Comando | Estado Esperado |
|---|--------------|---------|-----------------|
| 6.1 | restic instalado | `restic version` | Versión mostrada |
| 6.2 | Archivo de contraseña seguro | `stat -c %a /root/.restic-password` | `600` |
| 6.3 | Repositorio local inicializado | `sudo restic -r /mnt/backup-local snapshots 2>&1 \| grep -v "error"` | Lista de snapshots |
| 6.4 | Script de backup existe | `ls /usr/local/bin/backup-321.sh` | Archivo existe |
| 6.5 | Script con permisos correctos | `stat -c %a /usr/local/bin/backup-321.sh` | `700` |
| 6.6 | Cron de backup configurado | `cat /etc/cron.d/backup-321` | Tarea configurada |
| 6.7 | Al menos 3 copias (estrategia 3-2-1) | Verificar manual | 3 repositorios configurados |
| 6.8 | Último backup < 24h | `sudo restic -r /mnt/backup-local snapshots --latest 1 --json \| grep time` | Fecha reciente |
| 6.9 | Integridad del repositorio | `sudo restic -r /mnt/backup-local check` | Sin errores |
| 6.10 | Restauración funcional | Test manual de restauración | Archivos recuperables |

---

### Resumen de Comandos de Verificación Rápida

Ejecute este script para una verificación completa del Nivel 4:

```bash
#!/bin/bash
# /usr/local/bin/verificar-nivel4.sh
# Script de verificación rápida del Nivel 4

echo "=== VERIFICACIÓN NIVEL 4: Red, Servicios y Mantenimiento ==="
echo ""

# Colores
VERDE='\033[0;32m'
ROJO='\033[0;31m'
AMARILLO='\033[1;33m'
NC='\033[0m'

verificar() {
    local descripcion="$1"
    local comando="$2"
    local esperado="$3"

    resultado=$(eval "$comando" 2>/dev/null)

    if [[ "$resultado" == *"$esperado"* ]] || [[ "$resultado" -ge "$esperado" ]] 2>/dev/null; then
        echo -e "[${VERDE}OK${NC}] $descripcion"
        return 0
    else
        echo -e "[${ROJO}FALLO${NC}] $descripcion (obtenido: $resultado)"
        return 1
    fi
}

echo "--- Servicios de Red ---"
verificar "nftables activo" "systemctl is-active nftables" "active"
verificar "systemd-resolved activo" "systemctl is-active systemd-resolved" "active"
verificar "DNSSEC habilitado" "resolvectl status | grep -c 'DNSSEC setting: yes'" "1"

echo ""
echo "--- SSH ---"
verificar "SSH activo" "systemctl is-active ssh" "active"
verificar "Sintaxis SSH válida" "sshd -t 2>&1 | grep -c 'error'" "0"
verificar "Root login deshabilitado" "sshd -T | grep 'permitrootlogin no'" "permitrootlogin no"

echo ""
echo "--- Nginx ---"
verificar "nginx activo" "systemctl is-active nginx" "active"
verificar "Sintaxis nginx válida" "nginx -t 2>&1 | grep -c 'ok'" "1"

echo ""
echo "--- Gestión de Paquetes ---"
verificar "unattended-upgrades activo" "systemctl is-enabled unattended-upgrades" "enabled"

echo ""
echo "--- Logs y Auditoría ---"
verificar "journald activo" "systemctl is-active systemd-journald" "active"
verificar "auditd activo" "systemctl is-active auditd" "active"
verificar "Reglas de auditoría" "auditctl -l | grep -c '^-'" "10"

echo ""
echo "--- Backups ---"
verificar "restic instalado" "which restic | grep -c restic" "1"

echo ""
echo "=== VERIFICACIÓN COMPLETADA ==="
```

---

## Referencias y Recursos Adicionales

- [Manual de Administración de Debian](https://www.debian.org/doc/manuals/debian-handbook/)
- [Guía de Seguridad de Debian](https://www.debian.org/doc/manuals/securing-debian-manual/)
- [Documentación de OpenSSH](https://www.openssh.com/manual.html)
- [Wiki de WireGuard](https://www.wireguard.com/)
- [Documentación de nginx](https://nginx.org/en/docs/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [Documentación de systemd](https://systemd.io/)
- [Manual de auditd](https://man7.org/linux/man-pages/man8/auditd.8.html)
- [Documentación de Restic](https://restic.readthedocs.io/)

---

*Documento generado para el Manual de Seguridad Informática de Debian 13 "Trixie"*
*Nivel 4: Red, Servicios y Mantenimiento Avanzado*
*Versión 1.0*
