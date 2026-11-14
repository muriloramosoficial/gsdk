# Instalação e configuração

## Claude Code — testar o plugin local

Extraia o pacote para uma pasta conhecida. Abra o terminal nessa pasta e inicie uma sessão com o plugin local:

```bash
claude --plugin-dir /caminho/para/GAME-STUDIO-AI
```

A documentação oficial descreve `--plugin-dir` como forma de carregar diretamente um plugin durante desenvolvimento, sem marketplace. Na sessão, rode `/plugin` para conferir se o plugin está carregado e execute `/game-studio:start`. Essa sintaxe namespaced só funciona quando o plugin `game-studio` foi carregado. A sessão de diretório local é apropriada para testar; para instalação persistente ou distribuição para uma equipe, crie/adicione um marketplace segundo a documentação oficial. Este pacote não inclui um marketplace.

No modo plugin, `/game-studio:team` ou `/game-studio:status` são testes de leitura; `/game-studio:start` pede a ideia, cria plano e espera aprovação antes de preparar produção. Se esses nomes não aparecerem, confira que o plugin está carregado na sessão e use `/reload-plugins` ou reinicie o Claude Code.

## Skill adicionada diretamente ao Claude

Se você enviou/adicionou somente a skill `game-studio-ai` à sua conta Claude, sem instalar o plugin deste repositório, invoque `/game-studio-ai` e escreva a ação na mesma mensagem, por exemplo: `/game-studio-ai iniciar um jogo novo: puzzle 2D de engrenagens`. Nesse modo `start` é texto/intenção, não o comando namespaced `/game-studio:start`. Os comandos com `:` são fornecidos pelo plugin Claude Code.

## Codex CLI e OpenCode

Com o repositório do jogo já existente, rode do pacote:

```bash
python3 scripts/install_skill.py --target codex --project-dir /caminho/do/jogo
python3 scripts/install_skill.py --target opencode --project-dir /caminho/do/jogo
```

Escolha **um** dos comandos conforme o harness. O instalador copia somente a skill central e recusa destino existente, sem sobrescrever ou criar configuração MCP. Reinicie/atualize o harness se a nova skill não for descoberta. Agentes, modelo e permissões precisam da configuração específica do destino; exemplos e limites ficam em `adapters/codex/`, `adapters/opencode/` e `docs/adapter-matrix.md`.

## DeepSeek Harness (`dsh`)

Confira a versão e o mecanismo oficial de profiles/plugins no runtime instalado. As fontes consultadas identificam `dsh` como developer preview, mas não confirmam importação direta deste formato de skill. Não rode instalador que suponha um diretório não documentado. Injete a skill somente se o profile/plugin suportar explicitamente instruções ou arquivos de referência; do contrário, use o texto da skill manualmente e registre que delegação/MCP não está integrada.

## Runtime central e checklist de integrações

Antes de tarefas com inferência, autentique **um** runtime/modelo no harness escolhido. Claude Code pode usar login elegível ou modo API; Codex CLI aceita login ChatGPT ou API key; OpenCode usa um provider configurado; DeepSeek API usa `DEEPSEEK_API_KEY`, enquanto o serviço hospedado DeepSeek Harness usa login de conta. Não configure todos como requisito universal.

Para jogo novo, `scripts/init_project.py` cria a documentação e os arquivos `studio/AI_INTEGRATIONS.md` e `studio/integrations.json`. Para jogo existente com `studio/` já criado, execute o inicializador aditivo; ele não substitui arquivos existentes:

```bash
python3 scripts/init_integrations.py --project-dir /caminho/do/jogo
```

Leia o checklist, escolha as integrações usadas pelo projeto e configure logins/tokens fora do repositório. Scenario/PixelLab são opções 2D; Meshy e Blender MCP são para fluxos 3D; ElevenLabs é para áudio; Playwright é local e não precisa de API key; Supabase MCP usa OAuth no fluxo hospedado padrão. Essas ferramentas condicionais não são todas necessárias para cada jogo.

Depois de testar autenticação/conexão no harness, marque o provider como `verified` no JSON e rode o verificador. Ele não imprime nem lê valores de segredos, não faz a chamada remota e não valida saldo, licença ou direito comercial:

```bash
python3 scripts/check_integrations.py --project-dir /caminho/do/jogo --task model-inference
python3 scripts/check_integrations.py --project-dir /caminho/do/jogo --task concept_art
```

Capacidades: `code_review`, `concept_art`, `pixel_art`, `3d_generation`, `blender_scene_edit`, `audio_generation`, `browser_qa`, `supabase_backend` e `deepseek_inference`. Se uma integração faltar, bloqueie somente a tarefa dependente. Os detalhes de login, variáveis e fontes estão em `skills/game-studio-ai/references/provider-authentication.md`.

## MCP

MCP não é requisito para começar. Primeiro escolha o servidor e a ferramenta que atendem uma necessidade do jogo. Configure o servidor no cliente/harness apropriado, com menor escopo possível e credenciais fora do repositório. Confirme lista de tools e schemas, depois teste leitura inofensiva. Libere escrita apenas para as funções necessárias. Este pacote não oferece um endpoint, serviço de gestão de assets, issue tracker, engine, modelo nem chave de API.

## Fontes oficiais

- [Claude Code — plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code — criar/testar plugin local](https://code.claude.com/docs/en/plugins/create)
- [Claude Code — como o nome de skill vira slash command](https://code.claude.com/docs/en/skills#how-a-skill-gets-its-command-name)
- [Claude Code — componentes e skills namespaced de plugins](https://code.claude.com/docs/en/plugins/components#skills)
- [Claude Code — instalar/gerir plugins](https://code.claude.com/docs/en/plugins/install)
- [Codex — skills](https://developers.openai.com/codex/build-skills)
- [OpenCode — skills](https://opencode.ai/docs/skills/)
- [DeepSeek Harness — CLI](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/README.md)
