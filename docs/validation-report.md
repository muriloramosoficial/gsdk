# Relatório de validação

## Escopo

Validação estrutural e 16 testes automatizados de scaffold, preflight, inicialização aditiva e instalação em diretórios temporários. A demo editorial em `examples/demo-game/` não é jogo executável. Ambiente de construção: sandbox Linux, 14 nov 2026. Não declara testes em software externo não instalado.

## Resultados

- [x] Estrutura do plugin, manifesto Claude e template JSON de integrações conferidos pelo validador local.
- [x] Skills de comando com frontmatter conferidas; sem marcadores TODO e abaixo do limite definido pelo validador.
- [x] Caminhos Markdown relativos verificados.
- [x] `init_project.py` gera `studio/AI_INTEGRATIONS.md` e `studio/integrations.json`; mantém a recusa segura de pasta `studio/` existente.
- [x] `init_integrations.py` acrescenta somente arquivos ausentes a projetos existentes e preserva arquivos existentes sem sobrescrevê-los.
- [x] `check_integrations.py` bloqueia runtime/provider não verificado, aceita runtime OAuth sem API key, detecta variável de ambiente ausente e não expõe conteúdo inválido de campos.
- [x] O preflight de providers condicionais não bloqueia inferência não relacionada; tarefas explicitamente locais passam sem runtime.
- [x] `install_skill.py` copia a pasta autocontida da skill, incluindo scripts/templates, para destinos nativos Codex/OpenCode e recusa sobrescrita.
- [x] Scripts Python compilados sem erro sintático.
- [x] As duas cópias da skill passaram `quick_validate.py`.
- [x] Demo documental presente; engine/build não são parte dela.
- [ ] Plugin Claude Code e comandos `/game-studio:*`: não executados neste sandbox; CLI `claude` não está instalada. A documentação explica a distinção entre skill direta `/game-studio-ai` e plugin namespaced `/game-studio:start`.
- [ ] Skill adicionada a claude.ai/Cowork: não instalada/testada pelo autor; o README oferece a invocação direta que corresponde à skill avulsa.
- [ ] Skills/agentes/MCP em Codex CLI e OpenCode: não executados.
- [ ] Integração específica de DeepSeek Harness: não executada; carregamento direto deste formato não confirmado.
- [ ] Servidor MCP, engine, build de jogo ou publicação: não configurados nem executados.

## Limitações

Comandos e agentes devem ser validados no runtime/versão destino. Credenciais, servidores e ferramentas são configurados separadamente. Compatibilidade de `SKILL.md` não transfere automaticamente slash commands, agentes, hooks, permissões ou configuração MCP.
