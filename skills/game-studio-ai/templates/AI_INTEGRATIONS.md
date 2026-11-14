# Configuração das IAs e integrações

**Este arquivo é um checklist, não um local para colar chaves.** Configure cada login/token diretamente no harness, no keyring/secret manager, no CI ou no ambiente protegido do processo. Preencha apenas método, referência e estado em `integrations.json`; nunca salve o valor de uma credencial aqui.

## 1. Escolha um runtime central

Para tarefas com inferência, escolha e autentique **um** caminho principal no seu harness. Não é necessário conectar Claude, Codex e DeepSeek simultaneamente.

- Claude Code: login de uma conta Claude elegível ou login Console. Para integração direta à API Anthropic, use credencial própria de API. `ANTHROPIC_API_KEY` pode fazer Claude Code usar faturamento de API em vez da assinatura; confirme o modo ativo.
- Codex CLI: login ChatGPT ou API key da OpenAI Platform (`CODEX_API_KEY`); são caminhos com cobrança/entitlements distintos. `CODEX_ACCESS_TOKEN` é para automação Enterprise aprovada.
- OpenCode: escolha um modelo/provider suportado pela sua versão e configure a autenticação oficial desse provider; OpenCode não tem uma chave universal.
- DeepSeek Harness: escolha login do serviço hospedado ou provider/API. Para DeepSeek API, configure `DEEPSEEK_API_KEY`. O harness local pode abrir sem chave, mas chamadas de inferência precisam de um provider autenticado.

No manifesto, preencha `runtime.provider`, `runtime.auth_mode` e `runtime.status`. Marque `verified` somente depois de fazer um teste simples de inferência com o método escolhido. Se o runtime selecionado usa variáveis de ambiente, liste **somente os nomes** em `runtime.secret_env` e disponibilize-as ao processo antes de iniciar o harness.

## 2. Escolha as integrações por função do jogo

As opções iniciais do arquivo `integrations.json` representam a recomendação do pacote. Mantenha uma integração na lista `task_requirements` somente se esse departamento for usar a ferramenta. Troque o provider por uma alternativa ou remova a exigência quando o trabalho for manual/local. O preflight bloqueia somente a tarefa dependente.

- Revisão de código independente: Codex CLI. Para login, `secret_env` fica vazio; no modo API, `CODEX_API_KEY`.
- Concept art/UI: Scenario. A API/SDK Python usa `SCENARIO_SDK_API_KEY` e `SCENARIO_SDK_API_SECRET`; MCP também oferece OAuth. Para outros SDKs, confirme a variável apropriada na documentação.
- Pixel art/sprites: PixelLab API/MCP com token Bearer. O fornecedor não documenta um nome de variável de ambiente; o pacote usa `PIXELLAB_API_TOKEN` como convenção local. Você pode mapear o token por outro método seguro.
- Geração 3D: Meshy API/MCP com `MESHY_API_KEY`, ou login OAuth no CLI oficial.
- Ajuste de cena Blender: Blender MCP local. Não exige chave/API do Blender. Use backup, revisão de Python gerado e ambiente isolado.
- Voz/música/efeitos: ElevenLabs API/CLI com `ELEVENLABS_API_KEY`, ou OAuth no MCP hospedado. Confira entitlement e direitos do produto, especialmente para música.
- Testes de navegador: Playwright local, sem API key do fornecedor. Instale browsers e, se necessário, configure separadamente credenciais do site-alvo.
- Backend: Supabase MCP hospedado usa OAuth por padrão. `SUPABASE_ACCESS_TOKEN` é uma alternativa PAT para CI/manual; limite o acesso ao projeto, ferramentas e ações necessárias.
- Inferência DeepSeek: `DEEPSEEK_API_KEY`. MCP é opcional e conecta servidores externos; não presuma um servidor MCP hospedado oficial da DeepSeek API.

## 3. Configure segredos fora deste projeto

Nunca cole credenciais em chat, prompts, documentação, `integrations.json`, repositório ou logs. Use o keyring do sistema, gestor de segredos, segredo do CI ou variáveis de ambiente injetadas ao processo. Se decidir usar arquivo local `.env.local`, adicione-o ao `.gitignore` **antes** de inserir qualquer valor e confirme que não está staged.

Os nomes `secret_env` são nomes de variáveis que o preflight pode verificar; não são valores. `PIXELLAB_API_TOKEN` é convenção deste pacote, não nome oficial do fornecedor. Para OAuth ou ferramentas locais sem API key, deixe `secret_env` vazio.

## 4. Teste e libere cada departamento

Marque `status` de um provider como `verified` apenas depois de executar uma operação inofensiva no harness e observar o resultado. A verificação abaixo confere o manifesto, estados e existência das variáveis requeridas no ambiente; ela **não** chama a API, não valida a chave, saldo, preço, direito comercial nem instalação de MCP.

```bash
python3 /caminho/para/gsdk/scripts/check_integrations.py \
  --project-dir /caminho/para/o-jogo --task model-inference

python3 /caminho/para/gsdk/scripts/check_integrations.py \
  --project-dir /caminho/para/o-jogo --task pixel_art
```

Se você instalou somente a skill, use `scripts/check_integrations.py` dentro da pasta da skill em vez do caminho do clone. Se o harness não permitir executar esse arquivo, siga o mesmo checklist manualmente e registre o limite: não declare o script ou a conexão como testados.

Use a capacidade desejada no lugar de `pixel_art`: `code_review`, `concept_art`, `3d_generation`, `blender_scene_edit`, `audio_generation`, `browser_qa`, `supabase_backend` ou `deepseek_inference`. Para `local-docs` e `project-inspection`, o preflight não exige inferência. Se uma conexão faltar, não delegue aquela operação externa; continue apenas o trabalho independente que não dependa dela.

Para detalhes, variáveis oficiais, segurança e fontes, consulte `skills/game-studio-ai/references/provider-authentication.md` no pacote GAME STUDIO AI.
