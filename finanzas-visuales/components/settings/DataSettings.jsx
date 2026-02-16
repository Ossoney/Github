'use client'

import { db, exportDB, importDB } from '@/lib/db'
import { Button, Card, CardHeader, CardTitle, CardContent, useToast } from '@/components/ui/UI'
import { Trash2, AlertTriangle, Database, Download, FileSpreadsheet, Upload, Shield, Save, RefreshCw } from 'lucide-react'
import { exportToExcel, importFromExcel } from '@/lib/utils'
import { useLanguage } from '@/lib/i18n'

export function DataSettings() {
    const { addToast } = useToast()
    const { t } = useLanguage()

    // --- NUCLEAR RESET ---
    const handleReset = async () => {
        if (confirm(t('nuclear_warning_1'))) {
            if (confirm(t('nuclear_warning_2'))) {
                await db.delete()
                window.location.reload()
            }
        }
    }

    // --- JSON BACKUP (Full DB) ---
    const handleBackupCreate = async () => {
        try {
            const data = await exportDB()
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
            const url = URL.createObjectURL(blob)

            const date = new Date().toISOString().split('T')[0]
            const a = document.createElement('a')
            a.href = url
            a.download = `visualis-backup-${date}.json`
            document.body.appendChild(a)
            a.click()
            document.body.removeChild(a)
            URL.revokeObjectURL(url)

            addToast(t('backup_created') || 'Backup created', 'success')
        } catch (error) {
            console.error(error)
            addToast('Error creating backup', 'error')
        }
    }

    const handleBackupRestore = async (e) => {
        const file = e.target.files[0]
        if (!file) return

        if (confirm(t('restore_confirm'))) {
            const reader = new FileReader()
            reader.onload = async (event) => {
                try {
                    const json = JSON.parse(event.target.result)
                    await importDB(json)
                    addToast(t('json_restore_success'), 'success')
                    setTimeout(() => window.location.reload(), 1500)
                } catch (error) {
                    console.error(error)
                    addToast(t('json_restore_error') + error.message, 'error')
                }
            }
            reader.readAsText(file)
        }
        e.target.value = ''
    }

    // --- EXCEL DATA (Interoperability) ---
    const handleExcelExport = async () => {
        const transactions = await db.transactions.toArray()
        const wallets = await db.wallets.toArray()
        const categories = await db.categories.toArray()
        exportToExcel(transactions, wallets, categories)
    }

    const handleExcelImport = async (e) => {
        const file = e.target.files[0]
        if (!file) return

        if (confirm(t('import_confirm').replace('{fileName}', file.name))) {
            try {
                const result = await importFromExcel(file)
                addToast(t('import_success').replace('{count}', result.count), 'success')
                setTimeout(() => window.location.reload(), 2000)
            } catch (error) {
                addToast(t('import_error') + error.message, 'error')
            }
        }
        e.target.value = ''
    }

    return (
        <div className="space-y-8">

            {/* 1. SECURITY / BACKUPS */}
            <Card className="border-slate-800 bg-slate-900/50">
                <CardHeader>
                    <CardTitle className="text-slate-200 flex items-center gap-2">
                        <Shield className="w-5 h-5 text-blue-500" />
                        {t('security_title')}
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                    {/* Create Backup */}
                    <div className="space-y-2">
                        <h3 className="text-sm font-medium text-slate-300">{t('backup_create')}</h3>
                        <p className="text-sm text-slate-400">
                            {t('backup_desc')}
                        </p>
                        <Button
                            onClick={handleBackupCreate}
                            className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                        >
                            <Save className="w-4 h-4 mr-2" />
                            {t('json_backup_title')}
                        </Button>
                    </div>

                    <div className="border-t border-slate-800" />

                    {/* Restore Backup */}
                    <div className="space-y-2">
                        <h3 className="text-sm font-medium text-slate-300">{t('restore_title')}</h3>
                        <p className="text-sm text-slate-400">
                            {t('restore_desc')}
                        </p>
                        <div className="grid gap-2">
                            <input
                                type="file"
                                accept=".json"
                                onChange={handleBackupRestore}
                                className="hidden"
                                id="restore-file"
                            />
                            <label htmlFor="restore-file">
                                <Button
                                    as="div"
                                    variant="outline"
                                    className="w-full border-slate-700 hover:bg-slate-800 text-slate-300 cursor-pointer"
                                >
                                    <RefreshCw className="w-4 h-4 mr-2" />
                                    {t('restore_title')}
                                </Button>
                            </label>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* 2. EXCEL DATA */}
            <Card className="border-slate-800 bg-slate-900/50">
                <CardHeader>
                    <CardTitle className="text-slate-200 flex items-center gap-2">
                        <FileSpreadsheet className="w-5 h-5 text-emerald-500" />
                        {t('excel_data_title')}
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                    <p className="text-sm text-slate-400">
                        {t('excel_data_desc')}
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <Button
                            onClick={handleExcelExport}
                            className="w-full bg-emerald-600 hover:bg-emerald-700 text-white"
                        >
                            <Download className="w-4 h-4 mr-2" />
                            {t('download_excel')}
                        </Button>

                        <div>
                            <input
                                type="file"
                                accept=".xlsx, .xls"
                                onChange={handleExcelImport}
                                className="hidden"
                                id="import-excel"
                            />
                            <label htmlFor="import-excel">
                                <Button
                                    as="div"
                                    variant="outline"
                                    className="w-full border-slate-700 hover:bg-slate-800 text-slate-300 cursor-pointer"
                                >
                                    <Upload className="w-4 h-4 mr-2" />
                                    {t('import_excel')}
                                </Button>
                            </label>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* 3. DANGER ZONE */}
            <Card className="border-red-900/50 bg-red-950/10">
                <CardHeader>
                    <CardTitle className="text-red-500 flex items-center gap-2">
                        <AlertTriangle className="w-5 h-5" />
                        {t('danger_zone')}
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <p className="text-sm text-slate-400">
                        {t('danger_desc')}
                    </p>

                    <Button
                        variant="destructive"
                        onClick={handleReset}
                        className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-6 group relative overflow-hidden transition-all hover:scale-[1.02]"
                    >
                        <div className="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_10px,rgba(0,0,0,0.1)_10px,rgba(0,0,0,0.1)_20px)] opacity-50" />
                        <span className="flex items-center gap-2 relative z-10 text-lg uppercase tracking-widest">
                            <Trash2 className="w-6 h-6 animate-pulse" />
                            {t('nuclear_button')}
                        </span>
                    </Button>
                </CardContent>
            </Card>
        </div>
    )
}
