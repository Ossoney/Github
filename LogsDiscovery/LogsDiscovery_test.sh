#!/bin/bash
# Script de prueba para validar todas las funciones

set -euo pipefail

# Cargar el script principal
source /home/osso/Descargas/LogsDiscovery.sh

echo "=================================="
echo "PRUEBAS DEL SCRIPT LOGSDISCOVERY"
echo "=================================="
echo ""

# Test 1: Recursos del sistema
echo "[TEST 1] Analizando recursos del sistema..."
if analyze_system_resources | head -5 | grep -q "CPU\|MEMORIA\|CARGA\|DISCO"; then
    echo "✓ PASS: analyze_system_resources"
else
    echo "✘ FAIL: analyze_system_resources"
fi
echo ""

# Test 2: Archivos modificados
echo "[TEST 2] Buscando archivos modificados..."
if analyze_modified_files | head -5 | grep -q "ARCHIVOS\|etc\|home"; then
    echo "✓ PASS: analyze_modified_files"
else
    echo "✘ FAIL: analyze_modified_files"
fi
echo ""

# Test 3: Conexiones de red
echo "[TEST 3] Analizando conexiones de red..."
if analyze_network_connections | head -5 | grep -q "CONEXIONES\|PUERTOS\|LISTEN"; then
    echo "✓ PASS: analyze_network_connections"
else
    echo "✘ FAIL: analyze_network_connections"
fi
echo ""

# Test 4: Servicios
echo "[TEST 4] Analizando servicios..."
if analyze_services | head -5 | grep -q "SERVICIOS\|systemd\|active"; then
    echo "✓ PASS: analyze_services"
else
    echo "✘ FAIL: analyze_services"
fi
echo ""

# Test 5: Escalada de privilegios
echo "[TEST 5] Analizando escalada de privilegios..."
if analyze_privilege_escalation | head -5 | grep -q "ESCALADA\|SUDO\|privilegios"; then
    echo "✓ PASS: analyze_privilege_escalation"
else
    echo "✘ FAIL: analyze_privilege_escalation"
fi
echo ""

# Test 6: Crontabs
echo "[TEST 6] Analizando crontabs..."
if analyze_crontabs | head -5 | grep -q "CRONTAB\|TAREAS\|cron"; then
    echo "✓ PASS: analyze_crontabs"
else
    echo "✘ FAIL: analyze_crontabs"
fi
echo ""

# Test 7: Firewall
echo "[TEST 7] Analizando firewall..."
if analyze_firewall | head -5 | grep -q "FIREWALL\|UFW\|IPTABLES"; then
    echo "✓ PASS: analyze_firewall"
else
    echo "✘ FAIL: analyze_firewall"
fi
echo ""

# Test 8: Login fallidos
echo "[TEST 8] Analizando intentos fallidos..."
if analyze_failed_logins | head -5 | grep -q "LOGIN\|FALLIDOS\|fuerza"; then
    echo "✓ PASS: analyze_failed_logins"
else
    echo "✘ FAIL: analyze_failed_logins"
fi
echo ""

# Test 9: Archivos sospechosos
echo "[TEST 9] Buscando archivos sospechosos..."
if analyze_suspicious_files | head -5 | grep -q "SOSPECHOSOS\|setuid\|tmp"; then
    echo "✓ PASS: analyze_suspicious_files"
else
    echo "✘ FAIL: analyze_suspicious_files"
fi
echo ""

# Test 10: Permisos críticos
echo "[TEST 10] Analizando permisos críticos..."
if analyze_critical_permissions | head -5 | grep -q "PERMISOS\|passwd\|shadow"; then
    echo "✓ PASS: analyze_critical_permissions"
else
    echo "✘ FAIL: analyze_critical_permissions"
fi
echo ""

# Test 11: Archivos abiertos
echo "[TEST 11] Analizando archivos abiertos..."
if analyze_open_files | head -5 | grep -q "ARCHIVOS\|lsof\|abiertos"; then
    echo "✓ PASS: analyze_open_files"
else
    echo "✘ FAIL: analyze_open_files"
fi
echo ""

# Test 12: Exportar JSON
echo "[TEST 12] Exportando a JSON..."
local temp_json=$(mktemp)
if export_report_json "$temp_json" 2>&1 | grep -q "JSON"; then
    echo "✓ PASS: export_report_json"
    rm -f "$temp_json" "${temp_json%.txt}.json"
else
    echo "✘ FAIL: export_report_json"
fi
echo ""

# Test 13: Exportar CSV
echo "[TEST 13] Exportando a CSV..."
local temp_csv=$(mktemp)
if export_report_csv "$temp_csv" 2>&1 | grep -q "CSV"; then
    echo "✓ PASS: export_report_csv"
    rm -f "$temp_csv" "${temp_csv%.txt}.csv"
else
    echo "✘ FAIL: export_report_csv"
fi
echo ""

# Test 14: Línea de tiempo
echo "[TEST 14] Construyendo línea de tiempo..."
if build_timeline | head -5 | grep -q "TIMELINE\|EVENTOS\|TIMESTAMP"; then
    echo "✓ PASS: build_timeline"
else
    echo "✘ FAIL: build_timeline"
fi
echo ""

# Test 15: Correlación
echo "[TEST 15] Correlacionando eventos..."
if correlate_events | head -5 | grep -q "CORRELACIÓN\|eventos"; then
    echo "✓ PASS: correlate_events"
else
    echo "✘ FAIL: correlate_events"
fi
echo ""

# Test 16: Anomalías
echo "[TEST 16] Detectando anomalías..."
if detect_anomalies | head -5 | grep -q "ANOMAL\|CPU\|MEMORIA"; then
    echo "✓ PASS: detect_anomalies"
else
    echo "✘ FAIL: detect_anomalies"
fi
echo ""

# Test 17: Causalidad
echo "[TEST 17] Analizando causalidad..."
if analyze_causality | head -5 | grep -q "CAUSAL\|proceso\|chain"; then
    echo "✓ PASS: analyze_causality"
else
    echo "✘ FAIL: analyze_causality"
fi
echo ""

# Test 18: Funciones auxiliares
echo "[TEST 18] Probando funciones auxiliares..."
if print_color "1;32" "Test" | grep -q "Test"; then
    echo "✓ PASS: print_color"
else
    echo "✘ FAIL: print_color"
fi
echo ""

echo "=================================="
echo "PRUEBAS COMPLETADAS"
echo "=================================="
