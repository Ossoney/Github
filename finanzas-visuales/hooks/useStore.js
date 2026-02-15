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
    openTransactionModal: (tx = null) => set({ isTransactionModalOpen: true, editingTransaction: tx }),
    closeTransactionModal: () => set({ isTransactionModalOpen: false, editingTransaction: null }),

    isTagModalOpen: false,
    openTagModal: () => set({ isTagModalOpen: true }),
    closeTagModal: () => set({ isTagModalOpen: false }),

    // Filters (Global)
    selectedWalletId: null, // null = All wallets
    setSelectedWalletId: (id) => set({ selectedWalletId: id }),
}));
