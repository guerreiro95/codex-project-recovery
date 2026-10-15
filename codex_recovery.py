"""Unofficial Windows Codex project recovery. Standard library; no network."""
from __future__ import annotations

import argparse
from contextlib import closing
import ctypes
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import time

VERSION = '0.1.0'
LANGUAGES = {
    'pt': {
        'description': 'Recuperação local de projetos Codex. Prévia por padrão.',
        'preview': 'Prévia: nenhum arquivo foi alterado. Leia o plano antes de usar --apply.',
        'done': 'Concluído. Abra o Codex e confira os projetos. Backup anterior:',
        'closed': 'Feche completamente Codex/ChatGPT, inclusive a bandeja, antes de aplicar.',
        'sandbox': 'Reparo bloqueado no sandbox do Codex. Execute em terminal externo, após fechar o aplicativo.',
        'windows': 'Aplicação de reparos suportada somente no Windows.',
        'empty': 'Cadastro vazio ou inválido. Último backup válido preservado.',
        'schema': 'Banco ausente ou esquema não compatível. Nenhum reparo aplicado.',
        'watch': 'Backup ativo. Ctrl+C encerra. Janela de backup: até 15 minutos.',
        'error': 'Erro',
    },
    'en': {
        'description': 'Local Codex project recovery. Preview by default.',
        'preview': 'Preview: no files changed. Review the plan before using --apply.',
        'done': 'Completed. Open Codex and check projects. Previous backup:',
        'closed': 'Fully close Codex/ChatGPT, including the tray, before applying.',
        'sandbox': 'Repair blocked inside the Codex sandbox. Use an external terminal after closing the app.',
        'windows': 'Applying repairs is supported on Windows only.',
        'empty': 'Empty or invalid registry. Last good backup preserved.',
        'schema': 'Missing database or unsupported schema. No repair applied.',
        'watch': 'Backup active. Ctrl+C stops it. Backup window: up to 15 minutes.',
        'error': 'Error',
    },
    'zh': {
        'description': 'Codex 本地项目恢复。默认仅预览。',
        'preview': '预览：未修改任何文件。使用 --apply 前请检查方案。',
        'done': '已完成。打开 Codex 并检查项目。原始备份：',
        'closed': '应用恢复前，请完全关闭 Codex/ChatGPT，包括系统托盘中的程序。',
        'sandbox': '禁止在 Codex 沙盒中恢复。请关闭应用后在外部终端执行。',
        'windows': '仅支持在 Windows 上应用恢复。',
        'empty': '项目列表为空或无效。已保留上次有效备份。',
        'schema': '数据库不存在或结构不受支持。未应用恢复。',
        'watch': '备份正在运行。按 Ctrl+C 停止。备份间隔最长为 15 分钟。',
        'error': '错误',
    },
    'es': {
        'description': 'Recuperación local de proyectos Codex. Vista previa por defecto.',
        'preview': 'Vista previa: ningún archivo modificado. Revise el plan antes de usar --apply.',
        'done': 'Completado. Abra Codex y compruebe los proyectos. Copia anterior:',
        'closed': 'Cierre completamente Codex/ChatGPT, incluida la bandeja, antes de aplicar.',
        'sandbox': 'Recuperación bloqueada en el sandbox de Codex. Use un terminal externo después de cerrar la aplicación.',
        'windows': 'Aplicar la recuperación solo está soportado en Windows.',
        'empty': 'Registro vacío o inválido. Última copia válida conservada.',
        'schema': 'Base ausente o estructura incompatible. No se aplicó la recuperación.',
        'watch': 'Copia activa. Ctrl+C para detener. Intervalo de copia: hasta 15 minutos.',
        'error': 'Error',
    },
}


def timestamp():
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')


def read_json(path):
    value = json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(value, dict):
        raise ValueError('Expected a JSON object')
    return value


def atomic_write(path, raw):
    """Flush and sync a unique temporary file before replacing the target."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def write_json(path, value):
    atomic_write(path, json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8'))


def normalize(path):
    return str(path).removeprefix('\\\\?\\').replace('/', '\\').rstrip('\\').casefold()


def app_running():
    """Fail closed on enumeration errors; never trust sandbox process visibility."""
    from ctypes import wintypes
    class Entry(ctypes.Structure):
        _fields_ = [('size', wintypes.DWORD), ('usage', wintypes.DWORD),
                    ('pid', wintypes.DWORD), ('heap', ctypes.c_size_t),
                    ('module', wintypes.DWORD), ('threads', wintypes.DWORD),
                    ('parent', wintypes.DWORD), ('priority', wintypes.LONG),
                    ('flags', wintypes.DWORD), ('name', wintypes.WCHAR * 260)]
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(Entry)]
    kernel.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(Entry)]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.CreateToolhelp32Snapshot(2, 0)
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        entry = Entry()
        entry.size = ctypes.sizeof(entry)
        success = kernel.Process32FirstW(handle, ctypes.byref(entry))
        while success:
            if entry.name.casefold() in {'chatgpt.exe', 'codex.exe'}:
                return True
            success = kernel.Process32NextW(handle, ctypes.byref(entry))
        if ctypes.get_last_error() not in (0, 18):
            raise ctypes.WinError(ctypes.get_last_error())
        return False
    finally:
        kernel.CloseHandle(handle)


class Recovery:
    def __init__(self, home, backup_dir, lang='pt'):
        self.home = Path(home).expanduser().resolve()
        self.backups = Path(backup_dir).expanduser().resolve()
        if self.backups == self.home or self.home in self.backups.parents:
            raise ValueError('Backup directory must be outside CODEX_HOME')
        self.state = self.home / '.codex-global-state.json'
        self.database = self.home / 'state_5.sqlite'
        self.messages = LANGUAGES[lang]

    def connect(self):
        if not self.database.is_file():
            raise RuntimeError(self.messages['schema'])
        connection = sqlite3.connect(self.database.as_uri() + '?mode=ro', uri=True, timeout=10)
        connection.row_factory = sqlite3.Row
        return connection

    def historical(self):
        candidates = []
        for path in self.home.glob('*codex-global-state.json*'):
            if not path.is_file():
                continue
            try:
                data = read_json(path)
                projects = data.get('local-projects', {})
                assignments = data.get('thread-project-assignments', {})
                if isinstance(projects, dict) and projects and isinstance(assignments, dict):
                    candidates.append((len(projects), len(assignments), path.stat().st_mtime, path, data))
            except (OSError, ValueError):
                continue
        if not candidates:
            return {}
        return max(candidates, key=lambda item: item[:3])[4]

    def current(self):
        for path in (self.state, Path(str(self.state) + '.bak')):
            try:
                return read_json(path)
            except (OSError, ValueError):
                pass
        return {}

    def plan(self):
        current, old = self.current(), self.historical()
        try:
            with closing(self.connect()) as connection:
                if connection.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
                    raise RuntimeError('Database integrity check failed')
                projects = [dict(row) for row in connection.execute('SELECT * FROM projects ORDER BY position')]
                root_rows = list(connection.execute('SELECT project_id,path FROM project_roots ORDER BY position'))
                threads = list(connection.execute('SELECT id,cwd,source,project_id FROM threads'))
        except sqlite3.DatabaseError as error:
            raise RuntimeError(self.messages['schema']) from error
        if not projects:
            raise RuntimeError('No project records available; refusing an empty repair')
        host = 'local:' + str(self.home)
        maps = dict(current.get('app-server-project-id-by-legacy-project-id-by-host', {}))
        mapping = dict(old.get('app-server-project-id-by-legacy-project-id-by-host', {}).get(host, {}))
        mapping.update(maps.get(host, {}))
        inverse = {server: legacy for legacy, server in mapping.items()}
        roots = {}
        for row in root_rows:
            roots.setdefault(row['project_id'], []).append(row['path'])
        restored = dict(current.get('local-projects', {}))
        appearances = dict(current.get('project-appearances', {}))
        for project in projects:
            identifier = inverse.get(project['id'], project['id'])
            metadata = json.loads(project['metadata'])
            value = dict(old.get('local-projects', {}).get(identifier, {}))
            value.update(restored.get(identifier, {}))
            value.update(id=identifier, name=project['name'], rootPaths=roots.get(project['id'], []), createdAt=project['created_at_ms'], updatedAt=project['updated_at_ms'])
            restored[identifier] = value
            appearance = dict(old.get('project-appearances', {}).get(identifier, {}))
            if 'appearance.color' in metadata:
                appearance['color'] = metadata['appearance.color']
            if 'appearance.marker' in metadata:
                appearance['marker'] = json.loads(metadata['appearance.marker'])
            if appearance:
                appearances.setdefault(identifier, appearance)
            mapping[identifier] = project['id']
        assignments = dict(current.get('thread-project-assignments', {}))
        projectless = set(current.get('projectless-thread-ids', [])) | set(old.get('projectless-thread-ids', []))
        recovered, ambiguous = [], []
        server_to_local = {server: local for local, server in mapping.items()}
        for thread in threads:
            identifier = thread['id']
            if thread['source'] not in {'cli', 'vscode'} or identifier in assignments or identifier in projectless:
                continue
            previous = old.get('thread-project-assignments', {}).get(identifier, {})
            if thread['project_id'] in server_to_local:
                chosen, evidence = server_to_local[thread['project_id']], 'existing_database_assignment'
            elif previous.get('projectId') in restored and previous.get('projectKind') == 'local':
                chosen, evidence = previous['projectId'], 'explicit_historical_assignment'
            else:
                candidates = [p['id'] for p in restored.values() if any(normalize(root) == normalize(thread['cwd']) for root in p['rootPaths'])]
                if len(candidates) != 1:
                    if candidates:
                        ambiguous.append({'threadId': identifier, 'candidateProjectIds': candidates})
                    continue
                chosen, evidence = candidates[0], 'unique_exact_folder_inference'
            assignments[identifier] = {'projectKind': 'local', 'projectId': chosen}
            recovered.append({'threadId': identifier, 'projectId': chosen, 'evidence': evidence})
        maps[host] = mapping
        current.update({'local-projects': restored, 'project-appearances': appearances,
                        'app-server-project-id-by-legacy-project-id-by-host': maps,
                        'thread-project-assignments': assignments,
                        'projectless-thread-ids': sorted(projectless),
                        'thread-project-membership-host-ids': {**current.get('thread-project-membership-host-ids', {}), **{key: 'local' for key in assignments}},
                        'sidebar-project-thread-orders': {**old.get('sidebar-project-thread-orders', {}), **current.get('sidebar-project-thread-orders', {})}})
        order = [server_to_local[p['id']] for p in projects]
        current['project-order'] = list(dict.fromkeys(current.get('project-order', []) + order))
        migration = dict(current.get('app-server-projects-migration-by-host', {}))
        migration[host] = {**migration.get(host, {}), 'version': 1, 'projectsMigrated': True, 'threadAssignmentsMigrated': False, 'pendingThreadAssignmentIds': list(assignments)}
        current['app-server-projects-migration-by-host'] = migration
        report = {'version': VERSION, 'projects': len(restored), 'recoveredAssignments': len(recovered),
                  'ambiguousAssignments': len(ambiguous), 'assignmentEvidence': recovered,
                  'ambiguousThreads': ambiguous, 'databaseModified': False}
        return current, report

    def guard(self):
        if os.environ.get('CODEX_WINDOWS_SANDBOX_PACKAGE_FAMILY') or os.environ.get('CODEX_SANDBOX'):
            raise RuntimeError(self.messages['sandbox'])
        if sys.platform != 'win32':
            raise RuntimeError(self.messages['windows'])
        if app_running():
            raise RuntimeError(self.messages['closed'])

    def preserve(self, prefix='before-repair'):
        directory = self.backups / (prefix + '-' + timestamp())
        directory.mkdir(parents=True)
        # Preserve only global state files, never credentials or session transcripts.
        for path in self.home.glob('*codex-global-state.json*'):
            if path.is_file():
                atomic_write(directory / path.name, path.read_bytes())
        with closing(self.connect()) as source, closing(sqlite3.connect(directory / 'state.sqlite')) as target:
            source.backup(target)
            if target.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
                raise RuntimeError('Backup integrity check failed')
        return directory

    def apply(self):
        self.guard()
        state, report = self.plan()
        before = self.state.read_bytes() if self.state.exists() else None
        directory = self.preserve()
        write_json(directory / 'plan.json', report)
        self.guard()
        now = self.state.read_bytes() if self.state.exists() else None
        if now != before:
            raise RuntimeError('State changed during recovery; retry after closing all writers')
        raw = json.dumps(state, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        atomic_write(self.state, raw)
        atomic_write(Path(str(self.state) + '.bak'), raw)
        if read_json(self.state) != state:
            raise RuntimeError('Post-write verification failed; inspect the preserved backup')
        write_json(directory / 'result.json', report)
        return directory

    def backup(self):
        raw = self.state.read_bytes()
        state = json.loads(raw)
        if not isinstance(state, dict) or not isinstance(state.get('local-projects'), dict) or not state['local-projects']:
            raise ValueError(self.messages['empty'])
        protected = {key: value for key, value in state.items() if 'project' in key or key == 'remote-projects'}
        fingerprint = hashlib.sha256(json.dumps(protected, sort_keys=True).encode()).hexdigest()
        checkpoint = self.backups / 'last-good.json'
        try:
            if read_json(checkpoint).get('fingerprint') == fingerprint:
                return None
        except (OSError, ValueError):
            pass
        directory = self.preserve('snapshot')
        atomic_write(directory / 'global-state.json', raw)
        write_json(directory / 'manifest.json', {'version': VERSION, 'sha256': hashlib.sha256(raw).hexdigest(), 'projects': len(state['local-projects'])})
        write_json(checkpoint, {'fingerprint': fingerprint, 'directory': str(directory)})
        return directory

    def watch(self):
        print(self.messages['watch'], flush=True)
        previous, last = None, 0.0
        while True:
            try:
                state = read_json(self.state)
                count = len(state.get('local-projects', {}))
                if not count:
                    raise ValueError(self.messages['empty'])
                if previous is not None and count < previous:
                    write_json(self.backups / 'ATTENTION.json', {'time': timestamp(), 'event': 'project_count_decreased', 'previous': previous, 'current': count})
                if time.monotonic() - last >= 900:
                    self.backup()
                    last = time.monotonic()
                previous = count
            except (OSError, ValueError, RuntimeError, sqlite3.Error) as error:
                write_json(self.backups / 'ATTENTION.json', {'time': timestamp(), 'error': str(error), 'automaticRestore': False})
            time.sleep(30)


def main(argv=None):
    bootstrap = argparse.ArgumentParser(add_help=False)
    bootstrap.add_argument('--lang', choices=LANGUAGES, default='pt')
    language, _ = bootstrap.parse_known_args(argv)
    messages = LANGUAGES[language.lang]
    parser = argparse.ArgumentParser(description=messages['description'], parents=[bootstrap])
    parser.add_argument('action', choices=['plan', 'repair', 'preserve', 'backup', 'watch'], nargs='?', default='plan')
    parser.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))))
    parser.add_argument('--backup-dir', type=Path, default=Path.home() / 'Documents' / 'CodexProjectRecoveryBackups')
    parser.add_argument('--apply', action='store_true', help='write recovered state (repair only)')
    parser.add_argument('--version', action='version', version=VERSION)
    args = parser.parse_args(argv)
    if args.apply and args.action != 'repair':
        parser.error('--apply requires repair')
    recovery = Recovery(args.codex_home, args.backup_dir, args.lang)
    try:
        if args.action == 'plan' or (args.action == 'repair' and not args.apply):
            _, report = recovery.plan()
            print(messages['preview'])
            print(json.dumps(report, ensure_ascii=False, indent=2))
        elif args.action == 'repair':
            directory = recovery.apply()
            print(messages['done'], directory)
        elif args.action == 'preserve':
            print(recovery.preserve('incident'))
        elif args.action == 'backup':
            print(recovery.backup())
        else:
            recovery.watch()
    except KeyboardInterrupt:
        return 130
    except (OSError, ValueError, RuntimeError, sqlite3.Error) as error:
        print(messages['error'] + ': ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
