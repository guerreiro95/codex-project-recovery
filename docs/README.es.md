# Codex Project Recovery

[Português (predeterminado)](../README.md) · [English](README.en.md) · [简体中文](README.zh-CN.md) · **Español**

Recupere la organización de proyectos en **Codex Desktop para Windows** cuando desaparecen de la barra lateral, pero las conversaciones siguen en Recientes.

Herramienta comunitaria independiente y no oficial. Python 3.10+, solo biblioteca estándar. Sin servidor, API, telemetría ni conexión de red en el código de la herramienta.

> **Primero, vista previa.** Aplicar una recuperación modifica archivos internos de Codex. Conserve una copia, cierre la aplicación y use explícitamente `--apply`. No se garantiza la recuperación en todos los casos ni la prevención absoluta de nuevas corrupciones.

## Funciones y alcance

Reconstruye el registro local usando proyectos existentes en SQLite, conserva identificadores históricos conocidos, preferencias actuales y conversaciones explícitamente sin proyecto. Antes del cambio, conserva los archivos de estado y una copia consistente de SQLite. Nunca escribe directamente en la base original.

Las copias históricas son independientes del `.bak` inmediato de la aplicación. Un registro vacío o inválido no reemplaza la última referencia válida. No recupera código eliminado, transcripciones ausentes, proyectos remotos/en la nube ni datos de otro ordenador.

El proyecto nació de una recuperación real con JSON corrupto y apagados incorrectos. Esto no demuestra que todos los incidentes tengan esa causa. Consulte [detalles técnicos](HOW_IT_WORKS.md).

## Requisitos

- Windows 10/11 para aplicar cambios; Python 3.10 o superior.
- PowerShell, Símbolo del sistema o Git Bash **en Windows**.
- `state_5.sqlite` con tablas compatibles `projects`, `project_roots` y `threads`.
- La recuperación en macOS, Linux y WSL no está soportada en esta versión.

La estructura interna puede cambiar entre versiones de Codex. Una estructura incompatible detiene la operación. Las pruebas sintéticas no validan todas las versiones de la aplicación.

## Descargar y revisar sin Git

1. En GitHub, seleccione **Code → Download ZIP**.
2. Extraiga el ZIP completo. No ejecute archivos dentro del archivo comprimido.
3. Si hace falta, instale Python 3.10+ desde el [sitio oficial](https://www.python.org/downloads/windows/).
4. Abra la carpeta extraída en el Explorador. Escriba `powershell` en la barra de dirección y pulse Enter.
5. Ejecute la vista previa:

```powershell
py -3 .\codex_recovery.py plan --lang es
```

Si no existe `py`, sustituya `py -3` por `python` y confirme la versión 3.10+. Doble clic en `codex-recovery.cmd` también muestra la vista previa y mantiene abierta la ventana. El idioma predeterminado es portugués.

## Aplicar

1. Revise `projects`, `recoveredAssignments` y `ambiguousAssignments`. No se asignan automáticamente conversaciones con varios proyectos candidatos en una misma carpeta.
2. Guarde el trabajo. Cierre completamente Codex/ChatGPT, incluida la bandeja, y las sesiones de Codex CLI.
3. En un **terminal externo de Windows**, desde la carpeta extraída:

```powershell
py -3 .\codex_recovery.py repair --apply --lang es
```

4. Espere la confirmación. Abra Codex y compruebe proyectos y conversaciones en la interfaz.

Ante un error, conserve la copia indicada y evite repetir cambios sin revisar. Un proceso `codex.exe` activo bloquea la recuperación: cierre las sesiones normalmente, sin finalizar trabajo no guardado. `result.json` confirma la escritura; todavía hay que validar la migración al abrir la aplicación.

### Git Bash en Windows

```bash
python ./codex_recovery.py plan --lang es
# Tras guardar el trabajo y cerrar la aplicación y Codex CLI:
python ./codex_recovery.py repair --apply --lang es
```

Use `py -3` si es necesario. Estos comandos son para **Git Bash en Windows**, no Linux/WSL. No use ejecución remota sin revisar, `curl | bash` ni desactive protecciones.

## Usar con su IA/Codex

Copie el [prompt en español](AI_PROMPTS.md#español). La IA debe revisar el código y ejecutar primero solo la vista previa. Si está dentro de Codex o un sandbox, debe entregar el comando para un terminal externo, sin eludir bloqueos.

No envíe credenciales, bases reales, transcripciones ni copias a servicios de IA para facilitar el diagnóstico. La herramienta funciona localmente.

## Copias y prevención

```powershell
py -3 .\codex_recovery.py preserve --lang es
py -3 .\codex_recovery.py backup --lang es
py -3 .\codex_recovery.py watch --lang es
```

`preserve` conserva el incidente aunque el JSON esté corrupto. `backup` guarda un registro válido. `watch` funciona hasta Ctrl+C o hasta cerrar el terminal.

Destino predeterminado: `Documents\CodexProjectRecoveryBackups` dentro del perfil Windows. Use `--backup-dir` para cambiarlo; no elija `.codex`, este repositorio público ni una carpeta compartida. `--codex-home` cambia el origen; por defecto se utiliza `CODEX_HOME` o `~/.codex`.

El observador revisa cada 30 segundos y, cada 15 minutos, intenta guardar una nueva versión si cambió el estado protegido. Los errores o una disminución de proyectos generan `ATTENTION.json`. No hay notificaciones de Windows, restauración automática ni eliminación automática de versiones antiguas. Vigile el espacio y guarde otra copia protegida en un dispositivo independiente.

**Esta edición pública no instala el inicio automático.** Para ejecutarlo al iniciar sesión, cree un acceso directo a `python.exe` con la ruta completa del script y `watch --lang es`. Colóquelo en la carpeta de **Win+R → `shell:startup`**. Mantenga el script en su ubicación y un solo observador activo. La posible ventana de pérdida llega a 15 minutos.

Para restaurar una versión concreta, cierre todos los procesos que escriban y conserve el estado actual antes de sustituir manualmente el JSON principal y `.bak` por el `global-state.json` validado del snapshot. **No sobrescriba la base completa sobre conversaciones más recientes.** No existe restauración automática de snapshots en esta versión; solicite ayuda con datos anonimizados si tiene dudas.

## Idiomas, privacidad y contribución

Los enlaces superiores cambian la documentación completa. La consola acepta `--lang pt|en|zh|es`; los identificadores JSON y algunos errores técnicos permanecen en inglés. Chino simplificado usa `zh`/`zh-CN`, no `CH`.

El código público no da acceso a su ordenador ni a repositorios privados. Cada persona lo ejecuta sobre sus propios archivos. Las copias contienen nombres, rutas, metadatos e índices privados. Se excluyen `auth.json` y transcripciones, pero las demás copias siguen siendo confidenciales.

Nunca publique `.codex`, bases, copias, registros completos o capturas privadas. `.gitignore` ayuda con Git, **pero no bloquea cargas manuales en el navegador ni borra el historial publicado**. Lea [SECURITY.md](../SECURITY.md).

Pruebas: `python -m unittest discover -s tests -v`. CI usa datos ficticios en Windows y Linux; esto no habilita recuperación en Linux. Contribuciones: [CONTRIBUTING.md](../CONTRIBUTING.md). Licencia [MIT](../LICENSE). Sin afiliación ni soporte oficial de OpenAI.
