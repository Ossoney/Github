'use client'

import { db } from '@/lib/db'
import { Button, Card, CardHeader, CardTitle, CardContent, useToast } from '@/components/ui/UI'
import { Trash2, AlertTriangle, Database, Download, FileSpreadsheet, Upload } from 'lucide-react'
import { exportToExcel, importFromExcel } from '@/lib/utils'
import { useLanguage } from '@/lib/i18n'
import { useLanguage } from '@/lib/i18n'

export function DataSettings() {
    const { addToast } = useToast()
    const { t } = useLanguage()

    const handleReset = async () => {
        if (confirm(t('nuclear_warning_1'))) {
            if (confirm(t('nuclear_warning_2'))) {
                await db.delete()
                window.location.reload()
            }
        }
    }

    const handleExport = async () => {
        const transactions = await db.transactions.toArray()
        const wallets = await db.wallets.toArray()
        const categories = await db.categories.toArray()
        exportToExcel(transactions, wallets, categories)
    }

    const handleImport = async (e) => {
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

        // Reset input
        e.target.value = ''
    }

    return (
        <div className="space-y-6">
            <Card className="border-slate-800 bg-slate-900/50">
                <CardHeader>
                    <CardTitle className="text-slate-200 flex items-center gap-2">
                        <FileSpreadsheet className="w-5 h-5 text-emerald-500" />
                        {t('backups')}
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                    {/* Export Section */}
                    <div className="space-y-2">
                        <h3 className="text-sm font-medium text-slate-300">{t('export_title')}</h3>
                        <p className="text-sm text-slate-400">
                            {t('export_desc')}
                        </p>
                        <Button
                            onClick={handleExport}
                            className="w-full bg-emerald-600 hover:bg-emerald-700 text-white"
                        >
                            <Download className="w-4 h-4 mr-2" />
                            {t('download_excel')}
                        </Button>
                    </div>

                    <div className="border-t border-slate-800 my-4" />

                    {/* Import Section */}
                    <div className="space-y-2">
                        <h3 className="text-sm font-medium text-slate-300">{t('import_title')}</h3>
                        <p className="text-sm text-slate-400">
                            {t('import_desc')} ⚠️ <strong>{t('import_warning')}</strong>
                        </p>
                        <div className="grid gap-2">
                            <input
                                type="file"
                                accept=".xlsx, .xls"
                                onChange={handleImport}
                                className="hidden"
                                id="import-file"
                            />
                            <label htmlFor="import-file">
                                <Button
                                    asChild
                                    variant="outline"
                                    className="w-full border-slate-700 hover:bg-slate-800 text-slate-300 cursor-pointer"
                                >
                                    <span>
                                        <Upload className="w-4 h-4 mr-2" />
                                        {t('select_file')}
                                    </span>
                                </Button>
                            </label>
                        </div>
                    </div>
                </CardContent>
            </Card>

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
