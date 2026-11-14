#!/usr/bin/env python3
"""Check declared runtime/provider readiness without reading or printing secret values."""
import argparse
import json
import os
from pathlib import Path
import re
import sys

NO_MODEL_TASKS = {"local-docs", "project-inspection"}
ENV_NAME = re.compile(r"[A-Z][A-Z0-9_]{0,127}\Z")
ALLOWED_STATUSES = {"pending", "not_configured", "configured", "verified", "not_applicable"}


def read_env_names(entry, label, errors):
    names = entry.get("secret_env", [])
    if not isinstance(names, list):
        errors.append(f"{label}: secret_env deve ser uma lista de nomes; valor ignorado.")
        return []
    valid = []
    for name in names:
        if not isinstance(name, str) or not ENV_NAME.fullmatch(name):
            errors.append(f"{label}: nome de variável inválido/omitido (valor redigido).")
        else:
            valid.append(name)
    return valid


def check_entry(entry, label, errors):
    if not isinstance(entry, dict):
        errors.append(f"{label}: entrada inválida.")
        return
    status = entry.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"{label}: estado inválido; use pending/not_configured/configured/verified/not_applicable.")
    if status != "verified":
        errors.append(f"{label}: não está verified após teste observado; conteúdo do campo omitido por segurança.")
    if not isinstance(entry.get("auth_mode"), str) or not entry.get("auth_mode", "").strip():
        errors.append(f"{label}: defina auth_mode (por exemplo, oauth-login, subscription-login, api-key ou local-mcp).")
    for name in read_env_names(entry, label, errors):
        if not os.environ.get(name):
            errors.append(f"{label}: variável {name} ausente no ambiente do processo.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", required=True, help="Raiz do jogo que contém studio/integrations.json")
    parser.add_argument("--task", default="model-inference", help="Capacidade a liberar; padrão model-inference")
    args = parser.parse_args()

    manifest_path = Path(args.project_dir).expanduser().resolve() / "studio" / "integrations.json"
    if not manifest_path.is_file():
        print(f"Bloqueado: manifesto não encontrado: {manifest_path}")
        print("Crie/atualize o projeto com init_project.py e configure studio/AI_INTEGRATIONS.md.")
        return 1
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print("Erro: integrations.json não pôde ser lido como JSON válido.")
        return 2
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        print("Erro: formato de integrations.json inválido ou não suportado.")
        return 2

    task_requirements = manifest.get("task_requirements", {})
    providers = manifest.get("providers", [])
    if not isinstance(task_requirements, dict) or not isinstance(providers, list):
        print("Erro: task_requirements/providers devem ser objeto/lista.")
        return 2
    if args.task not in NO_MODEL_TASKS | {"model-inference"} and args.task not in task_requirements:
        print(f"Erro: capacidade desconhecida: {args.task}")
        print("Consulte as chaves de studio/integrations.json ou adicione uma capacidade própria.")
        return 2

    errors = []
    if args.task not in NO_MODEL_TASKS:
        runtime = manifest.get("runtime")
        if not isinstance(runtime, dict):
            errors.append("runtime: escolha um único provider/modelo central.")
        else:
            if not isinstance(runtime.get("provider"), str) or not runtime.get("provider", "").strip():
                errors.append("runtime: escolha provider (Claude Code, Codex CLI, OpenCode, DeepSeek Harness ou outro).")
            check_entry(runtime, "runtime central", errors)

    selected_ids = task_requirements.get(args.task, [])
    if not isinstance(selected_ids, list) or any(not isinstance(item, str) for item in selected_ids):
        print("Erro: o requisito desta tarefa deve ser uma lista de IDs de providers.")
        return 2
    provider_map = {}
    for item in providers:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            print("Erro: entrada de provider inválida; conteúdo redigido.")
            return 2
        provider_id = item["id"]
        if not re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", provider_id):
            print("Erro: ID de provider inválido; conteúdo redigido.")
            return 2
        provider_map[provider_id] = item

    for provider_id in selected_ids:
        entry = provider_map.get(provider_id)
        if entry is None:
            errors.append("provider necessário não está cadastrado (ID omitido por segurança).")
            continue
        check_entry(entry, f"provider {provider_id}", errors)

    if errors:
        print(f"PRE-FLIGHT BLOQUEADO para '{args.task}':")
        for error in errors:
            print(f"- {error}")
        print("Nenhum valor secreto foi lido ou impresso. Configure a conexão fora do chat e teste-a no harness.")
        return 1

    labels = ", ".join(selected_ids) if selected_ids else "nenhuma integração externa selecionada; fluxo manual/local"
    if args.task not in NO_MODEL_TASKS:
        labels = "runtime central + " + labels
    print(f"PRE-FLIGHT DECLARADO COMO VERIFIED para '{args.task}': {labels}.")
    print("Este script valida somente o manifesto e a presença de nomes de variáveis; não faz chamada remota nem valida licença, custo ou saldo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
