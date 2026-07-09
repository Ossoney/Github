import { Modal } from '@/components/ui/Modal'
import { Button } from '@/components/ui/Button'
import { AlertTriangle } from 'lucide-react'
import { useLanguage } from '@/lib/i18n'

export function ConfirmDialog({ isOpen, onClose, onConfirm, title, message, type = 'danger' }) {
    const { t } = useLanguage()

    return (
        <Modal isOpen={isOpen} onClose={onClose} title={title || t('confirm_action')} className="max-w-sm">
            <div className="space-y-4">
                <div className="flex items-start gap-4">
                    <div className="p-2 bg-rose-500/10 rounded-full text-rose-500 shrink-0">
                        <AlertTriangle className="w-6 h-6" />
                    </div>
                    <div className="space-y-1">
                        <p className="text-sm text-slate-300 leading-relaxed">
                            {message}
                        </p>
                    </div>
                </div>

                <div className="flex gap-3 justify-end pt-2">
                    <Button variant="ghost" onClick={onClose}>
                        {t('cancel')}
                    </Button>
                    <Button
                        variant={type === 'danger' ? 'destructive' : 'default'}
                        onClick={() => {
                            onConfirm()
                            onClose()
                        }}
                    >
                        {t('confirm')}
                    </Button>
                </div>
            </div>
        </Modal>
    )
}
