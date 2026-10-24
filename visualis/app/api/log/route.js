import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

const LOG_FILE_PATH = path.join(process.cwd(), 'visualis.log')
const isVercel = !!process.env.VERCEL

export async function POST(request) {
    try {
        const body = await request.json()
        const { level = 'INFO', message = '', details = null, source = 'client' } = body

        // Limitar tamaño de mensaje para evitar abusos o desbordamiento
        const safeMessage = String(message).slice(0, 500)
        const timestamp = new Date().toISOString()
        let logLine = `[${timestamp}] [${String(level).toUpperCase()}] [${String(source).slice(0, 50)}]: ${safeMessage}`
        
        if (details) {
            const formattedDetails = typeof details === 'object' ? JSON.stringify(details).slice(0, 2000) : String(details).slice(0, 2000)
            logLine += ` | Details: ${formattedDetails}`
        }

        // Si está en Vercel, emitir a consola estándar (se ve en panel Vercel Logs) sin bloquear disco efímero
        if (isVercel) {
            console.log(logLine)
        } else {
            // En local, persistir en visualis.log
            try {
                fs.appendFileSync(LOG_FILE_PATH, logLine + '\n', 'utf8')
            } catch (fsErr) {
                console.log(logLine)
            }
        }

        return NextResponse.json({ success: true })
    } catch (error) {
        return NextResponse.json({ success: false, error: 'Invalid payload' }, { status: 400 })
    }
}
