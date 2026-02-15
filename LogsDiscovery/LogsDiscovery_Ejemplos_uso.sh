#!/bin/bash
# Ejemplos de uso del LogsDiscovery v5.4

# ==============================================================================
# EJEMPLO 1: Ejecución interactiva completa
# ==============================================================================
# $ sudo /home/osso/Descargas/LogsDiscovery.sh
# 
# [Seleccionar opción 1 para auditoría forense]
# [Seleccionar 24 horas]
# [Seleccionar auditoría completa]
# [Esperar análisis]
# [Reporte se abre automáticamente]


# ==============================================================================
# EJEMPLO 2: Análisis rápido de recursos en línea de comandos
# ==============================================================================
# Cargar solo las funciones necesarias:

# source /home/osso/Descargas/LogsDiscovery.sh
# analyze_system_resources | less


# ==============================================================================
# EJEMPLO 3: Detección de escalada de privilegios
# ==============================================================================
# sudo bash -c 'source /home/osso/Descargas/LogsDiscovery.sh && analyze_privilege_escalation'


# ==============================================================================
# EJEMPLO 4: Búsqueda de archivos sospechosos
# ==============================================================================
# sudo bash -c 'source /home/osso/Descargas/LogsDiscovery.sh && analyze_suspicious_files | grep -i "setuid\|world-writable"'


# ==============================================================================
# EJEMPLO 5: Análisis de conexiones de red activas
# ==============================================================================
# sudo bash -c 'source /home/osso/Descargas/LogsDiscovery.sh && analyze_network_connections | grep ESTABLISHED'


# ==============================================================================
# EJEMPLO 6: Generar reportes en JSON y CSV para análisis posterior
# ==============================================================================

#!/bin/bash
set -euo pipefail

# Crear directorio temporal
WORK_DIR=$(mktemp -d)
trap "rm -rf $WORK_DIR" EXIT

# Generar reporte base
REPORT="$WORK_DIR/report_$(date +%s).txt"
echo "Generando reporte..." > "$REPORT"

# Cargar funciones
source /home/osso/Descargas/LogsDiscovery.sh

# Exportar a JSON
export_report_json "$REPORT"

# Exportar a CSV
export_report_csv "$REPORT"

echo "Reportes disponibles:"
ls -lah "$WORK_DIR"/*.json "$WORK_DIR"/*.csv


# ==============================================================================
# EJEMPLO 7: Análisis inteligente - Correlación de eventos
# ==============================================================================
# sudo bash -c 'source /home/osso/Descargas/LogsDiscovery.sh && correlate_events'


# ==============================================================================
# EJEMPLO 8: Detección de anomalías
# ==============================================================================
# sudo bash -c 'source /home/osso/Descargas/LogsDiscovery.sh && detect_anomalies'


# ==============================================================================
# EJEMPLO 9: Análisis de causalidad - ¿Qué proceso causó qué?
# ==============================================================================
# sudo bash -c 'source /home/osso/Descargas/LogsDiscovery.sh && analyze_causality'


# ==============================================================================
# EJEMPLO 10: Monitoreo de tareas programadas sospechosas
# ==============================================================================
# sudo bash -c 'source /home/osso/Descargas/LogsDiscovery.sh && analyze_crontabs | grep -v "^#"'


# ==============================================================================
# EJEMPLO 11: Auditoría de firewall en tiempo real
# ==============================================================================
# sudo bash -c 'source /home/osso/Descargas/LogsDiscovery.sh && analyze_firewall'


# ==============================================================================
# EJEMPLO 12: Detectar intentos de fuerza bruta (últimas 24 horas)
# ==============================================================================
# sudo bash -c 'source /home/osso/Descargas/LogsDiscovery.sh && analyze_failed_logins | tail -20'


# ==============================================================================
# EJEMPLO 13: Script automatizado para respuesta a incidentes
# ==============================================================================

#!/bin/bash
set -euo pipefail

# Configuración
INCIDENT_ID="${1:-INCIDENT_$(date +%s)}"
OUTPUT_DIR="/var/log/log_discovery/incident_${INCIDENT_ID}"

# Crear directorio de incidente
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# Cargar funciones
source /home/osso/Descargas/LogsDiscovery.sh

echo "[$(date)] Iniciando análisis de incidente: $INCIDENT_ID" | tee incident.log

# Ejecutar análisis completo
echo "[$(date)] 1. Analizando recursos..." | tee -a incident.log
analyze_system_resources > 01_resources.txt 2>&1

echo "[$(date)] 2. Buscando archivos modificados..." | tee -a incident.log
analyze_modified_files > 02_modified_files.txt 2>&1

echo "[$(date)] 3. Analizando conexiones de red..." | tee -a incident.log
analyze_network_connections > 03_network.txt 2>&1

echo "[$(date)] 4. Detectando escalada de privilegios..." | tee -a incident.log
analyze_privilege_escalation > 04_escalation.txt 2>&1

echo "[$(date)] 5. Buscando archivos sospechosos..." | tee -a incident.log
analyze_suspicious_files > 05_suspicious.txt 2>&1

echo "[$(date)] 6. Correlacionando eventos..." | tee -a incident.log
correlate_events > 06_correlation.txt 2>&1

echo "[$(date)] 7. Detectando anomalías..." | tee -a incident.log
detect_anomalies > 07_anomalies.txt 2>&1

echo "[$(date)] 8. Analizando causalidad..." | tee -a incident.log
analyze_causality > 08_causality.txt 2>&1

# Generar resumen
cat > INCIDENT_SUMMARY.txt << SUMMARY
ANÁLISIS DE INCIDENTE
====================
ID: $INCIDENT_ID
Timestamp: $(date)
Directorio: $OUTPUT_DIR

Archivos generados:
$(ls -1 *.txt | sed 's/^/  - /')

Para más detalles, revisar cada archivo .txt
SUMMARY

echo "[$(date)] Análisis completado. Ver INCIDENT_SUMMARY.txt" | tee -a incident.log

# Mostrar resumen
cat INCIDENT_SUMMARY.txt


# ==============================================================================
# EJEMPLO 14: Monitoreo periódico con cron
# ==============================================================================

# Agregar a crontab:
# 0 */6 * * * /usr/local/bin/logsdiscovery_periodic_check.sh

#!/bin/bash
# /usr/local/bin/logsdiscovery_periodic_check.sh

set -euo pipefail

REPORT_DIR="/var/log/log_discovery/periodic"
mkdir -p "$REPORT_DIR"

source /home/osso/Descargas/LogsDiscovery.sh

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT="$REPORT_DIR/check_$TIMESTAMP.txt"

{
    echo "Verificación periódica: $TIMESTAMP"
    echo "=================================="
    echo ""
    
    echo "ANOMALÍAS DETECTADAS:"
    detect_anomalies
    
    echo ""
    echo "EVENTOS CORRELACIONADOS:"
    correlate_events
    
    echo ""
    echo "INTENTOS FALLIDOS (últimas 24h):"
    analyze_failed_logins | head -10
    
} > "$OUTPUT" 2>&1

# Enviar alerta si hay anomalías críticas
if grep -q "⚠️" "$OUTPUT" 2>/dev/null; then
    echo "ALERTA: Anomalías detectadas en $TIMESTAMP" | \
        mail -s "LogsDiscovery Alert" root@localhost
fi


# ==============================================================================
# EJEMPLO 15: Integración con SIEM (Splunk, ELK, etc.)
# ==============================================================================

#!/bin/bash
# Exportar datos a formato SIEM-compatible

source /home/osso/Descargas/LogsDiscovery.sh

REPORT="/tmp/report_$(date +%s).txt"

# Crear reporte
{
    echo "timestamp=$(date +%s)"
    echo "hostname=$(hostname)"
    echo "event_type=forensic_analysis"
    analyze_system_resources
    analyze_network_connections
    detect_anomalies
} > "$REPORT"

# Enviar a servidor SIEM (ejemplo con curl/syslog)
# curl -X POST http://siem-server:8088/services/collector \
#   -H "Authorization: Splunk YOUR_TOKEN" \
#   --data-binary @"$REPORT"

# O usar rsyslog:
# logger -t logsdiscovery "$(cat $REPORT)"

echo "Datos exportados para SIEM"


# ==============================================================================
# EJEMPLO 16: Benchmark - Comparar estado antes/después de cambios
# ==============================================================================

#!/bin/bash
set -euo pipefail

BASELINE_DIR="/tmp/baseline_$(date +%s)"
mkdir -p "$BASELINE_DIR"

source /home/osso/Descargas/LogsDiscovery.sh

echo "=== CAPTURANDO BASELINE ACTUAL ==="
analyze_system_resources > "$BASELINE_DIR/baseline.txt"

echo ""
echo "Baseline guardado en: $BASELINE_DIR/baseline.txt"
echo ""
echo "Realizar cambios en el sistema..."
echo ""
read -p "Presione Enter cuando haya terminado los cambios"

echo ""
echo "=== CAPTURANDO ESTADO POST-CAMBIOS ==="
POSTCHANGE_DIR="/tmp/postchange_$(date +%s)"
mkdir -p "$POSTCHANGE_DIR"
analyze_system_resources > "$POSTCHANGE_DIR/postchange.txt"

echo ""
echo "=== COMPARACIÓN ==="
diff "$BASELINE_DIR/baseline.txt" "$POSTCHANGE_DIR/postchange.txt" || true


# ==============================================================================
# NOTAS IMPORTANTES
# ==============================================================================

# 1. REQUISITOS:
#    - Ejecutar con sudo para acceso a logs del sistema
#    - Herramientas: top, ps, find, grep, netstat/ss, systemctl, lsof

# 2. SEGURIDAD:
#    - Los reportes contienen información sensible
#    - Proteger /var/log/log_discovery/ con permisos restrictivos
#    - No compartir reportes sin verificar contenido

# 3. PERFORMANCE:
#    - Análisis completo puede tardar 1-5 minutos
#    - Para servidores grandes, usar opciones específicas
#    - No ejecutar múltiples instancias simultáneamente

# 4. TROUBLESHOOTING:
#    - Si hay errores, revisar /var/log/syslog
#    - Verificar permisos de directorios
#    - Asegurar que bash >= 4.4

# 5. INTEGRACIÓN:
#    - Compatible con ELK, Splunk, Graylog
#    - Exporta a JSON, CSV, texto plano
#    - Permite correlación de eventos

echo "Ejemplos completados"
