# Matriz de adaptadores por harness

Verificada em 13 nov 2026 a partir das páginas oficiais listadas ao final. Reconsulte as fontes ao instalar: caminhos e recursos mudam. **A existência de suporte a skill não garante que comandos, subagentes, permissões ou MCP config sejam portáveis.**

| Ambiente | Formato de skill/local | Agentes | MCP | O que adaptar |
|---|---|---|---|---|
| Claude Code | plugin `.claude-plugin/plugin.json`; skills `skills/<id>/SKILL.md` | `agents/*.md` no plugin | `.mcp.json` | Instalar plugin como unidade; `/game-studio:start` advém do namespace e da skill `start`. |
| Codex CLI | `.agents/skills/<id>/SKILL.md`; globais em `$HOME/.agents/skills` | `.codex/agents/*.toml` | `$HOME/.codex/config.toml` ou config de projeto confiável | Copiar skill, criar arquivos TOML dos papéis e configurar MCP em `config.toml`; o slash command de Claude não é assumido. |
| OpenCode | `.opencode/skills/<id>/SKILL.md`; também reconhece `.agents/skills` e `.claude/skills` | `.opencode/agents/*.md` ou config | bloco `mcp.servers` em `opencode.json[c]` | Copiar skill para local preferido; converter agentes e permissões; confirmar IDs de modelos no catálogo instalado. |
| DeepSeek Harness | `dsh` tem perfis e plugins; carregamento direto do padrão Agent Skills não confirmado | Usar apenas perfil/plugin confirmado na versão instalada; docs consultadas o marcam developer preview | Não presumir suporte MCP nativo sem verificar a versão e plugins | Injetar a skill só pelo mecanismo oficial realmente disponível; API DeepSeek não equivale a harness nem despacha chamadas de tools sozinha. |

## Claude Code

O plugin entregue tem `name: game-studio`, com `skills/<id>/SKILL.md`, agentes Markdown em `agents/` e `.claude-plugin/plugin.json`. A invocação esperada é namespaced, como `/game-studio:start`. Skills são a via recomendada para novos comandos; não depende da pasta legada `commands/`. MCP é configuração separada em `.mcp.json`, e o pacote não escolhe um servidor por você.

## Codex CLI

Copie `skills/game-studio-ai/` para `.agents/skills/game-studio-ai/` na raiz do repositório confiável (ou para `$HOME/.agents/skills/` se for global). Para agentes, siga o formato TOML de `name`, `description` e `developer_instructions`, salvando em `.codex/agents/`. Configure servers em `config.toml` sob `[mcp_servers.<nome>]`. Agentes Codex herdam permissões do pai; não use skill como substituto de permissões. A configuração MCP por projeto depende de confiança do projeto.

## OpenCode

Copie `skills/game-studio-ai/` para `.opencode/skills/game-studio-ai/` (ou use um dos outros locais reconhecidos na documentação). Crie agentes em `.opencode/agents/` ou config própria. Configure MCP em `mcp.servers` e use substituição `{env:NOME}` para variáveis em JSON conforme documentado. A skill é carregada sob demanda; assets e referências auxiliares precisam ser abertos pelo agente.

## DeepSeek Harness

A API DeepSeek suporta function/tool calling em formatos documentados, mas a chamada à função é executada pelo cliente/harness. O produto DeepSeek Harness (`dsh`) é uma camada separada e a referência oficial consultada o chama developer preview. Não declaramos instalação desta skill no `dsh`, invocação de subagentes ou client MCP sem contrato oficial da versão configurada. Confirme no README/release do runtime de fato usado.

## MCP como integração

MCP entrega tools, resources e prompts ao cliente; o protocolo não define workers, cargos, handoff ou gerente multiagente. O host controla qual modelo chama tool e como executa subagentes. Escolha servidor específico, restrinja escopo, confirme schemas/permissões e faça uma chamada segura de teste. Não coloque tokens no repositório.

## Fontes oficiais

- [Claude Code skills](https://code.claude.com/docs/en/skills.md), [subagents](https://code.claude.com/docs/en/sub-agents.md), [MCP](https://code.claude.com/docs/en/mcp.md), [plugin components](https://code.claude.com/docs/en/plugins/components.md)
- [Codex skills](https://developers.openai.com/codex/build-skills), [subagents](https://developers.openai.com/codex/agent-configuration/subagents), [MCP](https://developers.openai.com/codex/mcp)
- [OpenCode skills](https://opencode.ai/docs/skills/), [agents](https://opencode.ai/docs/agents/), [MCP servers](https://opencode.ai/docs/mcp-servers/)
- [DeepSeek tool calls](https://api-docs.deepseek.com/guides/tool_calls/), [DeepSeek Harness CLI](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/README.md)
- [MCP architecture](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture), [specification](https://modelcontextprotocol.io/specification/2026-07-28)
