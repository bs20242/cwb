# scripts/install_hook.py

import os
import sys
import stat

# Conteúdo que será escrito no arquivo do hook pre-push
HOOK_CONTENT = """#!/bin/sh
# Hook que executa a ferramenta CodeWise. Gerado por 'codewise-init'.
set -e

echo "--- [HOOK PRE-PUSH CodeWise ATIVADO] ---"
codewise-pr
echo "--- [HOOK PRE-PUSH CodeWise CONCLUÍDO] ---"
exit 0
"""

def main():
    """
    Encontra o diretório .git/hooks e instala o script pre-push.
    """
    print("🚀 Iniciando configuração do hook pre-push do CodeWise...")

    # O script roda a partir do diretório raiz do repositório do usuário
    repo_root = os.getcwd()
    hooks_dir = os.path.join(repo_root, '.git', 'hooks')

    if not os.path.isdir(hooks_dir):
        print(f"❌ Erro: O diretório de hooks do Git não foi encontrado em '{hooks_dir}'.")
        print("Você está executando este comando a partir da raiz de um repositório Git?")
        sys.exit(1)

    pre_push_path = os.path.join(hooks_dir, 'pre-push')

    try:
        with open(pre_push_path, 'w') as f:
            f.write(HOOK_CONTENT)
        print(f"✅ Arquivo de hook criado em: {pre_push_path}")

        # Torna o arquivo executável (essencial para Linux/macOS e boa prática no Windows com Git Bash)
        st = os.stat(pre_push_path)
        os.chmod(pre_push_path, st.st_mode | stat.S_IEXEC)
        print("✅ Permissão de execução concedida ao hook.")
        print("\n🎉 Configuração concluída! A automação está ativa para este repositório.")

    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado ao configurar o hook: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()