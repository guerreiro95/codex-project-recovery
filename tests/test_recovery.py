"""Synthetic fixtures only. Tests never read the user's Codex state."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('recovery', Path(__file__).resolve().parents[1] / 'codex_recovery.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / 'home'
        self.home.mkdir()
        self.tool = module.Recovery(self.home, self.root / 'backups')
        self.tool.state.write_text(json.dumps({'local-projects': {}, 'unrelated-preference': {'enabled': True}}), encoding='utf-8')
        with contextlib.closing(sqlite3.connect(self.tool.database)) as connection, connection:
            connection.executescript('''
                CREATE TABLE projects(id TEXT PRIMARY KEY,name TEXT,metadata TEXT,position INTEGER,created_at_ms INTEGER,updated_at_ms INTEGER);
                CREATE TABLE project_roots(project_id TEXT,position INTEGER,path TEXT);
                CREATE TABLE threads(id TEXT PRIMARY KEY,cwd TEXT,source TEXT,project_id TEXT);
                INSERT INTO projects VALUES('project-one','Example','{}',0,1000,1000);
                INSERT INTO project_roots VALUES('project-one',0,'C:\\example');
                INSERT INTO threads VALUES('thread-one','C:\\example','cli',NULL);
            ''')

    def test_preview_preserves_data_and_database_bytes(self):
        state_before, database_before = self.tool.state.read_bytes(), self.tool.database.read_bytes()
        state, report = self.tool.plan()
        self.assertEqual(report['projects'], 1)
        self.assertEqual(report['recoveredAssignments'], 1)
        self.assertEqual(state['unrelated-preference'], {'enabled': True})
        self.assertEqual(self.tool.state.read_bytes(), state_before)
        self.assertEqual(self.tool.database.read_bytes(), database_before)
        self.assertFalse(self.tool.backups.exists())

    def test_ambiguous_folder_never_auto_assigned(self):
        with contextlib.closing(sqlite3.connect(self.tool.database)) as connection, connection:
            connection.execute("INSERT INTO projects VALUES('project-two','Other','{}',1,2000,2000)")
            connection.execute("INSERT INTO project_roots VALUES('project-two',0,'C:\\example')")
        state, report = self.tool.plan()
        self.assertEqual(report['ambiguousAssignments'], 1)
        self.assertNotIn('thread-one', state['thread-project-assignments'])

    def test_projectless_and_subagents_excluded(self):
        state = json.loads(self.tool.state.read_text())
        state['projectless-thread-ids'] = ['thread-one']
        self.tool.state.write_text(json.dumps(state))
        with contextlib.closing(sqlite3.connect(self.tool.database)) as connection, connection:
            connection.execute("INSERT INTO threads VALUES('agent','C:\\example','subagent',NULL)")
        _, report = self.tool.plan()
        self.assertEqual(report['recoveredAssignments'], 0)

    def test_historical_ids_are_preserved(self):
        host = 'local:' + str(self.home.resolve())
        old = {'local-projects': {'legacy-one': {'id': 'legacy-one'}},
               'app-server-project-id-by-legacy-project-id-by-host': {host: {'legacy-one': 'project-one'}},
               'thread-project-assignments': {'thread-one': {'projectKind': 'local', 'projectId': 'legacy-one'}}}
        (self.home / '..codex-global-state.json.old.tmp').write_text(json.dumps(old))
        state, report = self.tool.plan()
        self.assertIn('legacy-one', state['local-projects'])
        self.assertEqual(report['assignmentEvidence'][0]['evidence'], 'explicit_historical_assignment')

    def test_corrupt_state_can_be_planned_from_sqlite(self):
        self.tool.state.write_bytes(b'\x00' * 32)
        state, report = self.tool.plan()
        self.assertEqual(report['projects'], 1)
        self.assertIn('project-one', state['local-projects'])

    def test_missing_database_does_not_create_database(self):
        self.tool.database.unlink()
        with self.assertRaises(RuntimeError):
            self.tool.plan()
        self.assertFalse(self.tool.database.exists())

    def test_live_app_and_sandbox_refuse_writes(self):
        with patch.dict(os.environ, {'CODEX_WINDOWS_SANDBOX_PACKAGE_FAMILY': 'test'}):
            with self.assertRaisesRegex(RuntimeError, 'sandbox'):
                self.tool.apply()
        with patch.dict(os.environ, {}, clear=True), patch.object(module.sys, 'platform', 'win32'), patch.object(module, 'app_running', return_value=True):
            with self.assertRaises(RuntimeError):
                self.tool.apply()
        self.assertFalse(self.tool.backups.exists())

    def test_apply_has_backup_and_never_updates_database(self):
        database_before = self.tool.database.read_bytes()
        with patch.object(self.tool, 'guard'):
            directory = self.tool.apply()
        self.assertTrue((directory / 'state.sqlite').exists())
        self.assertTrue((directory / self.tool.state.name).exists())
        self.assertEqual(self.tool.database.read_bytes(), database_before)
        self.assertIn('project-one', module.read_json(self.tool.state)['local-projects'])
        self.assertEqual(self.tool.state.read_bytes(), Path(str(self.tool.state) + '.bak').read_bytes())
        with contextlib.closing(sqlite3.connect(directory / 'state.sqlite')) as connection:
            self.assertEqual(connection.execute('PRAGMA quick_check').fetchone()[0], 'ok')

    def test_state_change_during_repair_aborts(self):
        def preserve(*args):
            directory = self.root / 'preserved'
            directory.mkdir()
            self.tool.state.write_text('{"concurrent": true}')
            return directory
        with patch.object(self.tool, 'guard'), patch.object(self.tool, 'preserve', side_effect=preserve):
            with self.assertRaisesRegex(RuntimeError, 'State changed'):
                self.tool.apply()
        self.assertEqual(module.read_json(self.tool.state), {'concurrent': True})

    def test_invalid_and_empty_states_preserve_last_good_checkpoint(self):
        checkpoint = self.tool.backups / 'last-good.json'
        module.write_json(checkpoint, {'fingerprint': 'known-good'})
        for raw in (b'{}', b'\x00\x00', b'[]'):
            self.tool.state.write_bytes(raw)
            with self.assertRaises(ValueError):
                self.tool.backup()
            self.assertEqual(module.read_json(checkpoint), {'fingerprint': 'known-good'})

    def test_snapshot_deduplicates_registry_not_volatile_preferences(self):
        state, _ = self.tool.plan()
        module.write_json(self.tool.state, state)
        first = self.tool.backup()
        self.assertTrue((first / 'manifest.json').exists())
        state['unrelated-preference'] = 'changed'
        module.write_json(self.tool.state, state)
        self.assertIsNone(self.tool.backup())

    def test_credentials_and_transcripts_never_copied(self):
        (self.home / 'auth.json').write_text('SECRET-NOT-FOR-BACKUP')
        (self.home / 'session.jsonl').write_text('PRIVATE-TRANSCRIPT')
        directory = self.tool.preserve()
        self.assertFalse((directory / 'auth.json').exists())
        self.assertFalse((directory / 'session.jsonl').exists())

    def test_backup_directory_cannot_be_codex_home(self):
        for path in (self.home, self.home / 'backups'):
            with self.assertRaises(ValueError):
                module.Recovery(self.home, path)

    def test_cli_languages(self):
        for language in module.LANGUAGES:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                result = module.main(['plan', '--lang', language, '--codex-home', str(self.home), '--backup-dir', str(self.root / 'backups')])
            self.assertEqual(result, 0)
            self.assertIn(module.LANGUAGES[language]['preview'], output.getvalue())

    def test_cli_defaults_to_english(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            result = module.main(['plan', '--codex-home', str(self.home), '--backup-dir', str(self.root / 'backups')])
        self.assertEqual(result, 0)
        self.assertIn(module.LANGUAGES['en']['preview'], output.getvalue())


if __name__ == '__main__':
    unittest.main()
