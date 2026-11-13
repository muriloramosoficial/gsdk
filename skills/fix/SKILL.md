---
name: fix
description: "Diagnosticar e corrigir bug com plano localizado e QA de regressão."
disable-model-invocation: true
---

# /game-studio:fix

Leia o registro do projeto, Git status e documentação antes da mudança. Reproduza o problema se possível; registre causa provável vs confirmada, responsável, risco, plano e critérios. Faça alteração localizada, execute teste específico e regressão pertinente, atualize bug/changelog. Preserve trabalho existente. Peça aprovação antes de qualquer operação destrutiva ou externa.

Bug/contexto: $ARGUMENTS
