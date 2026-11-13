# Codex CLI

Copie `../../skills/game-studio-ai/` para `.agents/skills/game-studio-ai/` no repositório confiável. Os papéis Claude em `../../agents/` não são TOML do Codex. Para configurar um agente, use um arquivo em `.codex/agents/` com formato documentado; exemplo mínimo abaixo. Skills podem ser invocadas pelo CLI com o mecanismo atual de skill. Configure MCP separadamente em `config.toml` e valide servidor, ferramenta e aprovações; este pacote não inclui nenhum MCP.

Veja https://developers.openai.com/codex/build-skills, https://developers.openai.com/codex/agent-configuration/subagents e https://developers.openai.com/codex/mcp.
