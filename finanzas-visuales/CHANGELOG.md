# Project Changelog

## [Unreleased]

### Added

- **Local-First Architecture**: Adopted IndexedDB (via Dexie.js) for privacy and offline speed.
- **Expenless-Inspired Features**: Wallet system, Visual budget alerts, Excel export.

### Changed

- **Database Strategy**: Dropped Supabase in favor of local IndexedDB to meet "Local First" and speed requirements.
- **UI Philosophy**: Focus on "Speed First" and "Visual Feedback" (progress bars).

### Deprecated

- `supabase_schema.sql` and `lib/supabase.js` are no longer needed for the initial version.
