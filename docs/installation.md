# Instalação e configuração

## Claude Code — testar o plugin local

Extraia o pacote para uma pasta conhecida. Abra o terminal nessa pasta e inicie uma sessão com o plugin local:

```bash
claude --plugin-dir /caminho/para/GAME-STUDIO-AI
```

A documentação oficial descreve `--plugin-dir` como forma de carregar diretamente um plugin durante desenvolvimento, sem marketplace. Na sessão, rode `/plugin` para conferir se o plugin está carregado e execute `/game-studio:start`. A sessão de diretório local é apropriada para testar; para instalação persistente ou distribuição para uma equipe, crie/adicione um marketplace segundo a documentação oficial. Este pacote não inclui um marketplace, pois faltam repositório remoto e namespace da organização.

Depois de extrair, um primeiro teste de apenas leitura pode ser `/game-studio:team` ou `/game-studio:status`. `/game-studio:start` pede a ideia, cria plano e espera aprovação antes de preparar produção.

## Codex CLI e OpenCode

Com o repositório do jogo já existente, rode do pacote:

```bash
python3 scripts/install_skill.py --target codex --project-dir /caminho/do/jogo
python3 scripts/install_skill.py --target opencode --project-dir /caminho/do/jogo
```

Escolha **um** dos comandos conforme o harness. O instalador copia somente a skill central e recusa destino existente, sem sobrescrever ou criar configuração MCP. Reinicie/atualize o harness se a nova skill não for descoberta. Agentes, modelo e permissões precisam da configuração específica do destino; exemplos e limites ficam em `adapters/codex/`, `adapters/opencode/` e `docs/adapter-matrix.md`.

## DeepSeek Harness (`dsh`)

Confira a versão e o mecanismo oficial de profiles/plugins no runtime instalado. As fontes consultadas identificam `dsh` como developer preview, mas não confirmam importação direta deste formato de skill. Não rode instalador que suponha um diretório não documentado. Injete a skill somente se o profile/plugin suportar explicitamente instruções ou arquivos de referência; do contrário, use o texto da skill manualmente e registre que delegação/MCP não está integrada.

## MCP

MCP não é requisito para começar. Primeiro escolha o servidor e a ferramenta que atendem uma necessidade do jogo. Configure o servidor no cliente/harness apropriado, com menor escopo possível e credenciais fora do repositório. Confirme lista de tools e schemas, depois teste leitura inofensiva. Libere escrita apenas para as funções necessárias. Este pacote não oferece um endpoint, serviço de gestão de assets, issue tracker, engine, modelo nem chave de API.

## Fontes oficiais

- [Claude Code — plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code — criar/testar plugin local](https://code.claude.com/docs/en/plugins/create)
- [Claude Code — instalar/gerir plugins](https://code.claude.com/docs/en/plugins/install)
- [Codex — skills](https://developers.openai.com/codex/build-skills)
- [OpenCode — skills](https://opencode.ai/docs/skills/)
- [DeepSeek Harness — CLI](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/README.md)
