# Sistema de produção

## Fases e gates

- **Discovery/conceito:** proposta, pilares, público/plataforma presumidos, loop, referências e riscos. Gate: usuário aprova intenção/escopo.
- **Pré-produção:** GDD suficiente para prototipar, decisão técnica, Art Bible, áudio, QA, assets/licenças, milestones e backlog. Gate: usuário aprova plano e quaisquer gastos/serviços.
- **Protótipo/vertical slice:** validar diversão e risco técnico usando o menor corte demonstrável. Gate: evidência de jogo funcional e decisão continuar/mudar/parar.
- **Produção:** implementar fatias com integrações frequentes, critérios de aceite e regressões.
- **Alpha/beta/release candidate:** congelar escopo progressivamente, testar plataforma alvo, acessibilidade/performance, conteúdo, save/migração e checklist de publicação. Gate: decisão humana de lançamento.
- **Lançado/live ops:** priorizar bugs/incidentes, compatibilidade de saves, telemetria com consentimento/privacidade, balanceamento, eventos e expansões. Nunca assumir que “lançado” encerra a manutenção.

Adote gates menores quando o projeto for simples. Para protótipo rápido, não criar documentos, departamentos ou integração que não ajudem a validar o jogo.

## Registro persistente por jogo

Manter no repositório do jogo, sem segredos:

- `studio/PROJECT.md`: resumo, fase, escopo, stack, decisões vigentes e ponteiros.
- `studio/GDD.md`: loop, pilares, sistemas, conteúdo, progressão e fora de escopo.
- `studio/TECH.md`: engine/versão, arquitetura, build/test commands confirmados e dependências.
- `studio/ART_BIBLE.md`: estilo, paleta, formatos/resolução, regras de assets e exemplos aprovados.
- `studio/AUDIO_PLAN.md`: objetivos, estados, formatos e integração.
- `studio/ROADMAP.md`: milestones e dependências.
- `studio/TASKS.md`: backlog com estado/owner/critério/teste.
- `studio/DECISIONS.md`: decisão, data, motivo, trade-offs e impacto.
- `studio/BUGS.md`: passos para reproduzir, esperado/atual, severidade, versão e evidência.
- `CHANGELOG.md`: mudanças relevantes por versão.

Se já houver documentação equivalente, use-a; não force duplicação. Mantenha status breve e atualize campos afetados.

## Máquina de estados de tarefa

`proposed -> ready -> in_progress -> review -> done` e alternativas `blocked`, `rejected`, `cancelled`. Uma tarefa só está `ready` quando entradas, permissão, dependências e critérios estão claros. `blocked` exige motivo e próximo passo. Para passar a `done`, é necessário artefato no caminho declarado e evidência de aceite/teste. Falha de ferramenta não é conclusão.

## Contrato de tarefa

```yaml
id: GS-0001
kind: feature | bug | art | audio | design | qa | docs | release
summary: frase curta
objective: resultado observável
priority: P0 | P1 | P2 | P3
status: proposed | ready | in_progress | review | done | blocked | rejected | cancelled
owner: role-id
inputs: []
outputs: []
dependencies: []
allowed_scope: []
excluded_scope: []
assumptions: []
risks: []
acceptance_criteria: []
tests_required: []
evidence: []
human_approval: none | pending | approved | rejected
```

Priorize bloqueadores que interrompem build/dados, depois riscos do loop principal, depois funcionalidades e polimento. Não invente datas/duração como certeza. Estime em faixa com premissas; atualize após observar produtividade real.

## Aceite por departamento

**Design/narrativa:** problema do jogador e comportamento descritos; regras sem contradição; teste/protótipo possível; coerência com pilares; texto revisado. **Código:** mudança localizada, estilo existente, tratamento de erro, teste ou explicação de ausência, build/test executado com comando e saída verificável; sem novas dependências injustificadas. **Arte/UI/animação/3D:** formato, resolução/escala, estilo, nome/pasta, funcionamento no jogo, performance razoável e proveniência/licença. **Áudio:** formato/codec/sample rate/canais conforme engine, duração/loop, volume, sincronização e integração local. **QA:** versão/build, passos, esperado vs atual, evidência, severidade e reteste. **Publicação:** plataforma alvo, requisitos e checklist verificados, direitos/licenças/privacidade revisados e aprovação humana antes de submissão.

Adapte o critério ao meio de entrega. Exigir um arquivo inexistente ou teste não executável não é critério útil; registrar a limitação.

## Mudanças, Git e recuperação

Antes de mudança substancial, observar branch, diff e arquivos não rastreados; não descartá-los. Criar checkpoint seguindo o fluxo que já existe. Não forçar commit, push, merge ou branch sem autorização/convencão aplicável. Antes de rollback, enumerar exatamente o que se perderia e pedir aprovação. Após mudança, atualizar changelog e documentação impactada, rodar testes focados e regressão proporcional ao risco.
