import os
import traceback
import argparse
from dotenv import load_dotenv
from cw_runner import CodewiseRunner

def main():
    load_dotenv()
    print("Modelo em uso:", os.getenv("MODEL_NAME"))

    parser = argparse.ArgumentParser(description="Code Wise - Ferramenta de Análise de Código com IA.")
    parser.add_argument(
        "--repo",
        type=str,
        default=".",
        help="Caminho para o repositório Git que você deseja analisar."
    )
    # --- NOVA LINHA ADICIONADA ---
    parser.add_argument(
        "--branch",
        type=str,
        default="cwb", # Mantemos 'cwb' como padrão, mas agora pode ser alterado
        help="Nome da branch que você deseja analisar."
    )
    args = parser.parse_args()

    try:
        runner = CodewiseRunner()
        # --- LINHA MODIFICADA ---
        # Agora passamos tanto o repositório quanto a branch
        runner.executar(caminho_repo=args.repo, nome_branch=args.branch) 
    except Exception:
        print("Erro ao executar:")
        traceback.print_exc()

if __name__ == "__main__":
    main()