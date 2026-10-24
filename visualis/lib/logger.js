/**
 * Módulo de logging de eventos y errores para Visualis
 * Envía logs al endpoint local /api/log para persistirlos en visualis.log
 */

async function sendLog(level, message, details = null, source = 'app') {
    try {
        if (typeof window === 'undefined') return

        const payload = {
            level,
            message,
            details,
            source
        }

        // Usar fetch sin bloquear
        fetch('/api/log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        }).catch(() => {
            // Silencioso si falla la red o el server está desconectado
        })
    } catch {
        // Fallback seguro
    }
}

export const logger = {
    info: (message, details, source) => {
        console.log(`[INFO] ${message}`, details || '')
        sendLog('INFO', message, details, source)
    },
    warn: (message, details, source) => {
        console.warn(`[WARN] ${message}`, details || '')
        sendLog('WARN', message, details, source)
    },
    error: (message, details, source) => {
        console.error(`[ERROR] ${message}`, details || '')
        sendLog('ERROR', message, details, source)
    }
}
