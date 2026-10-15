# Codex Project Recovery

Recover missing Codex Desktop projects on Windows. Local backups, preview-first repair and privacy safeguards.

**Languages / Idiomas / 语言**

Click a language below to expand its complete guide here. English starts expanded. Sections open independently; close English if you prefer to read only another language.

Clique em um idioma para expandir o guia completo aqui mesmo, sem abrir outro arquivo.

<details>
<summary><strong>Português</strong></summary>

Recupere a organização dos projetos no **Codex Desktop para Windows** quando os projetos desaparecem da barra lateral, mas as conversas continuam em Recentes.

Ferramenta comunitária, independente e não oficial. Python 3.10+, biblioteca padrão, sem servidor, sem API, sem telemetria e sem conexão de rede no código da ferramenta.

> **Primeiro visualize o plano.** Aplicar um reparo altera arquivos internos do Codex. Faça backup, feche o aplicativo e só então use `--apply`. Não há garantia universal de recuperação nem prevenção absoluta de novas corrupções.

## O que este projeto faz

- Reconstrói o cadastro local a partir de projetos que ainda existem no SQLite do Codex.
- Aproveita identificadores e associações históricas quando existem cópias válidas do estado global.
- Preserva preferências atuais e conversas explicitamente sem projeto.
- Cria cópia consistente do SQLite e preserva arquivos de estado antes do reparo.
- Mantém backups históricos independentes; estado vazio ou inválido não substitui a última referência válida.
- Oferece mensagens em português, inglês, chinês simplificado e espanhol: `--lang pt|en|zh|es`.

**Não recupera arquivos de código apagados, conversas cujas transcrições foram excluídas ou dados de outros computadores. Não grava diretamente no SQLite original.**

## Quando usar

Os projetos sumiram, as pastas continuam no disco e as conversas aparecem em Recentes. Isso pode ocorrer quando o estado global fica corrompido ou seu cadastro local fica vazio. O banco pode conservar os projetos, mesmo quando a interface deixa de mostrá-los.

O projeto nasceu de uma recuperação real com corrupção de JSON e desligamentos incorretos. Essa é uma evidência daquele incidente, **não um diagnóstico de todos os casos**. Para detalhes, consulte [como funciona](docs/HOW_IT_WORKS.md).

## Compatibilidade

| Item | Suporte |
| --- | --- |
| Sistema para aplicar reparos | Windows 10/11 |
| Python | 3.10 ou superior |
| Terminal | PowerShell, Prompt de Comando ou Git Bash no Windows |
| Esquema interno | `state_5.sqlite` com tabelas `projects`, `project_roots` e `threads` |
| macOS, Linux e WSL | Reparo não suportado nesta versão |
| Projetos remotos/nuvem | Fora do escopo |

O esquema interno pode mudar entre versões do Codex. Se ele não for compatível, a ferramenta interrompe a operação. Testes automatizados usam bancos fictícios; não equivalem à validação de todas as versões do aplicativo.

## Começar sem Git — download ZIP

1. Na página deste repositório, clique em **Code → Download ZIP**.
2. Extraia o ZIP inteiro. Não execute os arquivos de dentro do ZIP.
3. Instale Python 3.10+ pelo [site oficial](https://www.python.org/downloads/windows/) se ainda não tiver.
4. Abra a pasta extraída. No Explorador, clique na barra de endereço, digite `powershell` e pressione Enter.
5. Execute primeiro a prévia:

```powershell
py -3 .\codex_recovery.py plan --lang pt
```

Se `py` não existir, tente `python` no lugar de `py -3`. Confirme que o comando está usando Python 3.10+. Duplo clique em `codex-recovery.cmd` também abre a prévia e mantém a janela aberta.

### Aplicar a recuperação

1. Leia o plano. `projects` mostra o total; `ambiguousAssignments` mostra associações que exigem escolha.
2. Salve qualquer trabalho. Feche Codex/ChatGPT completamente, inclusive a bandeja. Encerre também sessões do Codex CLI antes de aplicar.
3. **Fora do Codex**, na janela do PowerShell da pasta extraída, execute:

```powershell
py -3 .\codex_recovery.py repair --apply --lang pt
```

4. Aguarde confirmação. Reabra Codex e valide os projetos e as conversas na interface.

Se houver erro, não repita reparos indiscriminadamente. Preserve o backup indicado na saída. Se ainda houver `codex.exe` ativo, a ferramenta bloqueia o reparo; feche as sessões normalmente, sem encerrar processos com trabalho pendente. O arquivo `result.json` confirma a gravação, mas a validação final é feita após reabrir o aplicativo.

### Git Bash no Windows

Na pasta extraída, os mesmos comandos funcionam com caminhos Bash:

```bash
python ./codex_recovery.py plan --lang pt
# Depois de salvar o trabalho e fechar Codex/ChatGPT e Codex CLI:
python ./codex_recovery.py repair --apply --lang pt
```

Se `python` não apontar para a versão correta, use `py -3`. **Esses exemplos são para Git Bash no Windows; não para Linux ou WSL.** Não use `curl | bash`, execução remota às cegas ou comandos que desativem proteções.

## Usar com sua IA/Codex

Copie o [prompt seguro no idioma escolhido](docs/AI_PROMPTS.md). A IA deve revisar o código e executar somente a prévia inicialmente. Ela deve fornecer o comando de aplicação para um terminal externo se estiver dentro do sandbox ou do aplicativo que precisa ser fechado.

Não forneça `auth.json`, tokens, banco de conversas ou backups à IA remota para “facilitar” o diagnóstico. O programa consegue operar localmente sem enviar esses arquivos.

## Backups e prevenção

```powershell
# Guardar o estado existente, inclusive se estiver corrompido:
py -3 .\codex_recovery.py preserve
# Backup de um cadastro válido:
py -3 .\codex_recovery.py backup
# Observar alterações enquanto esta janela permanecer aberta:
py -3 .\codex_recovery.py watch --lang pt
```

Destino padrão: pasta `Documents\CodexProjectRecoveryBackups` dentro do perfil Windows. É possível definir outro destino com `--backup-dir`. Não use uma pasta dentro de `.codex`, nem este repositório público.

O observador verifica o estado a cada 30 segundos e tenta criar uma nova versão a cada 15 minutos, se o cadastro protegido mudou. `Ctrl+C` encerra. **Não inicia no login automaticamente nesta edição pública.** Para início no login, crie um atalho para o comando `watch` usando `python.exe` e o caminho completo do script; coloque o atalho na pasta aberta por **Win+R → `shell:startup`**. Mantenha o script na mesma pasta e inicie apenas um observador.

Quedas na quantidade de projetos ou falhas geram `ATTENTION.json` na pasta de backup. O programa não mostra notificações do Windows e não restaura automaticamente. Não apaga versões antigas: revise espaço em disco e mantenha outra cópia protegida em dispositivo independente. A janela de perda pode chegar a 15 minutos, e o observador precisa estar ativo.

### Restaurar um estado conhecido

O reparo tenta reconstruir o cadastro a partir do banco atual. Para voltar especificamente a um snapshot, feche o aplicativo e guarde o estado atual antes de substituir manualmente o JSON principal e `.bak` pelo `global-state.json` validado de um snapshot. **Não substitua o SQLite inteiro por cima de conversas novas.** Se tiver dúvida, peça ajuda com informações anonimizadas. Não há restauração automática de snapshot nesta versão.

## Idiomas

A documentação inicial e a ferramenta usam inglês. O README principal inclui os quatro idiomas em seções expansíveis, sem sair da aba Code. Na ferramenta, use `--lang pt`, `--lang en`, `--lang zh` ou `--lang es`. Identificadores JSON e algumas mensagens técnicas de baixo nível permanecem em inglês para facilitar suporte. `CH` não é usado como código de idioma; chinês usa `zh` e a documentação usa `zh-CN`.

## Privacidade e segurança

O repositório distribuído contém somente código, documentação e testes sintéticos. Ele **não concede acesso** ao seu computador nem aos seus repositórios privados. Quem baixar executará a ferramenta nos próprios arquivos locais.

Backups gerados na máquina do usuário contêm dados privados: nomes de projetos, caminhos, metadados e índice de conversas. O programa não copia o arquivo de credenciais `auth.json` nem transcrições de sessões; isso não torna os demais arquivos públicos. Nunca publique backups, saídas completas, logs, capturas com dados pessoais ou a pasta `.codex`. Leia [SECURITY.md](SECURITY.md).

O `.gitignore` ajuda a evitar commits acidentais. **Ele não bloqueia upload manual pelo navegador nem remove arquivos já publicados.**

## Desenvolvimento

```powershell
py -3 -m unittest discover -s tests -v
```

A suíte cobre prévia sem alterações, integridade do backup, preservação de IDs e preferências, ambiguidades, estado corrompido, privacidade dos arquivos copiados e bloqueios de aplicação. O workflow do GitHub executa a suíte em Windows e Linux; os testes em Linux verificam lógica e proteções, não suporte ao reparo nesse sistema.

Contribuições são bem-vindas: [CONTRIBUTING.md](CONTRIBUTING.md). Licença [MIT](LICENSE). Projeto independente, sem afiliação ou suporte oficial da OpenAI.

</details>

<details>
<summary><strong>简体中文</strong></summary>

当 **Windows 版 Codex Desktop** 的侧边栏项目消失，但对话仍能在“最近”列表中找到时，此工具可尝试恢复本地项目组织。

这是独立、非官方的社区工具。需要 Python 3.10 或更高版本，仅使用标准库。工具代码不连接网络，不包含服务器、API 或遥测。

> **先预览，再恢复。** 应用恢复会修改 Codex 的内部状态文件。请先保存备份，完全关闭应用，再显式使用 `--apply`。无法保证所有情况都能恢复，也无法绝对防止再次损坏。

## 功能和范围

工具从现有 SQLite 项目记录重建本地项目列表，保留已知历史标识符、当前偏好设置以及明确未分配项目的对话。在修改前，它保存状态文件并创建一致的 SQLite 备份。**不会直接修改原始 SQLite 数据库。**

历史备份独立于应用自身的即时 `.bak`。空列表或无效状态不会替换上次有效备份的引用。工具不能恢复已删除的源代码、已丢失的会话转录、远程或云端项目，以及其他电脑的数据。

本项目源于一次真实恢复：JSON 损坏与异常关机同时出现。这并不意味着所有项目消失问题都有同样原因。参见[技术说明](docs/HOW_IT_WORKS.md)。

## 环境要求

- 仅支持在 Windows 10/11 上应用恢复，使用 Python 3.10+。
- 可使用 PowerShell、命令提示符或 **Windows 上的 Git Bash**。
- 需要兼容的 `state_5.sqlite`，包含 `projects`、`project_roots` 和 `threads` 表。
- 本版本不支持在 macOS、Linux 或 WSL 上应用恢复，也不支持远程/云项目。

Codex 的内部数据库结构可能变化。不兼容的结构会使工具停止操作。使用虚构数据通过测试，不等于已验证所有应用版本。

## 无需 Git：下载并预览

1. 在本仓库 GitHub 页面点击 **Code → Download ZIP**。
2. 完整解压 ZIP。不要直接在压缩包中运行文件。
3. 如未安装 Python，请从[官方网站](https://www.python.org/downloads/windows/)安装 Python 3.10+。
4. 在文件资源管理器中打开解压后的目录，在地址栏输入 `powershell`，按 Enter。
5. 先执行预览：

```powershell
py -3 .\codex_recovery.py plan --lang zh
```

如果没有 `py`，可将 `py -3` 替换为 `python`，但请确认版本至少为 3.10。双击 `codex-recovery.cmd` 也会显示预览并保留窗口。未指定 `--lang` 时默认使用英语。

## 应用恢复

1. 检查预览中的 `projects`、`recoveredAssignments` 和 `ambiguousAssignments`。多个项目指向同一目录时，不会自动猜测其归属。
2. 保存工作，完全关闭 Codex/ChatGPT（包括系统托盘中的程序），并关闭 Codex CLI 会话。
3. 在应用之外的 **Windows 外部终端**中，从解压目录执行：

```powershell
py -3 .\codex_recovery.py repair --apply --lang zh
```

4. 等待成功提示，然后重新打开 Codex，检查项目和对话。

如果出错，请保留输出中指定的备份，不要反复盲目应用修复。仍在运行的 `codex.exe` 会阻止恢复；请正常关闭会话，不要强行终止尚未保存的工作。`result.json` 只确认文件已写入，仍需在重新打开应用后检查迁移结果。

### Windows Git Bash

```bash
python ./codex_recovery.py plan --lang zh
# 保存工作并关闭桌面应用及 Codex CLI 后：
python ./codex_recovery.py repair --apply --lang zh
```

必要时改用 `py -3`。这些示例仅适用于 **Windows Git Bash**，不适用于 Linux/WSL。不要使用 `curl | bash`、未经检查的远程执行，或关闭安全保护的命令。

## 交给您的 AI/Codex

复制[中文提示词](docs/AI_PROMPTS.md#简体中文)。先要求 AI 审查代码，再仅执行预览。如果代理在 Codex 应用内或沙盒内，应提供外部终端使用的恢复命令，不得绕过保护。

不要为了方便诊断，把凭据、真实数据库、会话转录或备份上传给远程 AI 服务。恢复可完全在本地完成。

## 备份与预防

```powershell
py -3 .\codex_recovery.py preserve --lang zh
py -3 .\codex_recovery.py backup --lang zh
py -3 .\codex_recovery.py watch --lang zh
```

`preserve` 保存当前故障材料，即使 JSON 已损坏。`backup` 为有效项目列表创建快照。`watch` 持续运行，直到按 Ctrl+C 或关闭终端。

默认备份位置是 Windows 用户目录下的 `Documents\CodexProjectRecoveryBackups`。可通过 `--backup-dir` 更改；不要选择 `.codex`、本公开仓库或共享目录。`--codex-home` 可指定 Codex 数据目录；默认使用 `CODEX_HOME` 或 `~/.codex`。

观察程序每 30 秒检查状态，每 15 分钟在受保护的项目状态变化时尝试创建新版本。错误或项目数量下降会写入 `ATTENTION.json`。工具不会显示 Windows 通知、自动恢复或自动删除历史备份。请检查磁盘空间，并在独立设备上保存另一份受保护的副本。

**公开版本不会自动安装登录启动项。** 如需登录后运行，可创建指向 `python.exe` 的快捷方式，参数为脚本完整路径和 `watch --lang zh`，然后放入 **Win+R → `shell:startup`** 打开的文件夹。请保持脚本位置不变，并且仅运行一个观察程序。备份依赖观察程序运行；潜在数据丢失窗口最长为 15 分钟。

如果要恢复指定快照，请先关闭所有写入程序并保存当前状态，再用该快照中经过验证的 `global-state.json` 手动替换主 JSON 和 `.bak`。**不要用旧数据库整体覆盖包含新对话的数据库。** 本版本没有自动快照恢复命令；如有疑问，请使用脱敏信息寻求帮助。

## 语言、隐私与贡献

仓库主页默认显示英文，并在同一 README 中提供可展开的完整翻译。命令行支持 `--lang pt|en|zh|es`；JSON 字段名和部分底层错误保持英文。简体中文使用 `zh`/`zh-CN`，而不是 `CH`。

公开源代码不会授予他人访问您电脑或私人仓库的权限。每位用户只在自己的机器上操作自己的数据。生成的备份可能含有私密项目名、路径、元数据和对话索引。虽然不会复制 `auth.json` 或会话转录，其他备份内容仍然需要保密。

请勿公开 `.codex`、数据库、备份、未脱敏日志或私人截图。`.gitignore` 能减少误提交，**但不能阻止浏览器手动上传，也不能删除已公开的历史记录**。参见[安全说明](SECURITY.md)。

测试命令：`python -m unittest discover -s tests -v`。GitHub CI 在 Windows 和 Linux 上运行虚构数据测试；这不意味着支持 Linux 恢复。欢迎[参与贡献](CONTRIBUTING.md)。采用 [MIT 许可证](LICENSE)。本项目与 OpenAI 无隶属关系，也不提供官方支持。

</details>

<details>
<summary><strong>Español</strong></summary>

Recupere la organización de proyectos en **Codex Desktop para Windows** cuando desaparecen de la barra lateral, pero las conversaciones siguen en Recientes.

Herramienta comunitaria independiente y no oficial. Python 3.10+, solo biblioteca estándar. Sin servidor, API, telemetría ni conexión de red en el código de la herramienta.

> **Primero, vista previa.** Aplicar una recuperación modifica archivos internos de Codex. Conserve una copia, cierre la aplicación y use explícitamente `--apply`. No se garantiza la recuperación en todos los casos ni la prevención absoluta de nuevas corrupciones.

## Funciones y alcance

Reconstruye el registro local usando proyectos existentes en SQLite, conserva identificadores históricos conocidos, preferencias actuales y conversaciones explícitamente sin proyecto. Antes del cambio, conserva los archivos de estado y una copia consistente de SQLite. Nunca escribe directamente en la base original.

Las copias históricas son independientes del `.bak` inmediato de la aplicación. Un registro vacío o inválido no reemplaza la última referencia válida. No recupera código eliminado, transcripciones ausentes, proyectos remotos/en la nube ni datos de otro ordenador.

El proyecto nació de una recuperación real con JSON corrupto y apagados incorrectos. Esto no demuestra que todos los incidentes tengan esa causa. Consulte [detalles técnicos](docs/HOW_IT_WORKS.md).

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

Si no existe `py`, sustituya `py -3` por `python` y confirme la versión 3.10+. Doble clic en `codex-recovery.cmd` también muestra la vista previa y mantiene abierta la ventana. El idioma predeterminado es inglés.

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

Copie el [prompt en español](docs/AI_PROMPTS.md#español). La IA debe revisar el código y ejecutar primero solo la vista previa. Si está dentro de Codex o un sandbox, debe entregar el comando para un terminal externo, sin eludir bloqueos.

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

La página principal empieza en inglés e incluye las traducciones en secciones desplegables del mismo README. La consola acepta `--lang pt|en|zh|es`; los identificadores JSON y algunos errores técnicos permanecen en inglés. Chino simplificado usa `zh`/`zh-CN`, no `CH`.

El código público no da acceso a su ordenador ni a repositorios privados. Cada persona lo ejecuta sobre sus propios archivos. Las copias contienen nombres, rutas, metadatos e índices privados. Se excluyen `auth.json` y transcripciones, pero las demás copias siguen siendo confidenciales.

Nunca publique `.codex`, bases, copias, registros completos o capturas privadas. `.gitignore` ayuda con Git, **pero no bloquea cargas manuales en el navegador ni borra el historial publicado**. Lea [SECURITY.md](SECURITY.md).

Pruebas: `python -m unittest discover -s tests -v`. CI usa datos ficticios en Windows y Linux; esto no habilita recuperación en Linux. Contribuciones: [CONTRIBUTING.md](CONTRIBUTING.md). Licencia [MIT](LICENSE). Sin afiliación ni soporte oficial de OpenAI.

</details>

<details open>
<summary><strong>English</strong></summary>

Recover project organization in **Codex Desktop for Windows** when sidebar projects disappear but conversations remain in Recents.

Independent, unofficial community utility. Python 3.10+, standard library only. No server, API, telemetry or network connection in the utility code.

> **Preview first.** Applying a repair changes internal Codex state files. Preserve a backup, close the app, then explicitly use `--apply`. Recovery is not universally guaranteed, nor can future corruption be prevented absolutely.

## Capabilities and scope

The tool rebuilds the local registry from existing SQLite project records, preserves known historical IDs, retains current preferences and explicitly projectless conversations, and creates a consistent database backup before repairing global-state JSON. It never writes directly to the original SQLite database.

Historical backups are independent of the application's immediate `.bak`. Empty or invalid registries do not replace the last good backup reference. The tool does not recover deleted source files, missing session transcripts, remote/cloud projects or another computer's data.

This project originated in a real recovery involving JSON corruption and unclean shutdowns. That observation is not a diagnosis of every missing-project incident. See [technical details](docs/HOW_IT_WORKS.md).

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

Use the [English prompt](docs/AI_PROMPTS.md#english). Ask the AI to inspect the code and run only the preview first. When the agent is inside Codex or a sandbox, it must provide the apply command for an external terminal instead of bypassing process guards.

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

Never publish `.codex`, databases, backups, unredacted logs or personal screenshots. `.gitignore` helps with Git commits; **it does not stop manual browser uploads or remove published history**. Read [SECURITY.md](SECURITY.md).

Run tests with `python -m unittest discover -s tests -v`. GitHub CI covers Windows and Linux synthetic tests; Linux testing does not mean Linux repair is supported. Contributions: [CONTRIBUTING.md](CONTRIBUTING.md). License: [MIT](LICENSE). No OpenAI affiliation or official support.

</details>
