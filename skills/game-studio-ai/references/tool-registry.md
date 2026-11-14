# Registro de ferramentas

Mantenha a lista curta e por tarefa. Não recomende ferramenta pela popularidade. Para cada opção, registre:

- função de produção e necessidade do projeto;
- fornecedor, plano/preço (com fonte e data) ou open-source;
- API/CLI/MCP e protocolo oficialmente documentados;
- plataformas/engine e formatos de importação/exportação;
- licença comercial, direitos de saída e restrições relevantes;
- credencial/permissão necessária, tratamento de dados e custo variável;
- alternativa offline/gratuita/manual;
- teste que confirma que está conectada e versão usada.

Para cada projeto, mantenha `studio/AI_INTEGRATIONS.md` como checklist humano e `studio/integrations.json` como manifesto sem valores secretos. Escolha um runtime/modelo central; registre serviços especializados por função. `scripts/check_integrations.py` confere estado declarado e presença dos nomes de variáveis no ambiente, mas não valida remotamente chaves, créditos, entitlement, licença ou operação MCP. Consulte `references/provider-authentication.md` para modos documentados e fontes.

Não torne toda a stack bloqueante para qualquer projeto. Uma conexão ausente bloqueia somente a tarefa que depende dela; tarefas locais ou de outros departamentos podem continuar. Não peça API keys no chat e não escreva valores no manifesto, GDD, arquivos de exemplo, commits ou logs. Não invente variáveis de ambiente; Playwright local e Blender MCP oficial não exigem API key de fornecedor.

Use estes estados: `candidate` (apenas hipótese), `documented` (docs consultadas), `configured` (configuração presente), `verified` (chamada/teste de integração realmente passou), `blocked` (dependência faltante) ou `retired`. Atualize `verified` somente após teste real. Não escreva tokens, endpoints privados ou segredos em GDD, commits, logs, prompts, manifests públicos ou arquivos de exemplo.

Uma integração só é funcional se: a ferramenta/documentação oficial existe; o cliente expõe o servidor/ferramenta; permissões e credenciais necessárias estão configuradas; uma operação de teste foi executada e observada. Caso contrário, explique o passo exato que falta.
