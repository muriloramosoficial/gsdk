#!/usr/bin/env python3
"""Create a minimal Game Studio AI project record without overwriting files."""
import argparse
from pathlib import Path
import re
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def slug(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip().lower()).strip("-")
    return text or "game-project"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", required=True, help="Existing game repository or chosen project directory")
    parser.add_argument("--name", required=True, help="Human-readable project name")
    parser.add_argument("--engine", default="A confirmar")
    parser.add_argument("--platform", default="A confirmar")
    args = parser.parse_args()

    root = Path(args.project_dir).expanduser().resolve()
    if not root.is_dir():
        print(f"ERRO: diretório não existe ou não é pasta: {root}", file=sys.stderr)
        return 2
    studio = root / "studio"
    if studio.exists():
        print(f"ERRO: {studio} já existe; revise-o manualmente. Nenhum arquivo foi alterado.", file=sys.stderr)
        return 3

    files = {
        "PROJECT.md": f"""# Projeto: {args.name}\n\n- Fase: discovery\n- Responsável humano: A definir\n- Engine/versão: {args.engine}\n- Plataforma(s): {args.platform}\n- Última atualização: {__import__('datetime').date.today().isoformat()}\n- Fonte de tarefas: studio/TASKS.md\n\n## Pitch\nA definir.\n\n## Próximo marco\nCriar e aprovar concept brief e escopo inicial.\n\n## Estado atual\n- Concluído com evidência: estrutura inicial de documentação criada pelo script.\n- Em andamento: nenhum.\n- Bloqueado: decisões de design pendentes.\n- Próximo: capturar intenção do criador e documentar premissas.\n\n## Premissas/riscos\n- Engine e plataformas são valores provisórios até confirmação.\n\n## Integrações verificadas\n- Nenhuma.\n""",
        "GDD.md": """# Game Design Document\n\n## Visão\n- High concept: A definir\n- Gênero / público / plataformas: A definir\n- Pilares (até 3): A definir\n- Fora de escopo: A definir\n\n## Experiência e loop principal\n- Fantasia do jogador: A definir\n- Loop de 30 segundos / 5 minutos / sessão: A definir\n- Condições de sucesso, falha e progressão: A definir\n\n## Sistemas e conteúdo\n- Controles: A definir\n- Mecânicas/sistemas: A definir\n- Personagens, cenários e conteúdo: A definir\n- Progressão/balanceamento: A definir\n- UX/acessibilidade: A definir\n\n## Produção e riscos\n- Protótipo a validar: A definir\n- Dependências e riscos: A definir\n- Critérios de sucesso: A definir\n- Decisões pendentes: A definir\n""",
        "TECH.md": f"# Documento técnico\n\n- Engine/versão: {args.engine}\n- Plataformas: {args.platform}\n- Linguagem/build/testes: A confirmar após inspeção do repositório.\n- Arquitetura: A definir após levantamento.\n- Dependências externas: Nenhuma registrada.\n- Comandos: Não confirmados.\n",
        "ART_BIBLE.md": "# Art Bible\n\nEstilo visual, paleta, resolução, proporções, tipografia, animação, convenções de nomes e assets aprovados: a definir. Registre fontes e licenças antes de redistribuir.\n",
        "AUDIO_PLAN.md": "# Plano de áudio\n\nObjetivos sonoros, estados, eventos, formatos, fontes, licenças e integração: a definir. Música é opcional até ser solicitada.\n",
        "ROADMAP.md": "# Roadmap\n\n## Discovery\n- [ ] Aprovar concept brief, pilares e escopo\n\n## Protótipo\n- [ ] Demonstrar o loop principal\n\n## Próximos marcos\n- [ ] Definir após validar riscos e estimativas\n",
        "TASKS.md": "# Backlog\n\n## GS-0001 — Aprovar conceito inicial\n- Tipo / prioridade / estado: design / P1 / proposed\n- Responsável: game-studio-director\n- Objetivo: documentar ideia, pilares, público/plataforma presumidos, loop e fora de escopo.\n- Entradas / saídas: ideia do criador / concept brief em studio/GDD.md\n- Dependências: descrição do criador\n- Critérios de aceite: concept brief compreensível, premissas identificadas e aprovado pelo criador.\n- Testes requeridos: revisão humana do conceito\n- Aprovação humana: pending\n- Evidência / resultado: pendente\n",
        "DECISIONS.md": "# Registro de decisões\n\nNenhuma decisão de produção aprovada.\n",
        "BUGS.md": "# Bugs\n\nNenhum bug registrado.\n",
        "AI_INTEGRATIONS.md": (PACKAGE_ROOT / "templates" / "AI_INTEGRATIONS.md").read_text(encoding="utf-8"),
        "integrations.json": (PACKAGE_ROOT / "templates" / "integrations.json").read_text(encoding="utf-8"),
    }
    studio.mkdir()
    created = []
    try:
        for name, content in files.items():
            path = studio / name
            if path.exists():
                raise FileExistsError(path)
            path.write_text(content, encoding="utf-8")
            created.append(path)
        changelog = root / "CHANGELOG.md"
        if not changelog.exists():
            changelog.write_text("# Changelog\n\n## Unreleased\n- Criados registros iniciais de produção do Game Studio AI.\n", encoding="utf-8")
            created.append(changelog)
    except Exception as exc:
        for path in created:
            path.unlink(missing_ok=True)
        studio.rmdir() if studio.exists() and not any(studio.iterdir()) else None
        print(f"ERRO: criação interrompida e arquivos novos revertidos: {exc}", file=sys.stderr)
        return 4

    print(f"Projeto inicializado sem sobrescrever arquivos existentes: {root}")
    print(f"Documentação criada: {studio}")
    for path in created:
        print(f"  - {path.relative_to(root)}")
    print("Atenção: isso cria documentação inicial; não instala engine, MCP, plugin ou ferramentas externas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
