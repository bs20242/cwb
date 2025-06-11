import os
import sys
from crew import Codewise
from entradagit import gerar_entrada_automatica

class CodewiseRunner:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        self.caminho_entrada = os.path.join(self.BASE_DIR, "entrada.txt")
        self.caminho_saida = os.path.join(self.BASE_DIR, "resposta.txt")
        self.arquivos_md_saida = [
            os.path.join(self.BASE_DIR, "arquitetura_atual.md"),
            os.path.join(self.BASE_DIR, "analise_heuristicas_integracoes.md"),
            os.path.join(self.BASE_DIR, "analise_solid.md"),
            os.path.join(self.BASE_DIR, "padroes_de_projeto.md")
        ]

    def _ler_arquivo(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as arquivo:
                return arquivo.read()
        except FileNotFoundError:
            print(f"Erro: Arquivo '{file_path}' não encontrado.")
            return ""

    def _mesclar_resultados_markdown(self):
        print(">>> Mesclando resultados da análise...")
        with open(self.caminho_saida, "w", encoding="utf-8") as arquivo_saida:
            for caminho_md in self.arquivos_md_saida:
                if os.path.exists(caminho_md):
                    with open(caminho_md, "r", encoding="utf-8") as arquivo_md:
                        arquivo_saida.write(arquivo_md.read())
                        arquivo_saida.write("\n" + "="*80 + "\n\n")

    def executar(self, caminho_repo: str, nome_branch: str):
        if not gerar_entrada_automatica(
            caminho_repo=caminho_repo,
            caminho_saida=self.caminho_entrada,
            nome_branch=nome_branch
        ):
            print("Execução abortada, pois não há commits pendentes para analisar.")
            sys.exit(0)

        print("\n>>> Iniciando análise principal do código...")
        mensagem_commit = self._ler_arquivo(self.caminho_entrada)
        if not mensagem_commit:
            print("Execução abortada, pois o arquivo de entrada está vazio.")
            sys.exit(1)

        codewise_analyzer = Codewise(commit_message=mensagem_commit)
        analysis_crew = codewise_analyzer.crew()

        analysis_crew.kickoff(inputs={"input": mensagem_commit})

        self._mesclar_resultados_markdown()
        print(f"\n>>> Análise completa salva em: {self.caminho_saida}")

        print("\n>>> Gerando resumo da análise...")
        full_analysis_content = self._ler_arquivo(self.caminho_saida)

        if full_analysis_content.strip():
            codewise_summarizer = Codewise(commit_message="")

            summarizer_crew = codewise_summarizer.summary_crew()

            summary_result = summarizer_crew.kickoff(inputs={'analysis_result': full_analysis_content})

            print("\n\n✅ Resumo da Análise Automática do Commit:")
            print("-" * 50)
            print(summary_result)
            print("-" * 50)
        else:
            print("Alerta: O arquivo de análise final está vazio. Resumo não foi gerado.")
