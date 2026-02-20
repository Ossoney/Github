import { db, exportDB } from './db'

/**
 * Performs a daily local backup to localStorage if the feature is enabled.
 */
export async function processAutosave() {
    try {
        const settings = await db.settings.get('global')
        if (!settings || !settings.autosaveEnabled) return

        const lastAutosave = localStorage.getItem('visualis_last_autosave')
        const now = Date.now()
        const oneDay = 24 * 60 * 60 * 1000

        if (!lastAutosave || (now - parseInt(lastAutosave)) > oneDay) {
            console.log("Performing daily autosave...")
            const data = await exportDB()

            // We use a specific key for the daily backup
            // Limit size: Check if it fits (localStorage limit is ~5-10MB)
            const jsonData = JSON.stringify(data)

            try {
                localStorage.setItem('visualis_autosave_backup', jsonData)
                localStorage.setItem('visualis_last_autosave', now.toString())
                console.log("Autosave completed successfully.")
            } catch (e) {
                console.warn("Autosave failed (likely storage full):", e)
            }
        }
    } catch (err) {
        console.error("Error in autosave process:", err)
    }
}
