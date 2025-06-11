#!/bin/bash

set -e  # Para encerrar se algum erro ocorrer
cd "$(git rev-parse --show-toplevel)"  # Vai para o topo do repo

echo "🔍 Detectando branch atual..."
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "➡️ Branch atual: $BRANCH"

echo "🚀 Rodando Codewise para análise da branch..."
python3 ./docs/code_wise/codewise/src/codewise/main.py --repo . --branch "$BRANCH"

echo "📄 Lendo saída da análise (resposta.txt)..."
if [ ! -f resposta.txt ]; then
  echo "❌ Arquivo resposta.txt não encontrado!"
  exit 1
fi

# Pega número do PR (precisa estar em uma branch que esteja num PR ativo)
echo "🔎 Verificando número do Pull Request..."
PR_NUMBER=$(gh pr view --json number -q .number)

echo "📝 Postando comentário no PR #$PR_NUMBER..."
gh pr comment "$PR_NUMBER" --body "$(cat resposta.txt | head -c 65000)"

echo "✅ Comentário postado com sucesso!"
