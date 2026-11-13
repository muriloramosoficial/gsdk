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

Use estes estados: `candidate` (apenas hipótese), `documented` (docs consultadas), `configured` (configuração presente), `verified` (chamada/teste de integração realmente passou), `blocked` (dependência faltante) ou `retired`. Atualize `verified` somente após teste real. Não escreva tokens, endpoints privados ou segredos em GDD, commits, logs, prompts, manifests públicos ou arquivos de exemplo.

Uma integração só é funcional se: a ferramenta/documentação oficial existe; o cliente expõe o servidor/ferramenta; permissões e credenciais necessárias estão configuradas; uma operação de teste foi executada e observada. Caso contrário, explique o passo exato que falta.
