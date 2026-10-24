'use client'

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { db } from '@/lib/db'

const PinContext = createContext({
    isPinSet: false,
    isLocked: false,
    unlock: async () => false,
    setNewPin: async () => false,
    removePin: async () => false,
    lockApp: () => {},
})

// Función criptográfica local SHA-256 usando Web Crypto API nativa
async function hashPin(pin) {
    const encoder = new TextEncoder()
    const data = encoder.encode(`visualis_salt_${pin}`)
    const hashBuffer = await crypto.subtle.digest('SHA-256', data)
    const hashArray = Array.from(new Uint8Array(hashBuffer))
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
}

export function PinProvider({ children }) {
    const [isPinSet, setIsPinSet] = useState(false)
    const [isLocked, setIsLocked] = useState(false)
    const [isLoading, setIsLoading] = useState(true)

    // Comprobar estado del PIN al inicio
    useEffect(() => {
        let mounted = true
        const checkPin = async () => {
            try {
                const settings = await db.settings.get('global')
                if (!mounted) return
                if (settings?.pinHash) {
                    setIsPinSet(true)
                    // Si ya se había desbloqueado en la sesión actual de la pestaña, respetar
                    const sessionUnlocked = sessionStorage.getItem('visualis_unlocked') === 'true'
                    setIsLocked(!sessionUnlocked)
                } else {
                    setIsPinSet(false)
                    setIsLocked(false)
                }
            } catch (err) {
                console.error('Error checking PIN status:', err)
            } finally {
                if (mounted) setIsLoading(false)
            }
        }
        checkPin()
        return () => { mounted = false }
    }, [])

    const unlock = useCallback(async (enteredPin) => {
        try {
            const settings = await db.settings.get('global')
            if (!settings?.pinHash) {
                setIsLocked(false)
                return true
            }
            const enteredHash = await hashPin(enteredPin)
            if (enteredHash === settings.pinHash) {
                sessionStorage.setItem('visualis_unlocked', 'true')
                setIsLocked(false)
                return true
            }
            return false
        } catch (err) {
            console.error('Error verifying PIN:', err)
            return false
        }
    }, [])

    const setNewPin = useCallback(async (newPin) => {
        try {
            const hash = await hashPin(newPin)
            const settings = (await db.settings.get('global')) || { id: 'global' }
            await db.settings.put({
                ...settings,
                pinHash: hash,
                pinEnabled: true,
            })
            sessionStorage.setItem('visualis_unlocked', 'true')
            setIsPinSet(true)
            setIsLocked(false)
            return true
        } catch (err) {
            console.error('Error setting PIN:', err)
            return false
        }
    }, [])

    const removePin = useCallback(async (currentPin) => {
        try {
            const settings = await db.settings.get('global')
            if (settings?.pinHash) {
                const enteredHash = await hashPin(currentPin)
                if (enteredHash !== settings.pinHash) {
                    return false
                }
            }
            await db.settings.put({
                ...(settings || { id: 'global' }),
                pinHash: null,
                pinEnabled: false,
            })
            sessionStorage.removeItem('visualis_unlocked')
            setIsPinSet(false)
            setIsLocked(false)
            return true
        } catch (err) {
            console.error('Error removing PIN:', err)
            return false
        }
    }, [])

    const lockApp = useCallback(() => {
        sessionStorage.removeItem('visualis_unlocked')
        setIsLocked(true)
    }, [])

    return (
        <PinContext.Provider value={{ isPinSet, isLocked, isLoading, unlock, setNewPin, removePin, lockApp }}>
            {children}
        </PinContext.Provider>
    )
}

export function usePin() {
    return useContext(PinContext)
}
