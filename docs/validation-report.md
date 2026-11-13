# Relatório de validação

## Escopo

Validação estrutural e testes automatizados de scaffold/instalador em diretórios temporários. A demo editorial em `examples/demo-game/` não é jogo executável. Ambiente de construção: sandbox Linux, 13 nov 2026. Não declara testes em software externo não instalado.

## Resultados

- [x] Estrutura do plugin e JSON do manifesto conferidos pelo validador local.
- [x] Skills de comando com frontmatter conferidas; sem marcadores TODO e abaixo do limite definido pelo validador.
- [x] Caminhos Markdown relativos verificados.
- [x] Testes automatizados de `init_project.py` confirmaram scaffold em projeto vazio, recusa de `studio/` existente sem modificar arquivo e recusa de diretório inexistente.
- [x] Testes automatizados do `install_skill.py` confirmaram cópia para destinos nativos Codex/OpenCode e recusa de sobrescrita.
- [x] Scripts Python compilados sem erro sintático.
- [x] Demo documental presente; engine/build não são parte dela.
- [ ] Instalação em Claude Code: não executada neste sandbox.
- [ ] Skills/agentes/MCP em Codex CLI e OpenCode: não executados.
- [ ] Integração específica de DeepSeek Harness: não executada; carregamento direto deste formato não confirmado.
- [ ] Servidor MCP, engine, build de jogo ou publicação: não configurados nem executados.

## Limitações

Comandos e agentes devem ser validados no runtime/versão destino. Credenciais, servidores e ferramentas são configurados separadamente. Compatibilidade de `SKILL.md` não transfere automaticamente slash commands, agentes, hooks, permissões ou configuração MCP.
