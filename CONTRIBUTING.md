# Contributing

Contributions in Portuguese, English, Simplified Chinese and Spanish are welcome.

1. Open a focused issue or pull request explaining the observed problem and expected behavior.
2. Use synthetic databases and state files. Never commit a real user's data.
3. Preserve the preview-first workflow and the prohibition on direct writes to the original SQLite database.
4. Add tests for meaningful behavior changes, particularly schema compatibility, process guards and write ordering.
5. Run `python -m unittest discover -s tests -v`.
6. Update all four READMEs when commands, supported systems, safety limits or user-visible behavior change. JSON field names stay stable across languages.

Keep dependencies in the Python standard library unless an added dependency is necessary and justified. Do not add telemetry, upload diagnostics or automatic restoration without an explicit design discussion.

Compatibility claims require evidence from a known application version. CI with synthetic fixtures alone does not establish application compatibility. Contributions are licensed under the repository's MIT license.
