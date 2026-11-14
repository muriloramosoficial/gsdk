# GAME STUDIO AI

Uma skill de produção de jogos e um plugin para Claude Code. Ajuda a transformar uma ideia em um plano de produção, distribuir tarefas entre papéis especializados, integrar entregas, acompanhar QA e manter um jogo após o lançamento.

> **O que isto é — e o que não é:** o pacote fornece instruções, perfis, modelos, comandos e scripts. Ele não é um conjunto de modelos de IA, não cria uma empresa sozinho e não conecta MCPs sem configuração. “Agentes” são papéis; só viram processos/modelos independentes quando o harness instalado oferece e configura essa capacidade.

## Recursos do pacote

- Skill central portátil em `skills/game-studio-ai/`, com fluxo de produção, segurança, aceite e retomada.
- Plugin nativo de Claude Code, com comandos namespaced como `/game-studio:start` **quando o plugin está carregado**. Se instalar somente a skill na conta do Claude, o comando é `/game-studio-ai`.
- Perfis Claude Code para direção, game design, narrativa, engenharia, arte, UI/UX, áudio, QA, performance e publicação.
- Instalador da skill para diretórios nativos de Codex CLI e OpenCode.
- Scaffold de documentação que se recusa a sobrescrever uma pasta `studio/` existente e cria checklist/manifesto de integrações sem valores secretos.
- Preflight de runtime e provedores por função, com verificação de declaração e presença de variáveis de ambiente.
- Demo documental, testes automatizados e relatório de validação.

## Começo rápido

1. Clone o repositório e abra o terminal na pasta:

   ```bash
   git clone https://github.com/muriloramosoficial/gsdk.git
   cd gsdk
   ```

2. Escolha um runtime/modelo central e autentique-o no harness. As alternativas de login e API key estão descritas em [Pré-requisitos de IA e integrações](#pre-requisitos-de-ia-e-integrações).
3. Para jogo novo, execute o scaffold mostrado no tutorial. Ele cria `studio/AI_INTEGRATIONS.md` e `studio/integrations.json`, que pedem a configuração do runtime e dos serviços usados pelo jogo. Não coloque valores de chaves nesse repositório.
4. Rode o preflight para `model-inference` e, antes de cada departamento externo, para a capacidade correspondente. Uma ausência bloqueia só a tarefa dependente.
5. Inicie pela sintaxe correspondente à instalação: `/game-studio:start` no plugin Claude Code ou `/game-studio-ai` na skill instalada diretamente no Claude. Nos outros harnesses, invoque a skill `game-studio-ai`. Revise o concept brief, as premissas, o escopo e os riscos; aprove o plano antes de iniciar produção.
6. Acompanhe com `status`, execute a próxima tarefa, revise artefatos e testes. A publicação continua manual e exige sua aprovação.

## Pré-requisitos de IA e integrações

Para tarefas com inferência, configure **um runtime central** no harness escolhido. Isso não significa que você precise assinar Claude, OpenAI e DeepSeek ao mesmo tempo. O login do harness/modelo não equivale necessariamente a uma API key, e uma chave válida não garante créditos, permissões ou direitos comerciais.

- **Claude Code:** pode usar login de uma conta Claude elegível. Para chamadas diretas à API Anthropic, configure `ANTHROPIC_API_KEY`; é outro modo de cobrança. Se essa variável estiver no ambiente, Claude Code pode usar faturamento de API em vez do uso incluído na assinatura.
- **Codex CLI:** escolha login ChatGPT ou API da OpenAI Platform (`CODEX_API_KEY`). `CODEX_ACCESS_TOKEN` é uma opção restrita a automação Enterprise aprovada.
- **OpenCode:** escolha um modelo/provider suportado pela versão instalada e siga a autenticação oficial desse provider; não existe uma chave universal do OpenCode.
- **DeepSeek Harness:** para inferência via DeepSeek API, configure `DEEPSEEK_API_KEY`; o serviço hospedado usa login de conta. A instalação local do harness não autentica nem concede acesso ao modelo.

As ferramentas especializadas entram **quando o projeto precisa daquela função**:

- Revisão independente de código: Codex CLI, conectado por login ChatGPT ou `CODEX_API_KEY`.
- Arte conceitual/UI 2D: Scenario; API usa par de chave/segredo e MCP oferece OAuth ou chave/segredo.
- Pixel art, sprites e animação 2D: PixelLab; API/MCP usam token Bearer. `PIXELLAB_API_TOKEN` no manifesto é convenção deste pacote, não nome oficial de variável.
- Geração de modelos 3D/texturas: Meshy API/MCP usa `MESHY_API_KEY`; o CLI oficial também aceita login OAuth.
- Ajuste de cena 3D: Blender MCP local, sem API key Blender. Exige isolamento, backup e revisão de Python gerado.
- Voz, música e efeitos sonoros: ElevenLabs API usa `ELEVENLABS_API_KEY`; o MCP hospedado usa OAuth.
- QA de navegador: Playwright local, sem API key do fornecedor. Credenciais do site sob teste são configuradas separadamente.
- Backend: Supabase MCP hospedado usa OAuth por padrão; `SUPABASE_ACCESS_TOKEN` é alternativa PAT para CI/manual.

Isso significa que nenhum serviço de arte, áudio, 3D, backend ou browser é uma dependência universal. Se o jogo não usar 3D, por exemplo, Meshy não deve bloquear design ou programação. Configure as tarefas usadas no arquivo `studio/integrations.json`; para cada serviço ausente, a skill bloqueia só a ação que depende dele e continua tarefas independentes ou manuais.

No projeto recém-inicializado, o checklist em `studio/AI_INTEGRATIONS.md` pede para escolher o runtime e configurar os logins/tokens relevantes. O manifesto guarda apenas método, estado, referências e **nomes** de variáveis. Nunca cole segredos no chat ou no manifesto. Provisione-os em keyring/secret manager, CI ou ambiente protegido do processo. Se usar um arquivo `.env.local`, ignore-o no Git antes de preencher.

Teste a conexão no harness e marque-a como `verified` somente após observar uma chamada inofensiva. O script verifica somente o estado declarado e se os nomes de variáveis estão disponíveis no ambiente; não valida chaves, saldo, planos, direitos, licença nem funcionamento remoto:

```bash
python3 /caminho/para/gsdk/scripts/check_integrations.py \
  --project-dir /caminho/para/o-jogo --task model-inference

python3 /caminho/para/gsdk/scripts/check_integrations.py \
  --project-dir /caminho/para/o-jogo --task audio_generation
```

Capacidades incluídas: `code_review`, `concept_art`, `pixel_art`, `3d_generation`, `blender_scene_edit`, `audio_generation`, `browser_qa`, `supabase_backend` e `deepseek_inference`. Veja os detalhes e links oficiais em [`provider-authentication.md`](skills/game-studio-ai/references/provider-authentication.md).

## Instalar e conectar em cada harness

### Claude — skill direta ou plugin Claude Code

Há dois formatos diferentes. A sintaxe depende de qual deles você instalou; `/game-studio:start` **não** é um comando universal de qualquer instalação da skill.

**Se você adicionou/enviou a skill à sua conta Claude, sem carregar o plugin:** invoque `/game-studio-ai` e escreva o pedido após o nome, por exemplo `/game-studio-ai iniciar um jogo novo: puzzle 2D de engrenagens`. Neste modo, `start` é a intenção escrita por você, não um comando `:start` separado.

**Se você estiver usando Claude Code com o plugin deste repositório:**

1. Instale o Claude Code seguindo a documentação oficial e clone este repositório.
2. Carregue o plugin local na sessão de desenvolvimento:

   ```bash
   cd gsdk
   claude --plugin-dir "$PWD"
   ```

   O parâmetro `--plugin-dir` carrega o plugin local para essa sessão. Para compartilhar ou instalar de forma persistente em uma equipe, publique-o por um marketplace Claude Code conforme a documentação oficial; este repositório ainda não inclui um marketplace.
3. Na sessão, execute `/plugin` e confira se `game-studio` aparece como carregado.
4. Execute `/game-studio:start`. Para retomar um projeto existente, use `/game-studio:status`. O plugin também oferece os fluxos `next`, `review`, `fix`, `improve`, `update`, `optimize`, `regression`, `rollback`, `team`, `report`, `build` e `release`, sempre com o prefixo `/game-studio:`.
5. Se `:start` não aparecer, confira se iniciou Claude Code com a raiz correta (aquela que contém `.claude-plugin/plugin.json`), se o plugin está habilitado/carregado na sessão e recarregue/reinicie o plugin. Se você só adicionou a skill à conta Claude, volte ao comando `/game-studio-ai` em vez de usar `:start`.

O nome dos comandos muda conforme a localização da skill: a documentação oficial explica [skills em plugin e skills diretas](https://code.claude.com/docs/en/skills#how-a-skill-gets-its-command-name) e o [namespace do plugin](https://code.claude.com/docs/en/plugins/components#skills).

O pacote não inclui servidor MCP. O Claude Code usa sua própria configuração MCP, normalmente `.mcp.json` no escopo de projeto ou as opções de usuário/local disponíveis na versão instalada. Configure somente servidores reais, confira as ferramentas/permissões que serão expostas e não versione credenciais.

### Codex CLI — instalar a skill central

Codex recebe o processo e as referências da skill. Os agentes TOML e MCP são uma configuração separada do Codex; os agentes Claude deste repositório não são carregados automaticamente.

1. Abra o repositório do jogo e o terminal em qualquer pasta.
2. Execute o instalador incluído, indicando a raiz do jogo já existente:

   ```bash
   python3 /caminho/para/gsdk/scripts/install_skill.py \
     --target codex \
     --project-dir /caminho/para/o-jogo
   ```

   O destino será `.agents/skills/game-studio-ai/`. Se já existir, o script para sem sobrescrever.
3. Inicie o Codex CLI na raiz do jogo. Digite `/skills` para verificar se `game-studio-ai` foi descoberta. Invoque a skill explicitamente pelo nome que a instalação exibir, por exemplo `$game-studio-ai` nas versões que usam essa forma.
4. Para subagentes, converta os perfis desejados ao formato TOML do Codex e coloque-os em `.codex/agents/`. Há um exemplo em `adapters/codex/`. Confira permissões e modelo herdados antes de usá-los.
5. Configure MCP no `config.toml` do Codex conforme a documentação oficial. MCP de projeto pode depender de o repositório ser marcado como confiável. O pacote não cria servidores MCP nem adiciona credenciais.

### OpenCode — instalar a skill central

OpenCode recebe o núcleo portável. Agentes Markdown e configuração MCP têm esquema próprio do OpenCode.

1. Abra o repositório do jogo.
2. Execute:

   ```bash
   python3 /caminho/para/gsdk/scripts/install_skill.py \
     --target opencode \
     --project-dir /caminho/para/o-jogo
   ```

   O destino será `.opencode/skills/game-studio-ai/`. O script não sobrescreve uma skill existente.
3. Inicie o OpenCode na raiz do jogo. Confirme que `game-studio-ai` foi descoberta. Peça: “Use a skill `game-studio-ai`; comece um projeto novo a partir desta ideia: …”
4. Selecione e configure agentes em formato OpenCode somente quando necessário; veja o exemplo em `adapters/opencode/`. Os perfis de `agents/` na raiz são escritos para Claude Code e não devem ser copiados sem conversão.
5. Configure servidores MCP em `mcp.servers` no arquivo OpenCode conforme a documentação da sua versão. Se a skill não aparecer, confira o caminho e reinicie/recarregue o cliente.

### DeepSeek Harness (`dsh`) — integração manual, não automática

A documentação consultada confirma a existência de `dsh`, mas o identifica como developer preview e não confirma importação direta de skills Agent Skills ou dos perfis deste plugin.

1. Confira a versão instalada e o README oficial do `dsh`.
2. Verifique se o profile/plugin dessa versão aceita instruções de sistema, arquivos de referência, subagentes e/ou cliente MCP.
3. Somente se o runtime oferecer oficialmente esse mecanismo, forneça `skills/game-studio-ai/SKILL.md` como instrução e inclua as referências necessárias.
4. Configure os tools MCP e o dispatcher no harness; a API DeepSeek com tool calling descreve chamadas, mas é o cliente/harness que executa as ferramentas.
5. Faça um teste inofensivo e registre a integração como `verified` apenas se a operação foi realmente observada.

Veja `adapters/deepseek-harness/README.md`. Este pacote não promete uma instalação direta do plugin no `dsh`.

## Tutorial: criar um jogo do zero

### 1. Prepare a pasta do jogo

Crie um repositório/pasta para o código. Escolha uma engine só depois de comparar plataforma, tipo 2D/3D, experiência da equipe, exportação e licença. Inicie o harness dentro da pasta do jogo.

Opcionalmente, crie os registros iniciais:

```bash
python3 /caminho/para/gsdk/scripts/init_project.py \
  --project-dir /caminho/para/o-jogo \
  --name "Meu jogo" \
  --engine "A confirmar" \
  --platform "A confirmar"
```

O script só cria documentação em `studio/`. Recusa se `studio/` já existir; nesse caso, leia e preserve os documentos atuais.

Para jogo novo, o scaffold também cria `studio/AI_INTEGRATIONS.md` (checklist de configuração) e `studio/integrations.json` (manifesto sem valores secretos). Para projeto existente cuja pasta `studio/` já existe, acrescente apenas os arquivos de integrações:

```bash
python3 /caminho/para/gsdk/scripts/init_integrations.py \
  --project-dir /caminho/para/o-jogo
```

Escolha um runtime central, configure os logins/segredos diretamente no harness ou em um secret manager, teste a conexão e só então marque `verified`. O script não pede nem grava valores de chaves. Se o jogo não usar uma integração, edite `task_requirements` no manifesto para trocar o provider por alternativa/manual ou retirar essa exigência.

### 2. Dê a ideia uma vez

No Claude Code com o plugin carregado, use `/game-studio:start`. Se instalou a skill diretamente na conta Claude, use `/game-studio-ai` e escreva o pedido; nos demais harnesses, invoque `game-studio-ai`. Exemplo de pedido:

> Quero um puzzle 2D curto em que o jogador redireciona engrenagens para fazer um jardim mecânico florescer. Quero validar primeiro uma fase pequena para PC.

O diretor deve identificar gênero, loop, pilares, escopo, plataforma presumida, riscos e premissas. Ele só deve fazer perguntas se faltar uma informação que realmente bloqueie o plano.

### 3. Revise e aprove o planejamento

Antes de produção, confira o concept brief, GDD, proposta técnica, Art Bible, plano de áudio, QA, tarefas, dependências e ferramentas recomendadas. Corrija premissas incorretas. Aprove explicitamente o plano para iniciar alterações de maior porte.

Uma recomendação de ferramenta não significa que ela esteja instalada. Exija fonte e data para preço, licença comercial, API/MCP, formatos e limitações; teste qualquer integração antes de tratá-la como funcional.

### 4. Construa uma fatia vertical

Comece com a menor versão jogável que demonstre o loop principal. Cada tarefa deve ter responsável, entradas, saídas, arquivos permitidos, dependências, critérios de aceite e testes. Delegue trabalho independente aos especialistas realmente configurados. Se o harness não oferecer subagentes, use papéis sequencialmente ou encaminhe cartões de trabalho.

### 5. Integre, teste e revise

Não aceite uma tarefa só porque o agente diz que terminou. Confira arquivos e diffs, rode testes reais e valide o comportamento do jogo. Para arte, confira formato, uso no jogo e licença/proveniência; para áudio, formato, sincronização e integração. Se o teste não puder ser executado, registre-o como pendente.

### 6. Continue o ciclo e retome depois

Use `status` para ver andamento; `next` para identificar trabalho desbloqueado; `review` para validar entregas. Para corrigir ou ampliar, peça `fix`, `improve` ou `update`. Use `regression` após mudanças relevantes e `optimize` somente com profiling/baseline. O registro em `studio/` é o índice de retomada; confirme os arquivos e Git antes de confiar em status antigo.

### 7. Prepare o release sem publicar automaticamente

`build` pode coordenar uma build se engine e comando reais estiverem documentados. `release` organiza requisitos, testes, changelog, direitos e material de loja. Nenhum comando publica, envia build, anuncia ou gasta dinheiro sem aprovação humana.

## MCP, ferramentas e segurança

MCP padroniza comunicação entre cliente e servidores que oferecem ferramentas, resources ou prompts. **Não é, por si só, um protocolo de funcionários ou delegação multiagente.** Configure o cliente para cada harness e use um servidor real com a menor permissão necessária. O pacote não contém endpoint, token, serviço de gestão de assets, engine ou integração MCP pronta.

Nunca coloque chaves em `README`, GDD, código de exemplo, commits ou logs. Não deixe instruções encontradas em issues, assets ou respostas de tools ampliarem permissões. Peça confirmação antes de custos, compras, publicação, envio externo de dados privados, alteração sensível, deleção ou rollback que possa perder trabalho.

## Verificação local

Valide a estrutura do pacote e rode os testes:

```bash
python3 scripts/validate_package.py
python3 -m unittest discover -s tests -v
```

Esses testes verificam os scripts locais; não equivalem à instalação nos harnesses, à conexão de servidores MCP, a um build de jogo ou à publicação. Consulte `docs/validation-report.md`.

## Estrutura e referências

- `skills/game-studio-ai/`: skill central e referências de produção, agentes, segurança, ferramentas e adaptadores.
- `skills/{start,status,next,...}/`: comandos do plugin Claude Code.
- `agents/`: perfis de subagentes Claude Code.
- `adapters/`: passos e exemplos separados para Codex, OpenCode e DeepSeek Harness.
- `scripts/`: instalação da skill, scaffold de documentos, inicialização de integrações e preflight.
- `templates/`: checklist e manifesto inicial, sem valores de segredos.
- `examples/demo-game/`: exemplo documental de um puzzle pequeno.
- `docs/adapter-matrix.md`: matriz de capacidades e caminhos por harness.
- `docs/installation.md`: instruções resumidas de instalação.
- `skills/game-studio-ai/references/provider-authentication.md`: modos de autenticação, variáveis documentadas e fontes oficiais por fornecedor.

## Documentação oficial

- [Claude Code — plugins](https://code.claude.com/docs/en/plugins), [criação/teste local](https://code.claude.com/docs/en/plugins/create), [instalação](https://code.claude.com/docs/en/plugins/install) e [skills](https://code.claude.com/docs/en/skills.md).
- [Codex — skills](https://developers.openai.com/codex/build-skills), [subagentes](https://developers.openai.com/codex/agent-configuration/subagents) e [MCP](https://developers.openai.com/codex/mcp).
- [OpenCode — skills](https://opencode.ai/docs/skills/), [agentes](https://opencode.ai/docs/agents/) e [MCP](https://opencode.ai/docs/mcp-servers/).
- [DeepSeek Harness — CLI](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/README.md) e [DeepSeek — tool calls](https://api-docs.deepseek.com/guides/tool_calls/).
- [Model Context Protocol — arquitetura](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture) e [especificação](https://modelcontextprotocol.io/specification/2026-07-28).
- Para autenticação e requisitos dos provedores (Anthropic, Codex, Scenario, PixelLab, Meshy, ElevenLabs, Blender MCP, Playwright, Supabase e DeepSeek), use a referência com [fontes oficiais por integração](skills/game-studio-ai/references/provider-authentication.md).

## Estado e licença

A validação estrutural, compilação dos scripts e 16 testes automatizados passaram no sandbox. O plugin/skill não foi executado em Claude Code, Codex CLI, OpenCode ou DeepSeek Harness neste ambiente; nenhuma conexão MCP, engine, build ou publicação foi testada. O `LICENSE` permanece pendente de escolha pelo titular; selecione uma licença antes de declarar o projeto open source.
