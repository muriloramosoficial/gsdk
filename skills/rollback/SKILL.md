---
name: rollback
description: "Avaliar rollback Git e exigir aprovação antes de descartar trabalho."
disable-model-invocation: true
---

# /game-studio:rollback

Inspecione branch, log e status/diff. Proponha exatamente quais arquivos/commits seriam afetados e o que pode ser perdido. Não execute reset, checkout destrutivo, revert, clean, restore ou exclusão até o usuário aprovar o plano exato. Se houver arquivos não rastreados ou mudanças de terceiros, preserve-os. Após autorização, reverta e valide.

Motivo: $ARGUMENTS
