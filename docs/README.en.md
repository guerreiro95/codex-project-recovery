# Codex Project Recovery

[English](README.en.md) · [Português](README.pt.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md)

Recover project organization in **Codex Desktop for Windows** when sidebar projects disappear but conversations remain in Recents.

Independent, unofficial community utility. Python 3.10+, standard library only. No server, API, telemetry or network connection in the utility code.

> **Preview first.** Applying a repair changes internal Codex state files. Preserve a backup, close the app, then explicitly use `--apply`. Recovery is not universally guaranteed, nor can future corruption be prevented absolutely.

## Capabilities and scope

The tool rebuilds the local registry from existing SQLite project records, preserves known historical IDs, retains current preferences and explicitly projectless conversations, and creates a consistent database backup before repairing global-state JSON. It never writes directly to the original SQLite database.

Historical backups are independent of the application's immediate `.bak`. Empty or invalid registries do not replace the last good backup reference. The tool does not recover deleted source files, missing session transcripts, remote/cloud projects or another computer's data.

This project originated in a real recovery involving JSON corruption and unclean shutdowns. That observation is not a diagnosis of every missing-project incident. See [technical details](HOW_IT_WORKS.md).

## Requirements

- Windows 10/11 for applying repairs; Python 3.10 or newer.
- PowerShell, Command Prompt or Git Bash **on Windows**.
- `state_5.sqlite` with compatible `projects`, `project_roots` and `threads` tables.
- macOS, Linux and WSL repair are unsupported in this release.

Codex internal schemas can change. An incompatible schema stops recovery. Synthetic tests do not prove compatibility with every application version.

## Download and preview — no Git required

1. Click **Code → Download ZIP** on this repository's GitHub page.
2. Extract the entire ZIP. Do not run files inside the archive.
3. Install Python 3.10+ from the [official website](https://www.python.org/downloads/windows/) if necessary.
4. Open the extracted folder in File Explorer. Type `powershell` in its address bar and press Enter.
5. Preview:

```powershell
py -3 .\codex_recovery.py plan --lang en
```

If `py` is unavailable, replace `py -3` with `python`; confirm it is Python 3.10+. Double-clicking `codex-recovery.cmd` also previews and keeps the window open. Without `--lang`, English is the default.

## Apply

1. Review `projects`, `recoveredAssignments` and `ambiguousAssignments` in the preview. Shared-folder ambiguities are not assigned automatically.
2. Save work. Fully close Codex/ChatGPT, including the tray, and close Codex CLI sessions.
3. In an **external Windows terminal**, from the extracted folder:

```powershell
py -3 .\codex_recovery.py repair --apply --lang en
```

4. Wait for confirmation. Reopen Codex and verify projects and conversations in its UI.

If an error occurs, preserve the reported backup rather than repeatedly applying repairs. A remaining `codex.exe` process blocks repair; close sessions normally without terminating unsaved work. `result.json` confirms the write, not successful migration by every future version of the app.

### Git Bash on Windows

```bash
python ./codex_recovery.py plan --lang en
# After saving work and closing the desktop app and Codex CLI:
python ./codex_recovery.py repair --apply --lang en
```

Use `py -3` if needed. These are **Windows Git Bash**, not Linux/WSL commands. Do not use blind remote execution, `curl | bash`, or commands that disable security protections.

## Ask your AI/Codex

Use the [English prompt](AI_PROMPTS.md#english). Ask the AI to inspect the code and run only the preview first. When the agent is inside Codex or a sandbox, it must provide the apply command for an external terminal instead of bypassing process guards.

Do not upload credentials, real databases, transcripts or backup files to an AI service to simplify diagnosis. Recovery runs locally.

## Backups

```powershell
py -3 .\codex_recovery.py preserve --lang en
py -3 .\codex_recovery.py backup --lang en
py -3 .\codex_recovery.py watch --lang en
```

`preserve` saves incident state even when the JSON is corrupted. `backup` snapshots a valid registry. `watch` runs until Ctrl+C or the terminal closes.

Default destination: `Documents\CodexProjectRecoveryBackups` under your Windows user profile. Override it using `--backup-dir`; never choose `.codex`, this public checkout or a shared folder. Override the Codex data home with `--codex-home`; otherwise the tool uses `CODEX_HOME` or `~/.codex`.

Watch mode checks every 30 seconds and attempts a new historical snapshot every 15 minutes when protected project state changes. It writes `ATTENTION.json` on errors or a drop in project count. It does not display Windows notifications, automatically restore data or delete old backups. Monitor disk space and keep a protected second copy on an independent device.

**The public edition does not install login startup automatically.** To run at login, create a shortcut targeting `python.exe` with the full script path and `watch --lang en`, then put it in the folder opened by **Win+R → `shell:startup`**. Keep the script in place and run only one watcher. Backups require an active watcher; the potential loss window is up to 15 minutes.

To restore a specific known-good snapshot, close all writers and preserve current state before manually replacing the primary JSON and `.bak` using that snapshot's validated `global-state.json`. **Do not overwrite the whole database over newer conversations.** This release has no automatic snapshot restore command; seek help using redacted information if unsure.

## Languages

The repository homepage starts in English and includes expandable translations in the same README. CLI messages support `--lang pt|en|zh|es`. JSON keys and some low-level technical errors remain English. Simplified Chinese uses `zh`/`zh-CN`, not `CH`.

## Privacy and contribution

Publishing this source code grants no access to your machine or private repositories. Other users run it on their own local data. Generated backups can contain private names, paths, metadata and conversation indexes. The tool excludes `auth.json` and session transcripts, but other backup content still remains private.

Never publish `.codex`, databases, backups, unredacted logs or personal screenshots. `.gitignore` helps with Git commits; **it does not stop manual browser uploads or remove published history**. Read [SECURITY.md](../SECURITY.md).

Run tests with `python -m unittest discover -s tests -v`. GitHub CI covers Windows and Linux synthetic tests; Linux testing does not mean Linux repair is supported. Contributions: [CONTRIBUTING.md](../CONTRIBUTING.md). License: [MIT](../LICENSE). No OpenAI affiliation or official support.
