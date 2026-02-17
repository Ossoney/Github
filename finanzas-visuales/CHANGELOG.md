# Project Changelog

## [1.1.31] - Unreleased

### Added

- **Local-First Architecture**: Adopted IndexedDB (via Dexie.js) for privacy and offline speed.
- **Expenless-Inspired Features**: Wallet system, Visual budget alerts, Excel export.
- **Privacy Mode**: Toggle to hide sensitive financial amounts.
- **Split Transactions**: Added wizard to split a single transaction into multiple categories.
- **Smart Context**: "Add Transaction" button defaults to Income/Expense based on current view.
- **Smart Intervals**: History breakdown options (6m/12m/24m) hidden when no data is available.

### Changed

- **Database Strategy**: Dropped Supabase in favor of local IndexedDB to meet "Local First" and speed requirements.
- **UI Philosophy**: Focus on "Speed First" and "Visual Feedback" (progress bars).

### Deprecated

- `supabase_schema.sql` and `lib/supabase.js` are no longer needed for the initial version.
