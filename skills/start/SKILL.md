---
name: start
description: "Iniciar jogo: analisar ideia, propor conceito, plano, riscos e equipe sob demanda."
disable-model-invocation: true
---

# /game-studio:start — comando somente no plugin Claude Code

Leia `${CLAUDE_PLUGIN_ROOT}/skills/game-studio-ai/SKILL.md`, `references/production-system.md` e `references/provider-authentication.md` da skill. Atue como diretor. Localize/ confirme a pasta do jogo. Se `studio/` não existir, crie o scaffold aprovado; se já existir mas faltar `studio/integrations.json` ou `studio/AI_INTEGRATIONS.md`, use `${CLAUDE_PLUGIN_ROOT}/scripts/init_integrations.py` para adicionar apenas os arquivos ausentes, preservando o conteúdo existente. Leia os registros e peça para selecionar/autenticar um único runtime central antes de tarefas com inferência, além dos providers usados por função. Nunca peça segredos no chat, não grave valores de chaves no manifesto e não trate login, chave, créditos e licença como equivalentes. Rode o preflight incluído no pacote quando disponível; marque uma integração `verified` apenas após teste inofensivo observado. Se nenhuma ideia foi fornecida, pergunte apenas: “Descreva a ideia do jogo que você deseja desenvolver.” Com a resposta, analise conceito, gênero, público/plataforma presumidos, loop, pilares, escopo, risco e engine alternativa. Monte GDD enxuto, plano técnico, Art Bible, áudio, QA, cronograma em faixas, backlog com dependências e papéis mínimos. Informe quais integrações estão sugeridas, configuradas, verificadas ou bloqueadas. Uma integração ausente bloqueia somente a tarefa que depende dela; continue trabalho local independente. Apresente premissas e peça aprovação do plano antes de criar documentação ou iniciar produção. Não solicite dados repetidos que já estão no contexto.

Argumentos/contexto: $ARGUMENTS
