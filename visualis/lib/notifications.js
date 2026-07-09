'use client'

/**
 * Utility to handle browser notifications in a Local-First environment.
 */

export const requestNotificationPermission = async () => {
    if (!('Notification' in window)) {
        console.warn('This browser does not support notifications.');
        return false;
    }

    if (Notification.permission === 'granted') return true;

    if (Notification.permission !== 'denied') {
        const permission = await Notification.requestPermission();
        return permission === 'granted';
    }

    return false;
};

export const sendNotification = (title, options = {}) => {
    if (!('Notification' in window) || Notification.permission !== 'granted') {
        return;
    }

    const defaultOptions = {
        icon: '/icon.svg',
        badge: '/icon.svg',
        silent: false,
    };

    return new Notification(title, { ...defaultOptions, ...options });
};

/**
 * Check habits and trigger notifications if needed.
 * This runs on app load or periodically if the app is open.
 */
export const checkHabitReminders = async (db) => {
    if (typeof window === 'undefined') return;
    
    // We only check if permission is granted
    if (Notification.permission !== 'granted') return;

    const now = new Date();
    const currentTime = formatTime(now); // "HH:mm"
    
    try {
        const habits = await db.habits
            .where('reminderTime').equals(currentTime)
            .and(h => h.reminderEnabled)
            .toArray();
        
        for (const habit of habits) {
            // Check if already notified today to prevent spamming within the same minute
            const lastNotified = localStorage.getItem(`last_notified_${habit.id}`);
            const todayStr = now.toDateString();
            
            if (lastNotified !== todayStr) {
                sendNotification(`¡Hora de tu hábito: ${habit.name}!`, {
                    body: `Tienes como meta ${habit.goal} veces por semana. ¡Tú puedes!`,
                    tag: `habit_${habit.id}`
                });
                localStorage.setItem(`last_notified_${habit.id}`, todayStr);
            }
        }
    } catch (err) {
        console.error('Error checking reminders:', err);
    }
};

const formatTime = (date) => {
    const h = String(date.getHours()).padStart(2, '0');
    const m = String(date.getMinutes()).padStart(2, '0');
    return `${h}:${m}`;
};
