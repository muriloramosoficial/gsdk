# Adaptadores de harness e MCP

## Regra de interoperabilidade

Mantenha `SKILL.md` e os documentos/contratos de agentes como núcleo portável. O formato aberto de skills (diretório com `SKILL.md` e frontmatter `name`/`description`) ajuda na reutilização, mas **não padroniza** descoberta, invocação, permissões, agentes, hooks ou integração MCP entre produtos. Instale/configure cada destino de acordo com sua documentação e valide-o no runtime.

## Matriz resumida (documentação oficial consultada em 13 nov 2026)

| Destino | Skill | Agentes/delegação | MCP | Situação do pacote |
|---|---|---|---|---|
| Claude Code | `skills/<id>/SKILL.md` em plugin; suporta skill com frontmatter e referências | `agents/*.md` no plugin; subagents têm instruções e contexto/configuração próprios | `.mcp.json` com `mcpServers`; configurar por runtime/escopo | O diretório `.claude-plugin/plugin.json` + componentes na raiz é formato nativo. Comandos aqui são skills namespaced. |
| Codex CLI | `.agents/skills/<id>/SKILL.md`; também skills globais | agentes em TOML separados em `.codex/agents/`; subagents herdam permissões do pai | configuração em `config.toml`, `[mcp_servers.<nome>]` | O pacote-base precisa ser instalado/copiado para os caminhos Codex. `agents/openai.yaml` é extensão opcional, não requisito. |
| OpenCode | `.opencode/skills/<id>/SKILL.md`; também reconhece `.agents/skills` e `.claude/skills` | `agents/*.md` ou config; modos e permissões são do OpenCode | bloco `mcp.servers` no `opencode.json[c]` | A descoberta cruzada de arquivo não garante semântica idêntica. Configure ferramentas/agentes à parte. |
| DeepSeek Harness (`dsh`) | A documentação consultada descreve perfis/plugins, mas não confirma que carregue skills Agent Skills ou este pacote diretamente | Harness e CLI oficial existem, mas estão em developer preview; confirme a versão instalada e os contratos de plugin antes de integrar | A API do modelo e um servidor MCP são camadas distintas; não há promessa de que `dsh` use um cliente MCP para este projeto | Use o texto do núcleo como instrução de sistema/contexto apenas se o profile/plugin instalado aceitar isso; conecte ferramentas por mecanismo confirmado no harness/bridge escolhido. |
| Qualquer cliente MCP | Não é definido pelo protocolo | MCP não padroniza funcionários ou handoff multiagente | MCP define primitivas tools/resources/prompts, descoberta e transporte. O host controla modelos, invocação, permissões e UI. | Configuração é específica de cada cliente; um servidor compartilhado exige transporte, autenticação, permissões e suporte confirmados. |

## Caminhos/formatos publicados

### Claude Code

Um plugin pode conter `.claude-plugin/plugin.json`, `skills/`, `agents/`, `hooks/hooks.json` e `.mcp.json` na raiz. Skills do plugin ficam em `skills/<nome>/SKILL.md`; agentes em `agents/<nome>.md`. Skills aparecem com namespace do plugin, por exemplo `/game-studio:start` quando o plugin se chama `game-studio`. Também há instalação de skills/agentes fora de plugin. Preferir skills para novos comandos; não depender do formato legado `commands/`.

### Codex CLI

Uma skill é um diretório com `SKILL.md` e frontmatter `name`/`description`; para projeto, o caminho documentado é `.agents/skills/<id>/`. Agentes customizados são arquivos TOML em `.codex/agents/` (projeto) ou `$HOME/.codex/agents/`. Configuração de servidor MCP é em `config.toml`; MCP por projeto requer projeto confiável. Não confundir Codex app server (JSON-RPC próprio, experimental/não produção na documentação consultada) com servidor MCP.

### OpenCode

O caminho nativo é `.opencode/skills/<id>/SKILL.md`; a documentação também lista busca em `.agents/skills` e `.claude/skills`. Agentes são Markdown/config do OpenCode. Configuração MCP fica em `mcp.servers`; servidores locais executam comando/argumentos e os remotos usam URL/Streamable HTTP. Variáveis em JSON usam o mecanismo `{env:VAR}` documentado; não presuma expansão `$VAR`.

### DeepSeek

A DeepSeek API é compatível com a forma da API OpenAI em partes documentadas, mas isso não significa execução de ferramentas no servidor: tool calls precisam de um cliente/harness para despachar a função e devolver o resultado. A documentação oficial do DeepSeek Harness (`dsh`) descreve outro produto e o qualifica como developer preview. IDs de modelo, parâmetros, ferramentas e compatibilidade devem ser lidos na documentação/versionamento atual. Não declarar que este pacote tem instalação automática no `dsh` sem validar suporte a instruções/plugins/MCP da versão alvo.

## Como integrar um servidor MCP escolhido

1. Defina qual servidor real resolve uma função do jogo (por exemplo, issue tracking, filesystem com escopo, asset pipeline). Leia a documentação do fornecedor e verifique licença, manutenção, permissões, transporte, autenticação e se a ferramenta pode alterar dados.
2. Configure o servidor **no cliente**, nunca embuta tokens neste pacote. Comece com ferramentas de leitura; exponha escrita apenas com escopo necessário e aprovação para efeitos externos/irreversíveis.
3. Confira no runtime a lista de ferramentas e o schema. Não invente nomes. Faça uma chamada de leitura sem dados sensíveis e revise o resultado.
4. Confirme se o harness oferece delegação. Se oferecer, use agentes nomeados e limite de contexto. Se não, execute papéis sequenciais ou gere cartões de trabalho. MCP sozinho não cria subagentes.
5. Grave no projeto apenas identificação, finalidade, versão/documentação consultada e estado da integração. Não grave segredo, token ou URL de autorização temporária.

## Referências oficiais

- Claude Code Skills: https://code.claude.com/docs/en/skills.md
- Claude Code Subagents: https://code.claude.com/docs/en/sub-agents.md
- Claude Code MCP: https://code.claude.com/docs/en/mcp.md
- Claude Code plugin components: https://code.claude.com/docs/en/plugins/components.md
- Codex Skills: https://developers.openai.com/codex/build-skills
- Codex subagents: https://developers.openai.com/codex/agent-configuration/subagents
- Codex MCP: https://developers.openai.com/codex/mcp
- OpenCode Skills: https://opencode.ai/docs/skills/
- OpenCode agents: https://opencode.ai/docs/agents/
- OpenCode MCP: https://opencode.ai/docs/mcp-servers/
- DeepSeek API tool calls: https://api-docs.deepseek.com/guides/tool_calls/
- DeepSeek Responses API: https://api-docs.deepseek.com/guides/responses_api/
- DeepSeek Harness CLI (developer preview): https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/README.md
- MCP architecture: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture
- MCP specification: https://modelcontextprotocol.io/specification/2026-07-28

Consulte novamente antes de instalar: documentação e versões podem mudar. A presença destes links não implica que algum servidor externo esteja configurado ou testado.
