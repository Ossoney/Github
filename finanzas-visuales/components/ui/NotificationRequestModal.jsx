'use client'
import React from 'react'
import { Modal, Button } from '@/components/ui/UI'
import { Bell, ShieldCheck, XCircle } from 'lucide-react'
import { useLanguage } from '@/lib/i18n'
import { requestNotificationPermission } from '@/lib/notifications'
import { useToast } from '@/components/ui/UI'

export function NotificationRequestModal({ isOpen, onClose, onPermissionGranted }) {
    const { t } = useLanguage()
    const { addToast } = useToast()

    const handleRequest = async () => {
        const granted = await requestNotificationPermission()
        if (granted) {
            addToast(t('notifications_granted'), 'success')
            if (onPermissionGranted) onPermissionGranted()
            onClose()
        } else {
            addToast(t('notifications_denied'), 'error')
            onClose()
        }
    }

    return (
        <Modal 
            isOpen={isOpen} 
            onClose={onClose} 
            title={t('notifications_title')} 
            className="max-w-sm border-sky-500/20 shadow-sky-500/10"
        >
            <div className="flex flex-col items-center text-center space-y-6 py-4">
                <div className="relative">
                    <div className="w-20 h-20 rounded-full bg-sky-500/10 flex items-center justify-center animate-pulse">
                        <Bell className="w-10 h-10 text-sky-500" />
                    </div>
                    <div className="absolute -bottom-1 -right-1 bg-slate-900 rounded-full p-1 border-2 border-slate-900">
                        <ShieldCheck className="w-6 h-6 text-emerald-500" />
                    </div>
                </div>

                <div className="space-y-2">
                    <p className="text-slate-300 text-sm leading-relaxed px-2">
                        {t('notifications_desc')}
                    </p>
                </div>

                <div className="flex flex-col w-full gap-3 pt-4">
                    <Button 
                        onClick={handleRequest}
                        className="w-full py-6 text-base font-bold bg-sky-500 hover:bg-sky-600 shadow-sky-500/40"
                    >
                        {t('notifications_btn')}
                    </Button>
                    <Button 
                        variant="ghost" 
                        onClick={onClose}
                        className="text-slate-500 hover:text-slate-300"
                    >
                        {t('notifications_cancel')}
                    </Button>
                </div>
            </div>
        </Modal>
    )
}
