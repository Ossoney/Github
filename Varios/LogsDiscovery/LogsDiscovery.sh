#!/bin/bash
# log_discovery_interactive.sh - Versión 5.5
# Deep Scan + Process Forensic: Jerarquías, Zombis y Análisis de Padres.
set -uo pipefail

###############################################################################
# 1. FUNCIONES DE INTERFAZ Y UTILIDADES
###############################################################################

# Limpieza de archivos temporales
cleanup() {
    rm -f "${TEMP_RESULTS:-}" "${TEMP_DISCOVERED:-}" "${TEMP_CONSOLE:-}"
}
trap cleanup EXIT

print_color() { echo -e "\e[${1}m${2}\e[0m"; }

error_exit() {
    print_color "1;31" "✘ Error: $1"
    exit 1
}

print_main_header() {
    clear
    print_color "1;36" "==============================================="
    print_color "1;36" "   LOG DISCOVERY PRO v5.3 - FORENSIC EDITION"
    print_color "1;36" "==============================================="
}

display_results() {
    local temp_file="$1"
    local result_title="${2:-Reporte}"
    
    echo ""
    print_color "1;33" "┌─ OPCIONES DE VISUALIZACIÓN ──────────────────┐"
    print_color "1;37" "│"
    print_color "1;37" "│  1 = Ver PANTALLA A PANTALLA (con paginación)"
    print_color "1;30" "│     └─ Presiona SPACE para avanzar"
    print_color "1;30" "│     └─ Presiona Q para salir"
    print_color "1;37" "│"
    print_color "1;37" "│  2 = Ver TODO CONTINUO (sin pausas)"
    print_color "1;30" "│     └─ Usa scroll del terminal"
    print_color "1;30" "│     └─ Presiona Ctrl+C para detener"
    print_color "1;37" "│"
    print_color "1;37" "└────────────────────────────────────────────────┘"
    echo ""
    read -p "$(print_color '1;33' '➜ Seleccione visualización (1/2): ')" view_opt
    
    case "$view_opt" in
        1)
            echo ""
            print_color "1;36" "📄 Mostrando $result_title (PANTALLA A PANTALLA)"
            print_color "1;30" "   Instrucc: SPACE=siguiente | Q=salir"
            echo ""
            less "$temp_file"
            ;;
        2)
            echo ""
            print_color "1;36" "📄 Mostrando $result_title (CONTINUO)"
            print_color "1;30" "   Instruc: Ctrl+C para detener"
            echo ""
            cat "$temp_file"
            ;;
        *)
            echo ""
            print_color "1;31" "✘ Opción no válida"
            ;;
    esac
}

show_option_details() {
    local option="$1"
    
    case "$option" in
        1)
            print_color "1;36" "╔═══════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║    📋 AUDITORÍA FORENSE BÁSICA - DETALLES                     ║"
            print_color "1;36" "╚═══════════════════════════════════════════════════════════════╝"
            echo ""
            print_color "1;37" "  Esta opción va a:"
            print_color "1;30" "    ✓ Escanear logs del sistema, servicios y aplicaciones"
            print_color "1;30" "    ✓ Permitirte filtrar por antigüedad (24h, 7d, 30d, siempre)"
            print_color "1;30" "    ✓ Elegir ámbito: Sistema, Servicios o Completo"
            print_color "1;30" "    ✓ Buscar patrones críticos en los logs"
            print_color "1;30" "    ✓ Generar reporte en $REPORT_DIR"
            echo ""
            print_color "1;33" "  ⏱️  Tiempo estimado: 10-30 segundos"
            print_color "1;33" "  🔐 Requiere: sudo"
            echo ""
            ;;
        2)
            print_color "1;36" "╔═══════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║    💻 ANÁLISIS DE SISTEMA - DETALLES                         ║"
            print_color "1;36" "╚═══════════════════════════════════════════════════════════════╝"
            echo ""
            print_color "1;37" "  Esta opción va a:"
            print_color "1;30" "    ✓ Analizar recursos (CPU, RAM, Disco)"
            print_color "1;30" "    ✓ Buscar archivos modificados en últimas 24h"
            print_color "1;30" "    ✓ Listar conexiones de red activas"
            print_color "1;30" "    ✓ Estado y arranque automático de servicios"
            print_color "1;30" "    ✓ Mostrar resultado (pantalla a pantalla o continuo)"
            echo ""
            print_color "1;33" "  ⏱️  Tiempo estimado: 5-15 segundos"
            print_color "1;33" "  🔐 Requiere: sudo"
            echo ""
            ;;
        3)
            print_color "1;36" "╔═══════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║    🔒 SEGURIDAD AVANZADA - DETALLES                          ║"
            print_color "1;36" "╚═══════════════════════════════════════════════════════════════╝"
            echo ""
            print_color "1;37" "  Esta opción va a:"
            print_color "1;30" "    ✓ Detectar escalada de privilegios (SUID, SGID, sudo)"
            print_color "1;30" "    ✓ Analizar crontabs de todos los usuarios"
            print_color "1;30" "    ✓ Revisar configuración del firewall"
            print_color "1;30" "    ✓ Buscar intentos fallidos de login (últimas 24h)"
            print_color "1;30" "    ✓ Mostrar resultado (pantalla a pantalla o continuo)"
            echo ""
            print_color "1;33" "  ⏱️  Tiempo estimado: 10-20 segundos"
            print_color "1;33" "  🔐 Requiere: sudo"
            echo ""
            ;;
        4)
            print_color "1;36" "╔═══════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║    📁 ANÁLISIS DE ARCHIVOS - DETALLES                        ║"
            print_color "1;36" "╚═══════════════════════════════════════════════════════════════╝"
            echo ""
            print_color "1;37" "  Esta opción va a:"
            print_color "1;30" "    ✓ Buscar archivos sospechosos (SETUID, sin propietario)"
            print_color "1;30" "    ✓ Detectar permisos críticos cambiados en /etc"
            print_color "1;30" "    ✓ Listar archivos abiertos por procesos principales"
            print_color "1;30" "    ✓ Búsquedas optimizadas y rápidas (<1s cada una)"
            print_color "1;30" "    ✓ Mostrar resultado (pantalla a pantalla o continuo)"
            echo ""
            print_color "1;33" "  ⏱️  Tiempo estimado: 2-5 segundos"
            print_color "1;33" "  🔐 Requiere: sudo"
            echo ""
            ;;
        5)
            print_color "1;36" "╔═══════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║    📊 REPORTES AVANZADOS - DETALLES                          ║"
            print_color "1;36" "╚═══════════════════════════════════════════════════════════════╝"
            echo ""
            print_color "1;37" "  Esta opción va a:"
            print_color "1;30" "    ✓ Exportar último reporte a formato JSON"
            print_color "1;30" "    ✓ Exportar último reporte a formato CSV"
            print_color "1;30" "    ✓ Comparar con reportes anteriores (si los hay)"
            print_color "1;30" "    ✓ Opcionalmente enviar alerta por correo"
            print_color "1;30" "    ✓ Guardar en: $REPORT_DIR"
            echo ""
            print_color "1;33" "  ⏱️  Tiempo estimado: 5 segundos"
            print_color "1;33" "  📧 Nota: Requiere reporte previo (ejecuta primero opción 1-4)"
            echo ""
            ;;
        6)
            print_color "1;36" "╔═══════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║    🧠 ANÁLISIS INTELIGENTE - DETALLES                        ║"
            print_color "1;36" "╚═══════════════════════════════════════════════════════════════╝"
            echo ""
            print_color "1;37" "  Esta opción va a:"
            print_color "1;30" "    ✓ Correlacionar eventos (relaciones causa-efecto)"
            print_color "1;30" "    ✓ Detectar anomalías en el sistema"
            print_color "1;30" "    ✓ Analizar causalidad de problemas detectados"
            print_color "1;30" "    ✓ Generar prompts útiles para análisis con IA"
            print_color "1;30" "    ✓ Mostrar resultado (pantalla a pantalla o continuo)"
            echo ""
            print_color "1;33" "  ⏱️  Tiempo estimado: 15-30 segundos"
            print_color "1;33" "  🔐 Requiere: sudo"
            echo ""
            ;;
        7)
            print_color "1;36" "╔═══════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║    📅 LÍNEA DE TIEMPO - DETALLES                             ║"
            print_color "1;36" "╚═══════════════════════════════════════════════════════════════╝"
            echo ""
            print_color "1;37" "  Esta opción va a:"
            print_color "1;30" "    ✓ Construir cronología de eventos del sistema"
            print_color "1;30" "    ✓ Mostrar eventos críticos de las últimas 24h"
            print_color "1;30" "    ✓ Organizar por timestamps y source"
            print_color "1;30" "    ✓ Útil para investigación forense detallada"
            print_color "1;30" "    ✓ Mostrar resultado (pantalla a pantalla o continuo)"
            echo ""
            print_color "1;33" "  ⏱️  Tiempo estimado: 10 segundos"
            print_color "1;33" "  🔐 Requiere: sudo"
            echo ""
            ;;
    esac
}

###############################################################################
# 2. CONFIGURACIÓN DINÁMICA
###############################################################################

OS_TYPE="Linux"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS detection
    print_color "1;31" "=========================================================="
    print_color "1;31" " ✘ ERROR: SISTEMA OPERATIVO NO SOPORTADO"
    print_color "1;31" "=========================================================="
    echo " Este script no es compatible con macOS debido a diferencias"
    echo " en comandos fundamentales (systemctl, netstat, free, etc.)"
    echo " y la estructura del sistema de archivos BSD."
    echo ""
    exit 1
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || -n "${WINDIR:-}" ]]; then
    OS_TYPE="Windows"
    print_color "1;33" "=========================================================="
    print_color "1;33" " ⚠ AVISO: EJECUCIÓN EN WINDOWS DETECTADA"
    print_color "1;33" "=========================================================="
    print_color "1;37" " Para el correcto funcionamiento, asegúrate de estar usando:"
    print_color "1;37" "  - Git Bash (Recomendado)"
    print_color "1;37" "  - Cygwin"
    print_color "1;37" "  - MSYS2"
    echo ""
    print_color "1;30" " (Pulsa ENTER para continuar si estás en un entorno Bash válido...)"
    read -r
fi

REAL_USER="${SUDO_USER:-$USER}"

# Validar que el usuario existe
if ! id "$REAL_USER" &>/dev/null; then
    error_exit "Usuario no válido: $REAL_USER"
fi

if [ "$OS_TYPE" == "Linux" ]; then
    REPORT_DIR="/var/log/log_discovery"
    OPEN_CMD="sudo -u \"$REAL_USER\" xdg-open"
    PATH_SISTEMA="/var/log /home /opt /tmp"
    PATH_SERVICIOS="/var/log/apache2 /var/log/nginx /var/log/mysql /var/log/postgresql /var/lib/docker/containers"
    export PATH_SISTEMA PATH_SERVICIOS
    CRITICAL_PATTERNS=("Kernel/Hardware" "Disco/FS" "Seguridad/Auth" "App/Container" "Network/Firewall")
    declare -gA PATTERN_MAP=(
        ["Kernel/Hardware"]="kernel panic|OOM-killer|Machine Check Exception"
        ["Disco/FS"]="EXT4-fs error|XFS corruption|FAILED SMART|RAID1"
        ["Seguridad/Auth"]="authentication failure|failed password|user NOT in sudoers"
        ["App/Container"]="segfault|OutOfMemoryError|stack smashing|FATAL ERROR"
        ["Network/Firewall"]="transmit timeout|NETDEV WATCHDOG|UFW BLOCK"
    )
elif [ "$OS_TYPE" == "Windows" ]; then
    REPORT_DIR="/c/Users/$REAL_USER/Documents/LogDiscovery_Reports"
    OPEN_CMD="start"
    PATH_SISTEMA="/c/Windows/System32/winevt/Logs /c/Windows/Temp"
    PATH_SERVICIOS="/c/ProgramData /c/xampp/apache/logs /c/xampp/mysql/data"
    export PATH_SISTEMA PATH_SERVICIOS
    CRITICAL_PATTERNS=("Blue Screen" "Disk Error" "Logon Failure" "Service Error")
    declare -gA PATTERN_MAP=(
        ["Blue Screen"]="BugCheck|Critical Structure"
        ["Disk Error"]="disk is corrupt|Bad Block"
        ["Logon Failure"]="failed to log on|bad password"
        ["Service Error"]="terminated unexpectedly|timeout reached"
    )
fi

###############################################################################
# 3. MOTOR DE ANÁLISIS FORENSE DE PROCESOS (NUEVO)
###############################################################################

analyze_process_forensics() {
    {
        echo "==============================================================================="
        echo "                 ANÁLISIS FORENSE DE PROCESOS (SNAPSHOT)"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- PROCESOS JERÁRQUICOS (Árbol de ejecución) ---"
            # Muestra la jerarquía de procesos con PIDs y usuarios
            pstree -p -u | head -20
            
            echo -e "\n--- PROCESOS ZOMBIS / HUÉRFANOS ---"
            # Busca procesos en estado 'defunct' o huérfanos
            ps -ejH | grep '<defunct>' || echo "Estado: Sin procesos zombis detectados."
            
            echo -e "\n--- TOP 10 CPU (Relación Padre-Hijo) ---"
            # Identifica procesos con mayor consumo y su PPID para rastreo
            ps -eo pid,ppid,cmd,%cpu --sort=-%cpu | head -11
        else
            echo "Nota: El análisis jerárquico detallado (pstree) no está disponible nativamente"
            echo "en este entorno Windows. Se muestra lista de procesos básica:"
            tasklist | head -n 15
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

###############################################################################
# 4. ANÁLISIS DE SISTEMA (RECURSOS, RED, SERVICIOS)
###############################################################################

analyze_system_resources() {
    {
        echo "==============================================================================="
        echo "                    MONITOREO DE RECURSOS DEL SISTEMA"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- CPU Y MEMORIA (top) ---"
            timeout 2 top -b -n 1 2>/dev/null | head -15 || echo "Top no disponible o timeout"
            
            echo -e "\n--- CARGA DEL SISTEMA ---"
            uptime 2>/dev/null || echo "Uptime no disponible"
            
            echo -e "\n--- MEMORIA DETALLADA ---"
            free -h 2>/dev/null || echo "Free no disponible"
            
            echo -e "\n--- DISCO (Top 5 ubicaciones con más espacio) ---"
            timeout 5 du -sh /* 2>/dev/null | sort -rh | head -5 || echo "Du no disponible o timeout"
            
            echo -e "\n--- LOAD AVERAGE ---"
            cat /proc/loadavg 2>/dev/null || echo "Loadavg no disponible"
        else
            tasklist 2>/dev/null | head -20 || echo "Tasklist no disponible"
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

analyze_modified_files() {
    {
        echo "==============================================================================="
        echo "                 ARCHIVOS MODIFICADOS (últimas 24 horas)"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- MODIFICACIONES EN /etc ---"
            timeout 10s find /etc -type f -mtime -1 2>/dev/null | head -20
            
            echo -e "\n--- MODIFICACIONES EN /home ---"
            timeout 10s find /home -type f -mtime -1 2>/dev/null | head -20
            
            echo -e "\n--- MODIFICACIONES EN /opt ---"
            timeout 10s find /opt -type f -mtime -1 2>/dev/null | head -20
            
            echo -e "\n--- MODIFICACIONES EN /tmp ---"
            find /tmp -type f -mtime -1 2>/dev/null | head -20
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

analyze_network_connections() {
    {
        echo "==============================================================================="
        echo "                    CONEXIONES DE RED ACTIVAS"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- CONEXIONES ESTABLECIDAS (netstat) ---"
            if command -v netstat &>/dev/null; then
                netstat -tunap 2>/dev/null | grep ESTABLISHED | head -15 || true
            elif command -v ss &>/dev/null; then
                ss -tunap 2>/dev/null | grep ESTAB | head -15 || true
            fi
            
            echo -e "\n--- PUERTOS ESCUCHANDO ---"
            if command -v netstat &>/dev/null; then
                netstat -tunlp 2>/dev/null | grep LISTEN || true
            elif command -v ss &>/dev/null; then
                ss -tunlp 2>/dev/null | grep LISTEN || true
            fi
            
            echo -e "\n--- PROCESOS CON CONEXIONES DE RED ---"
            if command -v lsof &>/dev/null; then
                lsof -i -n -P 2>/dev/null | head -20 || true
            fi
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

analyze_services() {
    {
        echo "==============================================================================="
        echo "                   SERVICIOS Y DEMONIOS ACTIVOS"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- SERVICIOS SYSTEMD ACTIVOS ---"
            systemctl list-units --type=service --state=active --no-pager 2>/dev/null | head -20 || true
            
            echo -e "\n--- SERVICIOS HABILITADOS AL INICIO ---"
            systemctl list-unit-files --state=enabled 2>/dev/null | head -15 || true
            
            echo -e "\n--- PROCESOS CON PERMISOS ELEVADOS ---"
            ps -eo user,pid,ppid,cmd --sort=-cpu 2>/dev/null | awk '$1 ~ /root|sudo/ {print}' | head -15 || true
        fi

        echo "-------------------------------------------------------------------------------"
    }
}

analyze_docker() {
    {
        echo "==============================================================================="
        echo "                   ANÁLISIS DE CONTENEDORES DOCKER"
        echo "==============================================================================="
        
        if command -v docker &>/dev/null; then
            if docker ps >/dev/null 2>&1; then
                echo "--- CONTENEDORES ACTIVOS ---"
                docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}" | head -20
                
                echo -e "\n--- ESTADÍSTICAS (CPU/MEM) ---"
                timeout 5s docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | head -15
                
                echo -e "\n--- CONTENEDORES CON RESTARTING (Problemas) ---"
                docker ps --filter "status=restarting" --format "table {{.ID}}\t{{.Image}}\t{{.Status}}"
            else
                echo "Docker instalado pero no se puede contactar al demonio (¿falta sudo?)"
            fi
        else
            echo "Docker no encontrado en este sistema."
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

###############################################################################
# 5. ANÁLISIS DE SEGURIDAD AVANZADA
###############################################################################

analyze_privilege_escalation() {
    {
        echo "==============================================================================="
        echo "              ANÁLISIS DE ESCALADA DE PRIVILEGIOS"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- INTENTOS DE SUDO FALLIDOS (últimas 24h) ---"
            grep -i "sudo.*COMMAND=" /var/log/auth.log 2>/dev/null | grep -i denied | tail -10
            
            echo -e "\n--- CAMBIOS EXITOSOS A ROOT ---"
            grep "sudo.*COMMAND=" /var/log/auth.log 2>/dev/null | tail -10
            
            echo -e "\n--- SU FALLIDO ---"
            grep "su\[" /var/log/auth.log 2>/dev/null | grep FAILED | tail -10
            
            echo -e "\n--- USUARIOS CON CAPACIDAD SUDO ---"
            grep -i "sudo" /etc/group 2>/dev/null || echo "Grupo sudo no existe"
            
            echo -e "\n--- ENTRADAS SUDOERS SOSPECHOSAS ---"
            grep -v "^#" /etc/sudoers 2>/dev/null | grep -v "^$"
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

analyze_crontabs() {
    {
        echo "==============================================================================="
        echo "                 ANÁLISIS DE TAREAS PROGRAMADAS"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- CRONTAB DEL ROOT ---"
            cat /var/spool/cron/crontabs/root 2>/dev/null || echo "No disponible"
            
            echo -e "\n--- CRONTABS DE USUARIOS ---"
            for user in $(cut -f1 -d: /etc/passwd); do
                crontab -u "$user" -l 2>/dev/null && echo "Usuario: $user"
            done | head -30
            
            echo -e "\n--- TAREAS EN /etc/cron.* ---"
            find /etc/cron.* -type f 2>/dev/null | head -10
            
            echo -e "\n--- CONTENIDO DE /etc/cron.d ---"
            ls -la /etc/cron.d/ 2>/dev/null
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

analyze_firewall() {
    {
        echo "==============================================================================="
        echo "                   ANÁLISIS DE FIREWALL"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- UFW STATUS ---"
            if command -v ufw &>/dev/null; then
                ufw status verbose 2>/dev/null
            else
                echo "UFW no instalado"
            fi
            
            echo -e "\n--- IPTABLES RULES ---"
            if command -v iptables &>/dev/null; then
                iptables -L -n -v 2>/dev/null | head -30
            else
                echo "iptables no disponible"
            fi
            
            echo -e "\n--- FIREWALL LOG (últimas líneas) ---"
            grep -i "UFW\|FIREWALL" /var/log/syslog 2>/dev/null | tail -10
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

analyze_failed_logins() {
    {
        echo "==============================================================================="
        echo "              INTENTOS DE LOGIN FALLIDOS (posible fuerza bruta)"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- TOP 10 IPS CON INTENTOS FALLIDOS (últimas 24h) ---"
            grep "Failed password" /var/log/auth.log 2>/dev/null | grep "$(date +%b\ %d)" | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn | head -10
            
            echo -e "\n--- USUARIOS ATACADOS (últimas 24h) ---"
            grep "Failed password" /var/log/auth.log 2>/dev/null | grep "$(date +%b\ %d)" | awk '{print $9}' | sort | uniq -c | sort -rn | head -10
            
            echo -e "\n--- ÚLTIMOS 15 INTENTOS FALLIDOS ---"
            grep "Failed password" /var/log/auth.log 2>/dev/null | tail -15
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

###############################################################################
# 6. ANÁLISIS DE ARCHIVOS AVANZADO
###############################################################################

analyze_suspicious_files() {
    {
        echo "==============================================================================="
        echo "               BÚSQUEDA DE ARCHIVOS SOSPECHOSOS"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- ARCHIVOS SETUID/SETGID (posible escalada) ---"
            timeout 10s find /bin /sbin /usr/bin /usr/sbin -perm -4000 -o -perm -2000 2>/dev/null | head -20
            
            echo -e "\n--- SCRIPTS EN /tmp ---"
            find /tmp -type f \( -name "*.sh" -o -name "*.py" -o -name "*.pl" \) 2>/dev/null
            
            echo -e "\n--- ARCHIVOS SIN PERTENENCIA CLARA (en /home, /opt) ---"
            timeout 10s find /home /opt -nouser -o -nogroup 2>/dev/null | head -15
            
            echo -e "\n--- BINARIOS MODIFICADOS RECIENTEMENTE EN /bin, /sbin ---"
            find /bin /sbin -type f -mtime -7 2>/dev/null
            
            echo -e "\n--- ARCHIVOS CON PERMISOS WORLD-WRITABLE (en /tmp, /var) ---"
            timeout 10s find /tmp /var -perm -002 -type f 2>/dev/null | head -15
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

analyze_critical_permissions() {
    {
        echo "==============================================================================="
        echo "              ANÁLISIS DE PERMISOS EN ARCHIVOS CRÍTICOS"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- PERMISOS DE /etc/passwd, /etc/shadow, /etc/group ---"
            ls -l /etc/passwd /etc/shadow /etc/group /etc/gshadow 2>/dev/null
            
            echo -e "\n--- CAMBIOS EN /etc (últimas 24h) ---"
            timeout 10s find /etc -type f -mtime -1 2>/dev/null | head -20
            
            echo -e "\n--- PERMISOS DE ARCHIVOS SISTEMA CRÍTICOS ---"
            ls -l /boot/grub/grub.cfg /boot/vmlinuz* 2>/dev/null
            
            echo -e "\n--- SSH CONFIG ---"
            ls -l /etc/ssh/sshd_config /root/.ssh/authorized_keys 2>/dev/null
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

analyze_open_files() {
    {
        echo "==============================================================================="
        echo "           ARCHIVOS ABIERTOS POR PROCESOS (lsof analysis)"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ] && command -v lsof &>/dev/null; then
            echo "--- ARCHIVOS ABIERTOS POR TOP 5 PROCESOS ---"
            timeout 10 ps aux 2>/dev/null | sort -k3 -r | head -6 | tail -5 | while read line; do
                pid=$(echo "$line" | awk '{print $2}')
                cmd=$(echo "$line" | awk '{print $11}')
                echo "PID: $pid - CMD: $cmd"
                timeout 2 lsof -p "$pid" 2>/dev/null | head -3 || echo "Timeout o sin archivos"
                echo "---"
            done
            
            echo -e "\n--- ARCHIVOS ABIERTOS EN /tmp ---"
            timeout 5 lsof +D /tmp 2>/dev/null | head -10 || echo "Timeout o sin acceso"
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

###############################################################################
# 7. REPORTES AVANZADOS (JSON, CSV, EXPORTACIÓN)
###############################################################################

export_report_json() {
    local report_file="$1"
    local json_file="${report_file%.txt}.json"
    
    {
        echo "{"
        echo "  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
        echo "  \"hostname\": \"$(hostname)\","
        echo "  \"os_type\": \"$OS_TYPE\","
        echo "  \"user\": \"$REAL_USER\","
        echo "  \"report_file\": \"$report_file\","
        echo "  \"status\": \"completed\""
        echo "}"
    } > "$json_file"
    
    print_color "1;32" "✓ Reporte JSON: $json_file"
}

export_report_csv() {
    local report_file="$1"
    local csv_file="${report_file%.txt}.csv"
    
    {
        echo "timestamp,hostname,os_type,user,alert_type,status"
        echo "$(date +%Y-%m-%d\ %H:%M:%S),$(hostname),$OS_TYPE,$REAL_USER,forensic_analysis,completed"
    } > "$csv_file"
    
    print_color "1;32" "✓ Reporte CSV: $csv_file"
}

export_report_html() {
    local report_file="$1"
    local html_file="${report_file%.txt}.html"
    
    {
        echo "<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'><title>Reporte Forense</title>"
        echo "<style>"
        echo "body { background-color: #1e1e1e; color: #d4d4d4; font-family: monospace; padding: 20px; }"
        echo "h1, h2 { color: #569cd6; border-bottom: 1px solid #444; padding-bottom: 10px; }"
        echo ".alert { color: #f44747; font-weight: bold; }"
        echo ".ok { color: #608b4e; }"
        echo ".container { max-width: 1200px; margin: 0 auto; background: #252526; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.5); }"
        echo "pre { white-space: pre-wrap; word-wrap: break-word; }"
        echo "</style></head><body>"
        echo "<div class='container'>"
        echo "<h1>Reporte de Auditoría Digital</h1>"
        echo "<h2>Archivo fuente: $(basename "$report_file")</h2>"
        echo "<pre>"
        # Convert simple ANSI output or text to HTML safe text (basic) and highlight alerts
        sed -E 's/\[ ALERTA \]/\<span class="alert"\>\[ ALERTA \]\<\/span\>/g; s/\[ OK \]/\<span class="ok"\>\[ OK \]\<\/span\>/g' "$report_file" | \
        sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g" # Strip remaining colors
        echo "</pre>"
        echo "</div></body></html>"
    } > "$html_file"
    
    print_color "1;32" "✓ Reporte HTML: $html_file"
}

compare_reports() {
    {
        echo "==============================================================================="
        echo "                   COMPARACIÓN DE REPORTES"
        echo "==============================================================================="
        
        local reports=($(find "$REPORT_DIR" -name 'LogsDiscovery_*.txt' -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -2 | cut -d' ' -f2-))
        
        if [ ${#reports[@]} -lt 2 ]; then
            echo "Se necesitan al menos 2 reportes para comparar"
        else
            echo "Comparando: ${reports[0]} vs ${reports[1]}"
            echo "---"
            diff <(grep "ALERTA\|ERROR\|CRITICAL" "${reports[1]}" 2>/dev/null) \
                 <(grep "ALERTA\|ERROR\|CRITICAL" "${reports[0]}" 2>/dev/null)
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

send_email_alert() {
    local subject="$1"
    local message="$2"
    local recipient="${3:-root@localhost}"
    
    echo ""
    print_color "1;33" "📧 Iniciando proceso de envío de alerta..."
    
    # Intentar mail primero
    if command -v mail &>/dev/null; then
        print_color "1;33" "   ➜ Intentando usar 'mail' (utils-linux/bsd-mailx)..."
        if echo "$message" | mail -s "$subject" "$recipient"; then
            print_color "1;32" "   ✓ Comando 'mail' ejecutado correctamente."
            print_color "1;30" "     NOTA: Esto entrega el correo al MTA local (Postfix/Exim)."
            print_color "1;30" "     Si no llega, verifica la cola de correo (mailq) o logs (/var/log/mail.log)."
            return 0
        else
            print_color "1;31" "   ✘ Falló el comando 'mail'."
        fi
    fi
    
    # Intentar sendmail si mail no está disponible o falló
    if command -v sendmail &>/dev/null; then
        print_color "1;33" "   ➜ Intentando usar 'sendmail'..."
        if {
            echo "To: $recipient"
            echo "Subject: $subject"
            echo ""
            echo "$message"
        } | sendmail "$recipient"; then
            print_color "1;32" "   ✓ Comando 'sendmail' ejecutado correctamente."
            print_color "1;30" "     NOTA: Esto entrega el correo al MTA local."
            return 0
        else
            print_color "1;31" "   ✘ Falló el comando 'sendmail'."
        fi
    fi
    
    # Si nada está disponible, guardar en archivo .eml
    local eml_file="$REPORT_DIR/email_${recipient// /_}_$(date +%s).eml"
    mkdir -p "$REPORT_DIR"
    {
        echo "To: $recipient"
        echo "From: root@$(hostname)"
        echo "Subject: $subject"
        echo "Date: $(date -R)"
        echo ""
        echo "$message"
    } > "$eml_file"
    
    print_color "1;33" "⚠️  No se pudo enviar el correo (no hay 'mail'/'sendmail' o fallaron)."
    print_color "1;33" "   Guardado como archivo EML en: $eml_file"
    print_color "1;30" "   Puedes copiar este archivo o enviarlo manualmente."
    return 0
}


build_timeline() {
    {
        echo "==============================================================================="
        echo "                    LÍNEA DE TIEMPO DE EVENTOS"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- EVENTOS CRÍTICOS (últimas 24 horas) ---"
            {
                echo "TIMESTAMP|SOURCE|EVENT"
                grep -h "error\|ERROR\|CRITICAL\|FATAL\|failed\|FAILED" /var/log/auth.log /var/log/syslog 2>/dev/null | \
                    awk '{print $1" "$2" "$3"|auth/syslog|"$0}' | \
                    sort -k1 | head -20
            } | column -t -s '|'
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

###############################################################################
# 8. ANÁLISIS DE INTELIGENCIA Y CORRELACIÓN
###############################################################################

correlate_events() {
    {
        echo "==============================================================================="
        echo "                    CORRELACIÓN DE EVENTOS"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- EVENTOS RELACIONADOS (en la misma ventana de tiempo) ---"
            
            # Buscar patrones de correlación
            echo "Buscando procesos con conexiones sospechosas..."
            ps aux | while read line; do
                pid=$(echo $line | awk '{print $2}')
                cmd=$(echo $line | awk '{print $11}')
                if lsof -p $pid 2>/dev/null | grep -q "ESTABLISHED"; then
                    echo "CORRELACIÓN: PID $pid ($cmd) tiene conexión de red"
                fi
            done | head -10
            
            echo -e "\nBuscando procesos que acceden a archivos modificados..."
            for file in $(find /home /opt -type f -mtime -1 2>/dev/null | head -5); do
                if grep -r "$(basename $file)" /var/log/audit/ 2>/dev/null | head -1; then
                    echo "CORRELACIÓN: $file fue accedido por proceso registrado"
                fi
            done
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

detect_anomalies() {
    {
        echo "==============================================================================="
        echo "                    DETECCIÓN DE ANOMALÍAS"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- PROCESOS ANÓMALOS ---"
            ps aux | awk '{print $3}' | sort -rn | head -5 | while read cpu; do
                if (( $(echo "$cpu > 80" | bc -l 2>/dev/null) )); then
                    echo "⚠️  Proceso con CPU alta: $cpu%"
                fi
            done
            
            echo -e "\n--- MEMORIA ANÓMALA ---"
            ps aux | awk '{print $4}' | sort -rn | head -5 | while read mem; do
                if (( $(echo "$mem > 50" | bc -l 2>/dev/null) )); then
                    echo "⚠️  Proceso con memoria alta: $mem%"
                fi
            done
            
            echo -e "\n--- CONEXIONES ANÓMALAS (puertos inusuales) ---"
            if command -v netstat &>/dev/null; then
                netstat -tunap 2>/dev/null | awk '{print $4}' | grep -oE '[0-9]+$' | sort -u | while read port; do
                    if [ "$port" -gt 10000 ] && [ "$port" -lt 65535 ]; then
                        echo "⚠️  Puerto inusual detectado: $port"
                    fi
                done
            fi
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

analyze_causality() {
    {
        echo "==============================================================================="
        echo "                    ANÁLISIS DE CAUSALIDAD"
        echo "==============================================================================="
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo "--- RELACIÓN PROCESO PADRE-HIJO CON EVENTOS CRÍTICOS ---"
            
            # Analizar procesos que causaron errores
            echo "Procesos que generaron errores:"
            ps -ejH | while read line; do
                ppid=$(echo $line | awk '{print $2}')
                pid=$(echo $line | awk '{print $3}')
                if grep -q "pid=$pid\|ppid=$ppid" /var/log/syslog 2>/dev/null | head -1; then
                    echo "CAUSALIDAD: PID $pid (padre: $ppid) involucrado en evento crítico"
                fi
            done | head -10
            
            echo -e "\n--- CADENA DE CAUSAS (process chain) ---"
            echo "Analizando cadena padre-hijo de procesos del sistema..."
            ps -ejH --forest 2>/dev/null | head -20
        fi
        echo "-------------------------------------------------------------------------------"
    }
}

###############################################################################
# 4. MOTOR DE ESCANEO Y REPORTES
###############################################################################

setup_environment() {
    if [ "$OS_TYPE" == "Linux" ]; then
        if [[ $EUID -ne 0 ]]; then
            error_exit "Requiere sudo para ejecutar en Linux"
        fi
    fi
    
    # Crear directorio de reportes con manejo de errores
    if ! mkdir -p "$REPORT_DIR"; then
        error_exit "No se pudo crear directorio: $REPORT_DIR"
    fi
    
    # Verificar permisos de escritura
    if ! [ -w "$REPORT_DIR" ]; then
        error_exit "Sin permisos de escritura en: $REPORT_DIR"
    fi
}

manage_log_rotation() {
    local max_logs=5
    local count=0
    
    # Usar find para rotación segura
    while IFS= read -r file; do
        count=$((count + 1))
        if [ $count -gt $max_logs ]; then
            rm -f "$file" || print_color "1;33" "⚠️  No se pudo eliminar: $file"
        fi
    done < <(find "$REPORT_DIR" -name 'LogsDiscovery_*.txt' -type f -printf '%T@\0%p\n' 2>/dev/null | sort -zrn | cut -z -d' ' -f2-)
}

run_audit() {
    local time_filter="${1:-}"
    local scan_paths="${2:-}"
    local mode_name="${3:-}"
    
    # Validaciones
    [[ -z "$scan_paths" ]] && error_exit "scan_paths no especificado"
    [[ -z "$mode_name" ]] && error_exit "mode_name no especificado"
    
    local results ai_collector="" console_mirror
    results=$(mktemp) || error_exit "No se pudo crear archivo temporal"
    console_mirror=$(mktemp) || error_exit "No se pudo crear archivo temporal"
    TEMP_RESULTS="$results"
    TEMP_CONSOLE="$console_mirror"
    
    echo -e "\n"
    print_color "1;33" "🔍 Iniciando Análisis Forense en $OS_TYPE..."
    
    local discovered
    discovered=$(mktemp) || error_exit "No se pudo crear archivo temporal"
    TEMP_DISCOVERED="$discovered"
    
    # find seguro con comillas alrededor de paths
    find $scan_paths -type f \( -name "*.log" -o -name "*.evtx" -o -name "syslog" -o -name "auth.log" \) $time_filter -not -path "*/.*" 2>/dev/null > "$discovered" || true
    
    # Validar que se encontraron archivos
    if [ ! -s "$discovered" ]; then
        print_color "1;33" "⚠️  No se encontraron logs en los paths especificados"
    fi

    for err_name in "${CRITICAL_PATTERNS[@]}"; do
        printf "Verificando %-25s: " "$err_name" | tee -a "$console_mirror"
        
        # Usar xargs en lugar de expansión de globos para seguridad
        local match
        match=$(timeout 10s grep -i -lE -a "${PATTERN_MAP[$err_name]}" $(cat "$discovered") 2>/dev/null || true)
        local grep_exit=$?
        
        if [ $grep_exit -eq 124 ]; then
            echo -e "[ TIMEOUT ]" | tee -a "$console_mirror"
        elif [ -n "$match" ]; then
            echo -e "[ ALERTA ]" | tee -a "$console_mirror" && echo -ne "\a"
            while IFS= read -r f; do
                echo "$err_name|$f" >> "$results"
                ai_collector+="- $err_name detectado en $f\n"
            done <<< "$match"
        else
            echo -e "[ OK ]" | tee -a "$console_mirror"
        fi
    done
    

    
    local timestamp
    timestamp=$(date +"%Y%m%d_%H%M%S")
    local report_file="${REPORT_DIR}/LogsDiscovery_${timestamp}.txt"
    
    generate_report "$results" "$ai_collector" "$mode_name" "$console_mirror" "$report_file"
    
    display_results "$report_file" "Auditoría Forense ($mode_name)"
}

generate_report() {
    local results="${1:-}"
    local ai_data="${2:-}"
    local mode="${3:-}"
    local mirror="${4:-}"
    local report_file="${5:-}"
    
    # Validar archivos de entrada
    [[ -z "$results" || -z "$mirror" ]] && error_exit "Parámetros inválidos en generate_report"
    
    if [ -z "$report_file" ]; then
        local timestamp
        timestamp=$(date +"%Y%m%d_%H%M%S")
        report_file="${REPORT_DIR}/LogsDiscovery_${timestamp}.txt"
    fi
     
    
    {
        echo "==============================================================================="
        echo "                 REPORTE DISCOVERY & FORENSIC v5.4 - $timestamp"
        echo "==============================================================================="
        echo "SISTEMA: $OS_TYPE | ÁMBITO: $mode"
        echo "USUARIO: $REAL_USER | PID: $$"
        echo "-------------------------------------------------------------------------------"
        sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g" "$mirror"
        echo "-------------------------------------------------------------------------------"
        
        # Inserción de los nuevos datos de procesos
        analyze_process_forensics
        
        echo -e "\n>>> ANÁLISIS DE LOGS (Hallazgos Críticos) <<<"
        if [ -s "$results" ]; then
            column -t -s '|' "$results" 2>/dev/null || cat "$results"
        else
            echo "Sin alertas detectadas en logs."
        fi
        
        if [ "$OS_TYPE" == "Linux" ]; then
            echo -e "\n>>> KERNEL (dmesg) <<<"
            dmesg -T --level=err,warn 2>/dev/null | tail -n 5 || echo "(dmesg no disponible)"
        fi
        
        if [ -n "$ai_data" ]; then
            echo -e "\n==============================================================================="
            echo "                PROMPT PARA ANÁLISIS IA"
            echo "==============================================================================="
            echo -e "\"Analiza estos fallos críticos y la jerarquía de procesos:\n${ai_data:-Sin alertas de logs.}\n\nBasado en la lista de procesos y logs, ¿cuál es la causa raíz?\""
        fi
    } > "$report_file" || error_exit "No se pudo crear reporte en $report_file"

    chmod 644 "$report_file" 2>/dev/null || true
    manage_log_rotation
    
    print_color "1;32" "✓ Reporte generado: $report_file"
}

###############################################################################
# 5. INTERFAZ Y BUCLE
###############################################################################

# Variables globales para cleanup
TEMP_RESULTS=""
TEMP_DISCOVERED=""
TEMP_CONSOLE=""

display_main_menu() {
    print_main_header
    echo ""
    print_color "1;33" "┌─ OPCIONES DISPONIBLES ─────────────────────────────────────┐"
    print_color "1;37" "│"
    print_color "1;37" "│  1️⃣  Auditoría Forense Básica"
    print_color "1;37" "│  2️⃣  Análisis de Sistema (Recursos, Archivos, Red)"
    print_color "1;37" "│  3️⃣  Seguridad Avanzada (Escalada, Firewall, Failed Logins)"
    print_color "1;37" "│  4️⃣  Análisis de Archivos (SETUID, Permisos, Archivos Abiertos)"
    print_color "1;37" "│  5️⃣  Reportes Avanzados (JSON, CSV, Correo)"
    print_color "1;37" "│  6️⃣  Análisis Inteligente (Correlación, Anomalías)"
    print_color "1;37" "│  7️⃣  Línea de Tiempo (Cronología de eventos)"
    print_color "1;37" "│  0️⃣  Salir"
    print_color "1;37" "│"
    print_color "1;33" "└─────────────────────────────────────────────────────────────┘"
    print_color "1;30" "   ℹ️  Reportes en: $REPORT_DIR | ℹ️  Mayoría requiere: sudo"
    echo ""
}

setup_environment

while true; do
    display_main_menu
    read -p "$(print_color '1;33' '➜ Seleccione una opción (0-7): ')" main_input || exit 0
    
    case "$main_input" in
        0) 
            print_color "1;32" "✓ Gracias por usar LOG DISCOVERY PRO"
            exit 0 
            ;;
        
        1)

            show_option_details "1"
            read -p "$(print_color '1;33' '➜ ¿Desea continuar? (s/n): ')" confirm_opt || continue
            if [ "$confirm_opt" != "s" ] && [ "$confirm_opt" != "S" ]; then
                continue
            fi
            echo ""
            print_color "1;36" "╔════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║        AUDITORÍA FORENSE BÁSICA                            ║"
            print_color "1;36" "╚════════════════════════════════════════════════════════════╝"
            echo ""
            print_color "1;33" "📅 PASO 1: Seleccionar rango de tiempo"
            echo ""
            print_color "1;37" "  1 = Últimas 24 horas"
            print_color "1;37" "  2 = Últimos 7 días"
            print_color "1;37" "  3 = Últimos 30 días"
            print_color "1;37" "  4 = Todo el historial"
            echo ""
            read -p "$(print_color '1;33' '➜ Ingrese su opción (1-4): ')" t_input || continue
            case "$t_input" in
                1) t_filter="-mmin -1440"; t_label="últimas 24h" ;;
                2) t_filter="-mtime -7"; t_label="últimos 7 días" ;;
                3) t_filter="-mtime -30"; t_label="últimos 30 días" ;;
                4) t_filter=""; t_label="todo el historial" ;;
                *) 
                    print_color "1;31" "✘ Opción no válida"
                    continue 
                    ;;
            esac
            
            print_color "1;33" "📍 PASO 2: Seleccionar ámbito de búsqueda"
            echo ""
            print_color "1;37" "  a = Base (sistema, usuario, temporal)"
            print_color "1;37" "  b = Servicios (Apache, Nginx, MySQL, Docker, etc)"
            print_color "1;37" "  c = Completo (base + servicios)"
            echo ""
            read -p "$(print_color '1;33' '➜ Ingrese su opción (a/b/c): ')" a_input || continue
            case "$a_input" in
                a) 
                    run_audit "$t_filter" "$PATH_SISTEMA" "SISTEMA_BASE"
                    print_color "1;32" "✓ Auditoría completada para $t_label (Ámbito: Sistema Base)"
                    ;;
                b) 
                    run_audit "$t_filter" "$PATH_SERVICIOS" "SERVICIOS"
                    print_color "1;32" "✓ Auditoría completada para $t_label (Ámbito: Servicios)"
                    ;;
                c) 
                    run_audit "$t_filter" "$PATH_SISTEMA $PATH_SERVICIOS" "FULL_AUDIT"
                    print_color "1;32" "✓ Auditoría completada para $t_label (Ámbito: Completo)"
                    ;;
                *)
                    print_color "1;31" "✘ Opción no válida"
                    continue
                    ;;
            esac
            ;;
            
        2)

            show_option_details "2"
            read -p "$(print_color '1;33' '➜ ¿Desea continuar? (s/n): ')" confirm_opt || continue
            if [ "$confirm_opt" != "s" ] && [ "$confirm_opt" != "S" ]; then
                continue
            fi
            echo ""
            print_color "1;36" "╔════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║        ANÁLISIS DE SISTEMA                                 ║"
            print_color "1;36" "╚════════════════════════════════════════════════════════════╝"
            echo ""
            temp_analysis=$(mktemp) || error_exit "No se pudo crear archivo temporal"
            TEMP_RESULTS="$temp_analysis"
            
            print_color "1;33" "🚀 Iniciando análisis paralelo..."
            
            # Archivos temporales para cada subtarea
            t1=$(mktemp); t2=$(mktemp); t3=$(mktemp); t4=$(mktemp); t5=$(mktemp)
            
            # Ejecución paralela
            (analyze_system_resources > "$t1") &
            pid1=$!
            (analyze_modified_files > "$t2") &
            pid2=$!
            (analyze_network_connections > "$t3") &
            pid3=$!
            (analyze_services > "$t4") &
            pid4=$!
            (analyze_docker > "$t5") &
            pid5=$!
            
            wait $pid1 $pid2 $pid3 $pid4 $pid5
            
            cat "$t1" >> "$temp_analysis"
            cat "$t2" >> "$temp_analysis"
            cat "$t3" >> "$temp_analysis"
            cat "$t4" >> "$temp_analysis"
            cat "$t5" >> "$temp_analysis"
            
            rm -f "$t1" "$t2" "$t3" "$t4" "$t5"
            
            print_color "1;32" "✓ Análisis completado"
            display_results "$temp_analysis" "Análisis de Sistema"
            ;;
            
        3)

            show_option_details "3"
            read -p "$(print_color '1;33' '➜ ¿Desea continuar? (s/n): ')" confirm_opt || continue
            if [ "$confirm_opt" != "s" ] && [ "$confirm_opt" != "S" ]; then
                continue
            fi
            echo ""
            print_color "1;36" "╔════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║        SEGURIDAD AVANZADA                                  ║"
            print_color "1;36" "╚════════════════════════════════════════════════════════════╝"
            echo ""
            temp_security=$(mktemp) || error_exit "No se pudo crear archivo temporal"
            TEMP_RESULTS="$temp_security"
            
            print_color "1;33" "[1/4] Analizando escalada de privilegios..."
            analyze_privilege_escalation >> "$temp_security"
            print_color "1;32" "✓ Escaladas analizadas"
            
            print_color "1;33" "[2/4] Analizando crontabs programados..."
            analyze_crontabs >> "$temp_security"
            print_color "1;32" "✓ Crontabs analizados"
            
            print_color "1;33" "[3/4] Analizando firewall..."
            analyze_firewall >> "$temp_security"
            print_color "1;32" "✓ Firewall analizado"
            
            print_color "1;33" "[4/4] Buscando intentos de login fallidos..."
            analyze_failed_logins >> "$temp_security"
            print_color "1;32" "✓ Intentos fallidos encontrados"
            
            print_color "1;32" "✓ Análisis completado"
            display_results "$temp_security" "Seguridad Avanzada"
            ;;
            
        4)

            show_option_details "4"
            read -p "$(print_color '1;33' '➜ ¿Desea continuar? (s/n): ')" confirm_opt || continue
            if [ "$confirm_opt" != "s" ] && [ "$confirm_opt" != "S" ]; then
                continue
            fi
            echo ""
            print_color "1;36" "╔════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║        ANÁLISIS DE ARCHIVOS                                ║"
            print_color "1;36" "╚════════════════════════════════════════════════════════════╝"
            echo ""
            temp_files=$(mktemp) || error_exit "No se pudo crear archivo temporal"
            TEMP_RESULTS="$temp_files"
            
            print_color "1;33" "[1/3] Buscando archivos sospechosos..."
            print_color "1;30" "      (SETUID, SGID, sin propietario, world-writable)"
            analyze_suspicious_files >> "$temp_files"
            print_color "1;32" "✓ Archivos sospechosos analizados"
            
            print_color "1;33" "[2/3] Analizando permisos críticos..."
            print_color "1;30" "      (Cambios recientes en /etc)"
            analyze_critical_permissions >> "$temp_files"
            print_color "1;32" "✓ Permisos críticos analizados"
            
            print_color "1;33" "[3/3] Analizando archivos abiertos..."
            print_color "1;30" "      (Por procesos principales del sistema)"
            analyze_open_files >> "$temp_files"
            print_color "1;32" "✓ Archivos abiertos analizados"
            
            print_color "1;32" "✓ Análisis completado"
            display_results "$temp_files" "Análisis de Archivos"
            ;;
            
        5)

            show_option_details "5"
            read -p "$(print_color '1;33' '➜ ¿Desea continuar? (s/n): ')" confirm_opt || continue
            if [ "$confirm_opt" != "s" ] && [ "$confirm_opt" != "S" ]; then
                continue
            fi
            echo ""
            print_color "1;36" "╔════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║        REPORTES AVANZADOS                                  ║"
            print_color "1;36" "╚════════════════════════════════════════════════════════════╝"
            echo ""
            
            latest_report=$(find "$REPORT_DIR" -name 'LogsDiscovery_*.txt' -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
            
            if [ -z "$latest_report" ] || [ ! -s "$latest_report" ]; then
                print_color "1;31" "✘ No hay reportes disponibles. Ejecute primero una auditoría."
            else
                print_color "1;37" "📋 Reporte más reciente: $(basename "$latest_report")"
                echo ""
                
                print_color "1;33" "[1/5] Exportando a JSON..."
                export_report_json "$latest_report"
                print_color "1;32" "✓ JSON generado"
                
                print_color "1;33" "[2/5] Exportando a CSV..."
                export_report_csv "$latest_report"
                print_color "1;32" "✓ CSV generado"

                print_color "1;33" "[3/5] Exportando a HTML..."
                export_report_html "$latest_report"
                print_color "1;32" "✓ HTML generado"
                
                print_color "1;33" "[4/5] Comparando con reportes anteriores..."
                compare_reports
                print_color "1;32" "✓ Comparación completada"
                
                echo ""
                read -p "$(print_color '1;33' '➜ ¿Desea enviar alerta por correo? (s/n): ')" send_email_opt || continue
                if [ "$send_email_opt" == "s" ] || [ "$send_email_opt" == "S" ]; then
                    read -p "$(print_color '1;33' '➜ Email destino: ')" email_addr || continue
                    print_color "1;33" "[5/5] Enviando alerta por correo..."
                    send_email_alert "Análisis Forense Completado" "Se ha completado el análisis forense del sistema" "$email_addr"
                    if [ $? -eq 0 ]; then
                        print_color "1;32" "✓ Proceso completado"
                    fi
                fi
            fi
            ;;
            
        6)

            show_option_details "6"
            read -p "$(print_color '1;33' '➜ ¿Desea continuar? (s/n): ')" confirm_opt || continue
            if [ "$confirm_opt" != "s" ] && [ "$confirm_opt" != "S" ]; then
                continue
            fi
            echo ""
            print_color "1;36" "╔════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║        ANÁLISIS INTELIGENTE                                ║"
            print_color "1;36" "╚════════════════════════════════════════════════════════════╝"
            echo ""
            temp_intelligence=$(mktemp) || error_exit "No se pudo crear archivo temporal"
            TEMP_RESULTS="$temp_intelligence"
            
            print_color "1;33" "[1/3] Correlacionando eventos del sistema..."
            correlate_events >> "$temp_intelligence"
            print_color "1;32" "✓ Eventos correlacionados"
            
            print_color "1;33" "[2/3] Detectando anomalías..."
            detect_anomalies >> "$temp_intelligence"
            print_color "1;32" "✓ Anomalías detectadas"
            
            print_color "1;33" "[3/3] Analizando causalidad..."
            analyze_causality >> "$temp_intelligence"
            print_color "1;32" "✓ Causalidad analizada"
            
            print_color "1;32" "✓ Análisis completado"
            display_results "$temp_intelligence" "Análisis Inteligente"

            ;;
            
        7)
            show_option_details "7"
            read -p "$(print_color '1;33' '➜ ¿Desea continuar? (s/n): ')" confirm_opt || continue
            if [ "$confirm_opt" != "s" ] && [ "$confirm_opt" != "S" ]; then
                continue
            fi
            echo ""
            print_color "1;36" "╔════════════════════════════════════════════════════════════╗"
            print_color "1;36" "║        LÍNEA DE TIEMPO INTERACTIVA                         ║"
            print_color "1;36" "╚════════════════════════════════════════════════════════════╝"
            echo ""
            temp_timeline=$(mktemp) || error_exit "No se pudo crear archivo temporal"
            TEMP_RESULTS="$temp_timeline"
            
            print_color "1;33" "Construyendo línea de tiempo de eventos..."
            build_timeline >> "$temp_timeline"
            print_color "1;32" "✓ Línea de tiempo generada"
            display_results "$temp_timeline" "Línea de Tiempo"
            ;;
            
        *)
            print_color "1;31" "✘ Opción no válida. Ingrese un número del 0 al 7."
            ;;
    esac
    
    echo ""
    print_color "1;36" "════════════════════════════════════════════════════════════"
    read -p "$(print_color '1;33' '➜ Presione Enter para volver al menú principal...')" || exit 0
done