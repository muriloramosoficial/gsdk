# DeepSeek Harness (`dsh`) — adaptação manual, sem promessa de importação direta

A documentação oficial consultada confirma o runtime/CLI `dsh` e seus perfis, mas marca o projeto como developer preview e não confirma que carregue diretamente Agent Skills, frontmatter Claude/Codex/OpenCode ou este formato de agentes. Antes de integrar, confira o README, versão/release e mecanismo de plugin/perfil realmente disponíveis no ambiente alvo.

Se o profile/plugin instalado aceitar instruções de sistema ou arquivos Markdown, use `../../skills/game-studio-ai/SKILL.md` e os documentos necessários como contexto; configure delegação e MCP somente pelos meios documentados nessa versão. Se o harness não aceitar arquivos de referência, cole o conteúdo do núcleo de forma explícita e registre a limitação. A API DeepSeek com function calling não executa sozinha a ferramenta: o cliente/harness precisa despachar e devolver o resultado.

Não há secrets nem configuração MCP neste adapter. Não declare integração `verified` até executar um teste real no runtime. Fonte: https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/README.md e https://api-docs.deepseek.com/guides/tool_calls/.
