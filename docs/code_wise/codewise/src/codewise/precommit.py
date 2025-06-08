import sys
import os
from cw_runner import CodewiseRunner

def run_pre_commit_analysis():
    repo_path = "."  # pasta raiz do projeto
    branch_name = "cwb"  # ajuste se necessário

    print("🔍 Rodando CodeWise (pré-commit)...")

    runner = CodewiseRunner()
    runner.executar(caminho_repo=repo_path, nome_branch=branch_name)

    if not os.path.exists("resposta.txt"):
        print("❌ Análise falhou. Commit bloqueado.")
        sys.exit(1)

    print("✅ Análise concluída. Commit liberado.")

if __name__ == "__main__":
    run_pre_commit_analysis()
