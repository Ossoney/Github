import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

const LOG_FILE_PATH = path.join(process.cwd(), 'visualis.log')

export async function POST(request) {
    try {
        const body = await request.json()
        const { level = 'INFO', message = '', details = null, source = 'client' } = body

        const timestamp = new Date().toISOString()
        let logLine = `[${timestamp}] [${level.toUpperCase()}] [${source}]: ${message}`
        
        if (details) {
            const formattedDetails = typeof details === 'object' ? JSON.stringify(details) : String(details)
            logLine += ` | Details: ${formattedDetails}`
        }
        
        logLine += '\n'

        // Escribir en modo append de forma síncrona/segura
        fs.appendFileSync(LOG_FILE_PATH, logLine, 'utf8')

        return NextResponse.json({ success: true })
    } catch (error) {
        console.error('Error al registrar log en disco:', error)
        return NextResponse.json({ success: false, error: error.message }, { status: 500 })
    }
}
