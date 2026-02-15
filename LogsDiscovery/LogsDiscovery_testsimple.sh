#!/bin/bash
# Script de prueba simplificado para validar funciones sin sudo

set -euo pipefail

# Variables de configuración sin llamar a setup_environment
export OS_TYPE="Linux"
export REPORT_DIR="/tmp/test_logs_discovery"
export REAL_USER="$USER"
export PATH_SISTEMA="/var/log /home /opt /tmp"
export PATH_SERVICIOS="/var/log/apache2 /var/log/nginx /var/log/mysql"

mkdir -p "$REPORT_DIR"

# Cargar solo las funciones necesarias del script principal
source <(sed -n '/^print_color()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^error_exit()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^analyze_system_resources()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^analyze_modified_files()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^analyze_network_connections()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^analyze_services()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^analyze_privilege_escalation()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^analyze_crontabs()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^analyze_firewall()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^analyze_failed_logins()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^analyze_suspicious_files()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^analyze_critical_permissions()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^analyze_open_files()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^export_report_json()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^export_report_csv()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^build_timeline()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^correlate_events()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^detect_anomalies()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)
source <(sed -n '/^analyze_causality()/,/^}/p' /home/osso/Descargas/LogsDiscovery.sh)

echo "=================================="
echo "PRUEBAS DEL SCRIPT LOGSDISCOVERY"
echo "=================================="
echo ""

# Test 1: Recursos del sistema
echo "[TEST 1/18] Analizando recursos del sistema..."
result=$(analyze_system_resources 2>&1 | head -10)
if echo "$result" | grep -qi "CPU\|MEMORIA\|CARGA\|DISCO\|TOP\|uptime"; then
    echo "✓ PASS: analyze_system_resources"
else
    echo "✘ FAIL: analyze_system_resources"
    echo "Output: $result"
fi
echo ""

# Test 2: Archivos modificados
echo "[TEST 2/18] Buscando archivos modificados..."
result=$(analyze_modified_files 2>&1 | head -10)
if echo "$result" | grep -qi "ARCHIVOS\|MODIF\|etc\|home"; then
    echo "✓ PASS: analyze_modified_files"
else
    echo "✘ FAIL: analyze_modified_files"
fi
echo ""

# Test 3: Conexiones de red
echo "[TEST 3/18] Analizando conexiones de red..."
result=$(analyze_network_connections 2>&1 | head -10)
if echo "$result" | grep -qi "CONEXIONES\|RED\|PUERTOS\|LISTEN"; then
    echo "✓ PASS: analyze_network_connections"
else
    echo "✘ FAIL: analyze_network_connections"
fi
echo ""

# Test 4: Servicios
echo "[TEST 4/18] Analizando servicios..."
result=$(analyze_services 2>&1 | head -10)
if echo "$result" | grep -qi "SERVICIOS\|systemd\|active"; then
    echo "✓ PASS: analyze_services"
else
    echo "✘ FAIL: analyze_services"
fi
echo ""

# Test 5: Escalada de privilegios
echo "[TEST 5/18] Analizando escalada de privilegios..."
result=$(analyze_privilege_escalation 2>&1 | head -10)
if echo "$result" | grep -qi "ESCALADA\|PRIVILEGIOS\|sudo"; then
    echo "✓ PASS: analyze_privilege_escalation"
else
    echo "✘ FAIL: analyze_privilege_escalation"
fi
echo ""

# Test 6: Crontabs
echo "[TEST 6/18] Analizando crontabs..."
result=$(analyze_crontabs 2>&1 | head -10)
if echo "$result" | grep -qi "CRONTAB\|TAREAS\|cron"; then
    echo "✓ PASS: analyze_crontabs"
else
    echo "✘ FAIL: analyze_crontabs"
fi
echo ""

# Test 7: Firewall
echo "[TEST 7/18] Analizando firewall..."
result=$(analyze_firewall 2>&1 | head -10)
if echo "$result" | grep -qi "FIREWALL\|UFW\|IPTABLES"; then
    echo "✓ PASS: analyze_firewall"
else
    echo "✘ FAIL: analyze_firewall"
fi
echo ""

# Test 8: Login fallidos
echo "[TEST 8/18] Analizando intentos fallidos..."
result=$(analyze_failed_logins 2>&1 | head -10)
if echo "$result" | grep -qi "LOGIN\|FALLIDOS\|intentos"; then
    echo "✓ PASS: analyze_failed_logins"
else
    echo "✘ FAIL: analyze_failed_logins"
fi
echo ""

# Test 9: Archivos sospechosos
echo "[TEST 9/18] Buscando archivos sospechosos..."
result=$(analyze_suspicious_files 2>&1 | head -10)
if echo "$result" | grep -qi "SOSPECHOSOS\|setuid\|tmp"; then
    echo "✓ PASS: analyze_suspicious_files"
else
    echo "✘ FAIL: analyze_suspicious_files"
fi
echo ""

# Test 10: Permisos críticos
echo "[TEST 10/18] Analizando permisos críticos..."
result=$(analyze_critical_permissions 2>&1 | head -10)
if echo "$result" | grep -qi "PERMISOS\|passwd\|shadow"; then
    echo "✓ PASS: analyze_critical_permissions"
else
    echo "✘ FAIL: analyze_critical_permissions"
fi
echo ""

# Test 11: Archivos abiertos
echo "[TEST 11/18] Analizando archivos abiertos..."
result=$(analyze_open_files 2>&1 | head -10)
if echo "$result" | grep -qi "ARCHIVOS\|abiertos"; then
    echo "✓ PASS: analyze_open_files"
else
    echo "✘ FAIL: analyze_open_files"
fi
echo ""

# Test 12: Exportar JSON
echo "[TEST 12/18] Exportando a JSON..."
temp_json=$(mktemp)
if export_report_json "$temp_json" 2>&1 | grep -q "JSON"; then
    echo "✓ PASS: export_report_json"
    if [ -f "${temp_json%.txt}.json" ]; then
        echo "  ✓ Archivo JSON creado correctamente"
        rm -f "$temp_json" "${temp_json%.txt}.json"
    fi
else
    echo "✘ FAIL: export_report_json"
fi
echo ""

# Test 13: Exportar CSV
echo "[TEST 13/18] Exportando a CSV..."
temp_csv=$(mktemp)
if export_report_csv "$temp_csv" 2>&1 | grep -q "CSV"; then
    echo "✓ PASS: export_report_csv"
    if [ -f "${temp_csv%.txt}.csv" ]; then
        echo "  ✓ Archivo CSV creado correctamente"
        rm -f "$temp_csv" "${temp_csv%.txt}.csv"
    fi
else
    echo "✘ FAIL: export_report_csv"
fi
echo ""

# Test 14: Línea de tiempo
echo "[TEST 14/18] Construyendo línea de tiempo..."
result=$(build_timeline 2>&1 | head -10)
if echo "$result" | grep -qi "TIMELINE\|EVENTOS\|TIMESTAMP"; then
    echo "✓ PASS: build_timeline"
else
    echo "✘ FAIL: build_timeline"
fi
echo ""

# Test 15: Correlación
echo "[TEST 15/18] Correlacionando eventos..."
result=$(correlate_events 2>&1 | head -10)
if echo "$result" | grep -qi "CORRELACIÓN\|eventos\|relacionados"; then
    echo "✓ PASS: correlate_events"
else
    echo "✘ FAIL: correlate_events"
fi
echo ""

# Test 16: Anomalías
echo "[TEST 16/18] Detectando anomalías..."
result=$(detect_anomalies 2>&1 | head -10)
if echo "$result" | grep -qi "ANOMAL\|anómalos\|MEMORIA"; then
    echo "✓ PASS: detect_anomalies"
else
    echo "✘ FAIL: detect_anomalies"
fi
echo ""

# Test 17: Causalidad
echo "[TEST 17/18] Analizando causalidad..."
result=$(analyze_causality 2>&1 | head -10)
if echo "$result" | grep -qi "CAUSAL\|proceso\|chain\|RELACIÓN"; then
    echo "✓ PASS: analyze_causality"
else
    echo "✘ FAIL: analyze_causality"
fi
echo ""

# Test 18: Funciones auxiliares
echo "[TEST 18/18] Probando funciones auxiliares..."
result=$(print_color "1;32" "Test" 2>&1)
if echo "$result" | grep -q "Test"; then
    echo "✓ PASS: print_color"
else
    echo "✘ FAIL: print_color"
fi
echo ""

# Limpieza
rm -rf "$REPORT_DIR"

echo "=================================="
echo "PRUEBAS COMPLETADAS"
echo "=================================="
