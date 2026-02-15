import { db } from './db'

export async function processRecurringTransactions() {
    const today = new Date()
    const currentDay = today.getDate()
    const currentMonth = today.getMonth()
    const currentYear = today.getFullYear()

    // Get all active recurring items
    const recurringItems = await db.recurring.where('active').equals('true').toArray() // Note: dexie stores boolean, query might need checking if 1/0, but trying boolean first

    // Fallback if index issue: getAll
    const allRecurring = await db.recurring.toArray()

    for (const item of allRecurring) {
        if (!item.active) continue

        const lastRun = item.lastRun ? new Date(item.lastRun) : null

        // Check if we should run it
        // Criteria: 
        // 1. It hasn't run this month (or never run)
        // 2. Today is >= scheduled day

        let shouldRun = false

        if (!lastRun) {
            // Never run. If today >= day, run it.
            if (currentDay >= item.dayOfMonth) shouldRun = true
        } else {
            // Has run before. Check if run in this month.
            const lastRunMonth = lastRun.getMonth()
            const lastRunYear = lastRun.getFullYear()

            if (lastRunYear < currentYear || (lastRunYear === currentYear && lastRunMonth < currentMonth)) {
                // Last run was previous month.
                // If today >= day, run it.
                if (currentDay >= item.dayOfMonth) shouldRun = true
            }
        }

        if (shouldRun) {
            console.log(`Running recurring transaction: ${item.description}`)

            await db.transaction('rw', db.transactions, db.wallets, db.recurring, async () => {
                // 1. Create Transaction
                await db.transactions.add({
                    walletId: item.walletId,
                    categoryId: item.categoryId,
                    amount: item.amount,
                    type: item.type,
                    description: item.description + ' (Recurrente)',
                    tags: ['#recurrente'],
                    date: new Date(), // Now
                })

                // 2. Update Wallet Balance
                const wallet = await db.wallets.get(item.walletId)
                if (wallet) {
                    const newBalance = item.type === 'income'
                        ? wallet.balance + item.amount
                        : wallet.balance - item.amount
                    await db.wallets.update(item.walletId, { balance: newBalance })
                }

                // 3. Update Last Run
                await db.recurring.update(item.id, { lastRun: new Date() })
            })
        }
    }
}
