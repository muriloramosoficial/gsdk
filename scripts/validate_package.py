#!/usr/bin/env python3
"""Structural checks for the GAME STUDIO AI distribution; no harness install is performed."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ".claude-plugin/plugin.json",
    "README.md",
    "LICENSE",
    "skills/game-studio-ai/SKILL.md",
    "skills/start/SKILL.md",
    "skills/game-studio-ai/references/provider-authentication.md",
    "skills/game-studio-ai/scripts/init_project.py",
    "skills/game-studio-ai/scripts/init_integrations.py",
    "skills/game-studio-ai/scripts/check_integrations.py",
    "skills/game-studio-ai/templates/AI_INTEGRATIONS.md",
    "skills/game-studio-ai/templates/integrations.json",
    "agents/game-studio-director.md",
    "docs/adapter-matrix.md",
    "docs/installation.md",
    "docs/validation-report.md",
    "scripts/init_project.py",
    "scripts/init_integrations.py",
    "scripts/check_integrations.py",
    "scripts/install_skill.py",
    "scripts/validate_package.py",
    "tests/test_init_project.py",
    "tests/test_init_integrations.py",
    "tests/test_check_integrations.py",
    "templates/AI_INTEGRATIONS.md",
    "templates/integrations.json",
]
errors = []
for rel in REQUIRED:
    if not (ROOT / rel).is_file():
        errors.append(f"arquivo obrigatório ausente: {rel}")

manifest = ROOT / ".claude-plugin/plugin.json"
if manifest.exists():
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for key in ("name", "version", "description"):
            if not isinstance(data.get(key), str) or not data[key].strip():
                errors.append(f"manifesto: campo ausente/inválido: {key}")
        if data.get("name") != "game-studio":
            errors.append("manifesto: esperado name=game-studio para o namespace dos comandos")
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"manifesto JSON inválido: {exc}")

integration_template = ROOT / "templates/integrations.json"
if integration_template.exists():
    try:
        data = json.loads(integration_template.read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or not isinstance(data.get("task_requirements"), dict):
            errors.append("template integrations.json: schema_version ou task_requirements inválido")
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"template integrations.json inválido: {exc}")

skill_files = list((ROOT / "skills").glob("*/SKILL.md")) if (ROOT / "skills").exists() else []
if not skill_files:
    errors.append("nenhuma skill de plugin encontrada")
for path in skill_files:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or text.count("\n---\n") < 1:
        errors.append(f"frontmatter ausente ou malformado: {path.relative_to(ROOT)}")
    if "[TODO" in text:
        errors.append(f"TODO de template não removido: {path.relative_to(ROOT)}")
    if len(text.splitlines()) > 500:
        errors.append(f"skill excede 500 linhas: {path.relative_to(ROOT)}")

for path in (ROOT / "agents").glob("*.md") if (ROOT / "agents").exists() else []:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "name:" not in text[:500] or "description:" not in text[:500]:
        errors.append(f"metadados básicos de agente ausentes: {path.relative_to(ROOT)}")

for path in ROOT.rglob("*.md"):
    if any(part in {".git", "node_modules"} for part in path.parts):
        continue
    text = path.read_text(encoding="utf-8")
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1)
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        resolved = (path.parent / target.split("#", 1)[0]).resolve()
        if target.split("#", 1)[0] and not resolved.exists():
            errors.append(f"link local quebrado em {path.relative_to(ROOT)}: {target}")

if errors:
    print("VALIDAÇÃO ESTRUTURAL: FALHOU")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("VALIDAÇÃO ESTRUTURAL: OK")
print(f"Pacote: {ROOT}")
print(f"Skills encontradas: {len(skill_files)}")
print("Verificado: manifesto do plugin, template JSON, arquivos esperados, frontmatter, limites de linhas e links relativos Markdown.")
print("Não verificado: login ou chamada real de provider, credenciais, permissões/custos, instalação dos harnesses/MCP, build de jogo ou publicação.")
