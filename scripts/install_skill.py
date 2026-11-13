#!/usr/bin/env python3
"""Install the portable Game Studio AI skill into a Codex or OpenCode project."""
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "game-studio-ai"
DESTINATIONS = {
    "codex": Path(".agents/skills/game-studio-ai"),
    "opencode": Path(".opencode/skills/game-studio-ai"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, choices=sorted(DESTINATIONS))
    parser.add_argument("--project-dir", required=True, help="Existing project/repository directory")
    args = parser.parse_args()
    project = Path(args.project_dir).expanduser().resolve()
    if not project.is_dir():
        print(f"ERRO: diretório do projeto não existe: {project}", file=sys.stderr)
        return 2
    if not (SOURCE / "SKILL.md").is_file():
        print(f"ERRO: núcleo da skill não encontrado: {SOURCE}", file=sys.stderr)
        return 3
    destination = project / DESTINATIONS[args.target]
    if destination.exists():
        print(f"ERRO: destino já existe; nada foi alterado: {destination}", file=sys.stderr)
        return 4
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copytree(SOURCE, destination)
    except Exception as exc:
        shutil.rmtree(destination, ignore_errors=True)
        print(f"ERRO: instalação cancelada e cópia parcial removida: {exc}", file=sys.stderr)
        return 5
    print(f"Skill instalada para {args.target}: {destination}")
    print("Os subagentes e servidores MCP são configuração separada. Nenhuma credencial ou MCP foi criado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
