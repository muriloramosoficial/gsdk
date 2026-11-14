# Provedores de IA e conexões

**Consulta das fontes oficiais: 13 nov. 2026.** Revalide planos, métodos de login, preços, créditos, permissões, políticas de dados e licenças no momento da configuração. Ter uma chave não comprova saldo, entitlement, licença comercial ou integração funcional.

## Princípio de configuração

Escolha **um runtime/modelo central** para as tarefas que precisam de inferência. Não é necessário configurar Claude, Codex e DeepSeek ao mesmo tempo. O harness (Claude Code, Codex CLI, OpenCode ou DeepSeek Harness) e o fornecedor do modelo são camadas distintas. MCP é uma conexão de ferramentas opcional; não é requisito geral para iniciar um harness nem sinônimo de subagente.

Depois, habilite provedores por departamento do jogo. Uma integração ausente bloqueia apenas o trabalho que depende dela. Planejamento, documentação local, implementação e outras tarefas independentes podem continuar se não exigirem aquela ferramenta. No registro `studio/integrations.json`, edite `task_requirements` para declarar provedores selecionados, `runtime` para um único caminho de inferência e o estado de cada conexão.

Use `not_configured`, `configured` e `verified` com cuidado. Marque `verified` apenas após uma operação de teste observada no harness. O script de preflight verifica declaração e presença de variáveis de ambiente, mas não autentica remotamente nem valida créditos/licença.

## Runtime central: escolha um

- **Claude Code / Anthropic:** Claude Code pode usar login por navegador com um plano Claude elegível, sem API key, ou autenticação Console. Chamadas diretas à Claude API usam credencial de API — `ANTHROPIC_API_KEY` é o nome documentado para esse modo — e faturamento de API. Não confunda login de assinatura com uma chave para a API. Se `ANTHROPIC_API_KEY` estiver definida, Claude Code pode preferir esse modo e gerar cobrança de API em vez do uso incluído na assinatura; confira a autenticação efetiva.
- **Codex CLI / OpenAI:** login ChatGPT por navegador ou chave da OpenAI Platform são opções distintas. A variável documentada para o modo de chave do Codex CLI é `CODEX_API_KEY`; `CODEX_ACCESS_TOKEN` é uma opção específica de automação Enterprise autorizada. O modo API tem cobrança própria. Codex pode trabalhar localmente nos arquivos, mas a inferência do modelo continua sendo um serviço remoto.
- **OpenCode:** OpenCode é um harness, não um provedor único. Escolha e autentique um provedor/modelo que sua versão do OpenCode suporta e siga os nomes de segredo documentados por esse provedor. Não invente uma variável universal `OPENCODE_API_KEY`.
- **DeepSeek Harness (`dsh`):** instalar/iniciar o harness não requer por si só uma chave de modelo. Para inferência DeepSeek API, use `DEEPSEEK_API_KEY`; o serviço hospedado DeepSeek Harness usa login de conta, que não é o mesmo que API key. A documentação consultada descreve o harness como preview/experimental, sem auditoria de segurança, e não confirma um MCP hospedado oficial da DeepSeek API. Use isolamento e revisão humana.

O runtime central deve estar autenticado e ter passado por teste antes de tarefas com inferência. Tarefas explicitamente locais e sem chamadas a modelo podem prosseguir sem ele.

## Integrações por função

| Função | Integração recomendada | Conexão/autenticação | Quando bloquear |
|---|---|---|---|
| Arte conceitual/UI visual 2D | Scenario | Interface web não exige configurar API/MCP. API usa par de chave/segredo; SDK Python documenta `SCENARIO_SDK_API_KEY` e `SCENARIO_SDK_API_SECRET`; exemplos TypeScript também usam `SCENARIO_API_KEY` e `SCENARIO_API_SECRET`. MCP remoto oficial aceita OAuth ou chave/segredo. | Só bloquear geração/edição programática Scenario quando essa função for selecionada. Confirmar plano elegível, créditos, equipe/projeto e permissões. |
| Pixel art, sprites e animação 2D | PixelLab | API/MCP remotos usam Bearer token. A documentação consultada não nomeia uma variável de ambiente do fornecedor. Se o projeto adotar `PIXELLAB_API_TOKEN`, marque-o como convenção local, não como nome oficial; o SDK sugere `PIXELLAB_SECRET` em `from_env()`, mas esse nome não está explicitamente documentado. | Bloquear apenas chamadas de geração/edição PixelLab quando selecionadas; verificar conta, assinatura exigida pelo MCP, créditos e direitos de uso. |
| Geração de modelos 3D/texturas | Meshy | REST API e MCP usam `MESHY_API_KEY`. O CLI oficial também oferece login OAuth, então chave não é universalmente obrigatória. A geração é remota; auxiliares locais como encaminhar a um slicer não são geração offline. | Bloquear geração cloud até autenticação, acesso/credits, limites e permissões verificados. Baixar/preservar outputs conforme retenção do fornecedor. |
| Acabamento/inspeção de cena 3D | Blender MCP oficial | Add-on/servidor MCP local; não foi documentada API key, assinatura ou login Blender. Requer configuração local, versões compatíveis e permissão de internet do Blender. | Só bloquear operações LLM sobre a cena Blender. O servidor pode executar Python gerado sem salvaguardas; usar backup, revisão humana, ambiente isolado e sockets em loopback. |
| Voz, música e efeitos sonoros | ElevenLabs | API/SDK/CLI usam `ELEVENLABS_API_KEY`; MCP hospedado oficial usa OAuth. Geração usa serviço remoto. Direitos e planos variam por produto; música tem limitações próprias. | Bloquear só geração/uso ElevenLabs selecionados. Antes de uso comercial, confirmar plano, créditos, direitos do produto e mídia de distribuição. |
| QA de navegador | Playwright | Test runner/CLI/MCP oficial rodam localmente e não exigem API key nem conta Playwright. É necessário instalar dependências/navegadores e alcançar o site sob teste. Login do site e conexão a browser remoto são credenciais separadas. | Bloquear apenas teste que dependa de browser/website indisponível. Não inventar `PLAYWRIGHT_API_KEY`; proteger credenciais e estado de login do site. |
| Backend/gestão Supabase | Supabase MCP | MCP hospedado oficial usa OAuth no navegador por padrão, sem PAT. `SUPABASE_ACCESS_TOKEN` é alternativa PAT documentada para CI/manual; `SUPABASE_PROJECT_REF` pode limitar o projeto. | Habilitar somente para tarefas que precisam de tools Supabase; restringir por projeto, ferramentas e modo read-only quando possível, com aprovação manual para escrita/destruição. |
| Revisão independente de código | Codex CLI | Ver modo de runtime acima. Uma segunda revisão Codex é opcional quando outro runtime central foi escolhido. | Bloquear apenas a revisão delegada a Codex se ela for requisito aceito para a tarefa; oferecer revisão do runtime atual/manual em vez de fingir execução Codex. |

## Segredos: nomes conhecidos e limites

Os nomes abaixo são variáveis documentadas nos respectivos contextos, não uma lista de chaves que todo usuário deve criar:

- Anthropic API: `ANTHROPIC_API_KEY`. Claude Code também documenta variáveis distintas para outros modos, como `ANTHROPIC_AUTH_TOKEN` e `CLAUDE_CODE_OAUTH_TOKEN`; não são intercambiáveis com API key.
- Codex API: `CODEX_API_KEY`; automação Enterprise pode usar `CODEX_ACCESS_TOKEN` com autorização administrativa.
- DeepSeek API: `DEEPSEEK_API_KEY`.
- Scenario SDK Python: `SCENARIO_SDK_API_KEY` e `SCENARIO_SDK_API_SECRET`. Nos exemplos TypeScript: `SCENARIO_API_KEY` e `SCENARIO_API_SECRET`.
- PixelLab: token Bearer; a variável `PIXELLAB_API_TOKEN` pode ser adotada pelo projeto como convenção própria, pois o fornecedor não documenta esse nome.
- Meshy: `MESHY_API_KEY`.
- ElevenLabs: `ELEVENLABS_API_KEY`.
- Supabase: `SUPABASE_ACCESS_TOKEN` somente para modo PAT/CI/manual; OAuth do MCP hospedado não precisa dele.
- Blender MCP e Playwright local: nenhuma API key de fornecedor foi documentada.

Nunca cole chaves, tokens, cookies, `auth.json` ou estado de navegador em chat, prompts, commits, logs ou manifests. Não escreva valores de segredos em `studio/integrations.json`. Provisione-os diretamente em keyring/secret manager, nos segredos do CI ou no ambiente protegido do processo. Se usar arquivo local de ambiente, garanta que está ignorado pelo Git antes de inserir valores. O pacote não recebe, armazena nem transmite segredos.

## Fontes oficiais consultadas

- [Claude Code — autenticação](https://code.claude.com/docs/en/authentication), [variáveis de ambiente](https://code.claude.com/docs/en/env-vars), [MCP](https://code.claude.com/docs/en/mcp) e [Claude API — autenticação](https://platform.claude.com/docs/en/manage-claude/authentication).
- [Codex — autenticação](https://developers.openai.com/codex/auth), [variáveis de ambiente](https://developers.openai.com/codex/config-file/environment-variables) e [MCP](https://developers.openai.com/codex/mcp).
- [DeepSeek API](https://api-docs.deepseek.com/), [integração Claude Code](https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code) e [DeepSeek Harness — segurança](https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md).
- [Scenario — autenticação da API](https://docs.scenario.com/get-started/documentation/key-concepts-terminology/api-key-and-authentication/), [SDK Python](https://docs.scenario.com/api/python/) e [MCP](https://mcp.scenario.com/docs).
- [PixelLab — API v2](https://api.pixellab.ai/v2/docs), [MCP](https://www.pixellab.ai/mcp) e [formas de usar PixelLab](https://www.pixellab.ai/docs/ways-to-use-pixellab).
- [Meshy — autenticação](https://docs.meshy.ai/en/api/authentication), [CLI](https://www.meshy.ai/cli) e [preços da API](https://docs.meshy.ai/en/api/pricing).
- [ElevenLabs — autenticação](https://elevenlabs.io/docs/api-reference/authentication), [MCP](https://elevenlabs.io/docs/eleven-api/resources/mcp-server), [preços](https://elevenlabs.io/pricing/api) e [termos de música](https://elevenlabs.io/music-terms).
- [Blender MCP Lab — página](https://www.blender.org/lab/mcp-server/), [setup](https://projects.blender.org/lab/blender_mcp/wiki/Setup) e [repositório oficial](https://projects.blender.org/lab/blender_mcp/src/branch/main/readme.md).
- [Playwright — instalação](https://playwright.dev/docs/intro), [MCP](https://playwright.dev/mcp/installation) e [autenticação do browser testado](https://playwright.dev/docs/auth).
- [Supabase — MCP](https://supabase.com/docs/guides/ai-tools/mcp), [access tokens](https://supabase.com/docs/guides/platform/access-tokens) e [self-hosting](https://supabase.com/docs/guides/self-hosting/enable-mcp).
