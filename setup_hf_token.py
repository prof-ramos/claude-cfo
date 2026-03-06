#!/usr/bin/env python3
"""
Script para configurar o token do Hugging Face e fazer deploy.

Instruções:
1. Acesse: https://huggingface.co/settings/tokens
2. Crie um token com permissão "Write"
3. Execute: uv run python setup_hf_token.py
"""

import os
import subprocess

from huggingface_hub import login

# Configurações do Hugging Face Space
HF_SPACE_USER = os.environ.get("HF_SPACE_USER", "profgabrielramos")
HF_SPACE_NAME = os.environ.get("HF_SPACE_NAME", "claude-cfo")
HF_SPACE_URL = f"https://huggingface.co/spaces/{HF_SPACE_USER}/{HF_SPACE_NAME}"
HF_APP_URL = f"https://{HF_SPACE_USER}-{HF_SPACE_NAME}.hf.space/"


def main():
    print("=== Configuração do Deploy Hugging Face ===\n")
    print("Para configurar o token:")
    print("1. Acesse: https://huggingface.co/settings/tokens")
    print("2. Crie um token com permissão 'Write'")
    print("")

    # Ler token do ambiente ou input
    token = os.environ.get("HF_TOKEN")
    if not token:
        token = input("Cole o token do Hugging Face aqui: ").strip()

    if not token:
        print("✗ Token não fornecido")
        return 1

    try:
        # Fazer login
        print("\n🔐 Fazendo login no Hugging Face...")
        login(token, add_to_git_credential=True)

        # Fazer push para o Space
        print("\n🚀 Fazendo deploy para o Hugging Face Space...")
        result = subprocess.run(
            ["git", "push", "hf-space", "main", "--force-with-lease"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✓ Deploy realizado com sucesso!")
            print(f"📦 Space: {HF_SPACE_URL}")
            print(f"🌐 URL: {HF_APP_URL}")
            return 0
        else:
            print(f"✗ Erro no deploy: {result.stderr}")
            return 1

    except Exception as e:
        print(f"✗ Erro: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
