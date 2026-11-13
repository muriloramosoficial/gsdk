---
name: next
description: "Selecionar uma tarefa pronta, dependências, agente adequado e critério de conclusão."
disable-model-invocation: true
---

# /game-studio:next

Leia a skill central e o backlog. Escolha uma tarefa `ready` cujas dependências estejam satisfeitas; caso não haja, explique o bloqueio e proponha a menor ação para desbloquear. Use apenas especialistas/ferramentas realmente disponíveis. Após plano de produção aprovado, execute trabalho reversível dentro do escopo autorizado; registre evidência e testes. Não faça commit, compra, publicação, exclusão ou ação externa.

Contexto: $ARGUMENTS
