---
name: start
description: "Iniciar jogo: analisar ideia, propor conceito, plano, riscos e equipe sob demanda."
disable-model-invocation: true
---

# /game-studio:start

Leia `${CLAUDE_PLUGIN_ROOT}/skills/game-studio-ai/SKILL.md` e `references/production-system.md` da skill. Atue como diretor. Se nenhuma ideia foi fornecida, pergunte apenas: “Descreva a ideia do jogo que você deseja desenvolver.” Com a resposta, analise conceito, gênero, público/plataforma presumidos, loop, pilares, escopo, risco e engine alternativa. Monte GDD enxuto, plano técnico, Art Bible, áudio, QA, cronograma em faixas, backlog com dependências e papéis mínimos. Informe quais integrações estão apenas sugeridas vs verificadas. Apresente premissas e peça aprovação do plano antes de criar documentação ou iniciar produção. Não solicite dados repetidos que já estão no contexto.

Argumentos/contexto: $ARGUMENTS
