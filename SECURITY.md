# Security and privacy

This utility reads sensitive local application metadata. Keep generated backups private even though the source code is public.

## Never publish

- `.codex`, `auth.json`, tokens, API keys, cookies or environment files.
- SQLite databases, WAL/SHM files, global-state JSON, session transcripts or backup directories.
- Unredacted command output, private project names, usernames, folder paths or screenshots of private conversations.

The tool uses no network library or remote service. Its backup routine copies only global-state candidates and a consistent SQLite snapshot. It intentionally excludes credential and session-transcript files. Other metadata can still be sensitive. The default backup directory is outside the repository; do not override it to a public checkout or shared folder.

`.gitignore` prevents some accidental Git additions. It does not protect files uploaded through a browser, force-added files, history, or data already published. If a credential is exposed, revoke/rotate it; deleting the latest file is insufficient.

## Execution

Review downloaded code. Start with `plan`. Keep the application and CLI closed while applying repairs from a normal external Windows terminal. Do not disable the sandbox or security software to make recovery run. Do not run unknown remote scripts via `curl | bash` or `irm | iex`. Never force-kill another person's session or unsaved work.

## Reporting

Use public issues only for redacted, non-sensitive descriptions. Do not attach a real database for reproduction. Include OS, Python version, application version if known, command used, a short redacted error and expected behavior. Reproduce schema issues with synthetic fixtures.

For a vulnerability requiring sensitive details, use GitHub private vulnerability reporting **if the repository owner has enabled it**. Otherwise request a private reporting channel without disclosing exploit details or credentials. This project does not claim a staffed security response service.
