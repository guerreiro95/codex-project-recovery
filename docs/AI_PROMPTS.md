# Prompts for your AI / Prompts para sua IA

[Português](#português) · [English](#english) · [简体中文](#简体中文) · [Español](#español)

Use after downloading and extracting this repository, with your AI pointed at that folder. Never include credentials or private backups in the prompt. An agent inside Codex cannot close its own host safely; the final repair may require a manual command in an external Windows terminal.

## Português

```text
Estou no Windows e baixei o projeto comunitário codex-project-recovery.
Meus projetos desapareceram do Codex, mas ainda encontro conversas em Recentes.

Leia README.md, SECURITY.md e codex_recovery.py antes de executar.
Confirme a pasta deste projeto e Python 3.10+. Não instale dependências desnecessárias.
Não leia nem envie auth.json, tokens, cookies, transcrições ou arquivos de credenciais.
Não envie bancos, backups, caminhos privados ou saídas completas a serviços externos.
Execute inicialmente apenas a prévia: python codex_recovery.py plan --lang pt.
Explique o total de projetos, associações recuperáveis e ambiguidades sem expor nomes privados.
Não use --apply sem eu revisar o plano e autorizar especificamente a aplicação.
Se estiver no aplicativo Codex ou no sandbox, não burle as proteções:
forneça o comando para eu executar em terminal externo após salvar o trabalho e fechar o aplicativo e CLI.
Não encerre processos à força, não sobrescreva o SQLite original e não apague dados.
Depois do reparo, ajude a validar a interface e explique backup/watch e suas limitações.
```

## English

```text
I am on Windows and downloaded the community codex-project-recovery project.
My Codex projects disappeared, but conversations remain in Recents.

Read README.md, docs/README.en.md, SECURITY.md and codex_recovery.py first.
Verify this project folder and Python 3.10+. Do not install unnecessary dependencies.
Do not read or transmit auth.json, tokens, cookies, transcripts or credential files.
Do not send databases, backups, private paths or complete output to external services.
Initially run preview only: python codex_recovery.py plan --lang en.
Explain project counts, recoverable memberships and ambiguities without exposing private names.
Do not use --apply until I review the plan and specifically authorize applying it.
If inside Codex or a sandbox, do not bypass safeguards:
give me the command for an external terminal after I save work and close the app and CLI.
Do not force-kill processes, overwrite the original SQLite database or delete data.
After repair, help verify the UI and explain backup/watch and their limitations.
```

## 简体中文

```text
我使用 Windows，并已下载社区项目 codex-project-recovery。
我的 Codex 项目消失了，但“最近”列表中仍然有对话。

请先阅读 README.md、docs/README.zh-CN.md、SECURITY.md 和 codex_recovery.py。
确认项目目录及 Python 3.10+，不要安装不必要的依赖。
不要读取或传输 auth.json、令牌、Cookie、会话转录或凭据文件。
不要把数据库、备份、私人路径或完整输出发送到外部服务。
最初仅执行预览：python codex_recovery.py plan --lang zh。
说明项目数量、可恢复的归属和不明确的归属，不要暴露私人名称。
在我审查方案并明确授权应用恢复前，不要使用 --apply。
如果你在 Codex 应用或沙盒中，不要绕过保护：
请提供在外部终端执行的命令，让我先保存工作并关闭应用和 CLI。
不要强行终止进程、覆盖原始 SQLite 数据库或删除数据。
恢复后帮助检查界面，并说明 backup/watch 的用途和限制。
```

## Español

```text
Uso Windows y he descargado el proyecto comunitario codex-project-recovery.
Mis proyectos de Codex desaparecieron, pero las conversaciones siguen en Recientes.

Lea primero README.md, docs/README.es.md, SECURITY.md y codex_recovery.py.
Verifique la carpeta del proyecto y Python 3.10+. No instale dependencias innecesarias.
No lea ni transmita auth.json, tokens, cookies, transcripciones o credenciales.
No envíe bases, copias, rutas privadas ni salidas completas a servicios externos.
Ejecute inicialmente solo la vista previa: python codex_recovery.py plan --lang es.
Explique cantidades, asociaciones recuperables y ambigüedades sin revelar nombres privados.
No use --apply hasta que revise el plan y autorice específicamente la aplicación.
Si está dentro de Codex o un sandbox, no eluda las protecciones:
proporcione el comando para un terminal externo después de guardar mi trabajo y cerrar la aplicación y CLI.
No fuerce el cierre de procesos, no sobrescriba SQLite original y no elimine datos.
Después ayúdeme a validar la interfaz y explique backup/watch y sus limitaciones.
```
