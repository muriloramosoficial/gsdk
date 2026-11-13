---
name: optimize
description: "Encontrar gargalo com profiling e validar otimização contra baseline."
disable-model-invocation: true
---

# /game-studio:optimize

Identifique plataforma alvo, build, workload reproduzível e baseline. Se não houver profiling/métrica, primeiro planeje coleta segura e reporte o que falta; não reescreva por intuição. Com medição disponível, priorize gargalos, proponha mudança mínima, compare desempenho e rode testes funcionais/de regressão.

Alvo: $ARGUMENTS
