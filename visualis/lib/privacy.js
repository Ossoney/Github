'use client'

import { createContext, useContext, useState, useEffect } from 'react'
import { db } from '@/lib/db'

const PrivacyContext = createContext({
    isPrivacyMode: false,
    togglePrivacyMode: () => { }
})

export function PrivacyProvider({ children }) {
    const [isPrivacyMode, setIsPrivacyMode] = useState(false)
    const [isLoaded, setIsLoaded] = useState(false)

    useEffect(() => {
        // Load initial state
        const loadSettings = async () => {
            try {
                const settings = await db.settings.get('global')
                if (settings?.privacyMode) {
                    setIsPrivacyMode(true)
                }
            } catch (e) {
                console.error("Error loading privacy settings:", e)
            } finally {
                setIsLoaded(true)
            }
        }
        loadSettings()
    }, [])

    const togglePrivacyMode = async () => {
        const newMode = !isPrivacyMode
        setIsPrivacyMode(newMode)

        try {
            const exists = await db.settings.get('global')
            if (exists) {
                await db.settings.update('global', { privacyMode: newMode })
            } else {
                await db.settings.put({ id: 'global', privacyMode: newMode })
            }
        } catch (e) {
            console.error("Failed to save privacy mode", e)
        }
    }

    // Optional: Avoid rendering children until settings are loaded to prevent "flash" of private data?
    // Or just let it default to visible (false) and switch.
    // Defaulting to false is safer for UX (user sees data by default).

    return (
        <PrivacyContext.Provider value={{ isPrivacyMode, togglePrivacyMode }}>
            {children}
        </PrivacyContext.Provider>
    )
}

export const usePrivacy = () => useContext(PrivacyContext)
