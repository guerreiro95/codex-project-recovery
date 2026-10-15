# Codex Project Recovery

**Português (padrão)** · [English](docs/README.en.md) · [简体中文](docs/README.zh-CN.md) · [Español](docs/README.es.md)

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

O README principal é português. Os links do topo abrem traduções completas. Na ferramenta, use `--lang pt`, `--lang en`, `--lang zh` ou `--lang es`. Identificadores JSON e algumas mensagens técnicas de baixo nível permanecem em inglês para facilitar suporte. `CH` não é usado como código de idioma; chinês usa `zh` e a documentação usa `zh-CN`.

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
