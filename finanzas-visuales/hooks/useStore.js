import { create } from 'zustand';

export const useStore = create((set) => ({
    // Date Navigation
    currentDate: new Date(),
    setCurrentDate: (date) => set({ currentDate: date }),
    nextMonth: () => set((state) => {
        const next = new Date(state.currentDate)
        next.setMonth(next.getMonth() + 1)
        return { currentDate: next }
    }),
    prevMonth: () => set((state) => {
        const prev = new Date(state.currentDate)
        prev.setMonth(prev.getMonth() - 1)
        return { currentDate: prev }
    }),

    // UI State
    isTransactionModalOpen: false,
    editingTransaction: null,
    newTransactionType: 'expense', // Default new transaction type
    openTransactionModal: (tx = null, type = 'expense') => set({ isTransactionModalOpen: true, editingTransaction: tx, newTransactionType: type }),
    closeTransactionModal: () => set({ isTransactionModalOpen: false, editingTransaction: null }),

    isTagModalOpen: false,
    openTagModal: () => set({ isTagModalOpen: true }),
    closeTagModal: () => set({ isTagModalOpen: false }),

    // Filters (Global)
    selectedWalletId: null, // null = All wallets
    setSelectedWalletId: async (id) => {
        set({ selectedWalletId: id });
        try {
            const { db } = await import('@/lib/db');
            const settings = await db.settings.get('global') || { id: 'global' };
            await db.settings.put({ ...settings, lastSelectedWalletId: id });
        } catch (e) {
            console.error("Failed to persist selectedWalletId:", e);
        }
    },
}));
