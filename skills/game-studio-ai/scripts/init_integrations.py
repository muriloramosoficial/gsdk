#!/usr/bin/env python3
"""Add the Game Studio AI integration checklist to an existing project without overwriting files."""
import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = {
    "AI_INTEGRATIONS.md": PACKAGE_ROOT / "templates" / "AI_INTEGRATIONS.md",
    "integrations.json": PACKAGE_ROOT / "templates" / "integrations.json",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", required=True, help="Existing game repository or project directory")
    args = parser.parse_args()

    root = Path(args.project_dir).expanduser().resolve()
    if not root.is_dir():
        print(f"ERRO: diretório não existe ou não é pasta: {root}", file=sys.stderr)
        return 2
    studio = root / "studio"
    targets = {name: studio / name for name in TEMPLATES}
    missing = [(name, source) for name, source in TEMPLATES.items() if not targets[name].exists()]
    if not missing:
        print("Checklist/manifesto já existem; nenhum arquivo foi alterado.")
        return 0

    try:
        for _, template in missing:
            if not template.is_file():
                raise FileNotFoundError(template)
        studio.mkdir(exist_ok=True)
        created = []
        try:
            for name, source in missing:
                target = targets[name]
                with target.open("x", encoding="utf-8") as stream:
                    stream.write(source.read_text(encoding="utf-8"))
                created.append(target)
        except Exception:
            for path in created:
                path.unlink(missing_ok=True)
            if studio.exists() and not any(studio.iterdir()):
                studio.rmdir()
            raise
    except Exception as exc:
        print(f"ERRO: configuração não foi concluída: {exc}", file=sys.stderr)
        return 4

    print(f"Arquivos de integração adicionados em: {studio}")
    print("Nenhuma chave, token ou valor secreto foi solicitado ou gravado.")
    for name, _ in missing:
        print(f"  - {targets[name].relative_to(root)}")
    print("Leia AI_INTEGRATIONS.md, configure os logins/segredos fora do projeto e teste antes de marcar qualquer provider como verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
