import os
import sys
from crew import Codewise
from entradagit import gerar_entrada_automatica

class CodewiseRunner:
    def __init__(self, caminho_entrada: str = "entrada.txt", caminho_saida: str = "resposta.txt"):
        self.caminho_entrada = caminho_entrada
        self.caminho_saida = caminho_saida
        self.arquivos_md_saida = [
            "arquitetura_atual.md",
            "analise_heuristicas_integracoes.md",
            "analise_solid.md",
            "padroes_de_projeto.md"
        ]

    def _ler_arquivo(self, file_path: str) -> str:
        """Lê o conteúdo de um arquivo de forma segura."""
        try:
            with open(file_path, "r", encoding="utf-8") as arquivo:
                return arquivo.read()
        except FileNotFoundError:
            print(f"Erro: Arquivo '{file_path}' não encontrado.")
            return ""

    def _mesclar_resultados_markdown(self):
        """Mescla os arquivos de análise Markdown em um único 'resposta.txt'."""
        print(">>> Mesclando resultados da análise...")
        with open(self.caminho_saida, "w", encoding="utf-8") as arquivo_saida:
            for caminho_md in self.arquivos_md_saida:
                if os.path.exists(caminho_md):
                    with open(caminho_md, "r", encoding="utf-8") as arquivo_md:
                        arquivo_saida.write(arquivo_md.read())
                        arquivo_saida.write("\n" + "="*80 + "\n\n")

    def executar(self, caminho_repo: str, nome_branch: str):
        # 1. Gera a entrada com base nos commits
        if not gerar_entrada_automatica(caminho_repo=caminho_repo, nome_branch=nome_branch):
            print("Execução abortada, pois não há commits pendentes para analisar.")
            sys.exit(0)

        # 2. Roda a equipe de análise principal
        print("\n>>> Iniciando análise principal do código...")
        mensagem_commit = self._ler_arquivo(self.caminho_entrada)
        if not mensagem_commit:
            print("Execução abortada, pois o arquivo de entrada está vazio.")
            sys.exit(1)
            
        codewise_analyzer = Codewise(commit_message=mensagem_commit)
        analysis_crew = codewise_analyzer.crew()
        analysis_crew.kickoff(inputs={"input": mensagem_commit})
        
        # 3. Mescla os resultados detalhados em 'resposta.txt'
        self._mesclar_resultados_markdown()
        print(f"\n>>> Análise completa salva em: {self.caminho_saida}")

        # 4. Roda a equipe de resumo e imprime o resultado
        print("\n>>> Gerando resumo da análise...")
        full_analysis_content = self._ler_arquivo(self.caminho_saida)

        if full_analysis_content.strip():
            # Usamos uma nova instância de Codewise para obter a equipe de resumo
            codewise_summarizer = Codewise()
            summarizer_crew = codewise_summarizer.summary_crew()
            
            # Passamos o conteúdo da análise como input para a tarefa de resumo
            summary_result = summarizer_crew.kickoff(inputs={'analysis_result': full_analysis_content})

            # Imprime o resumo final de forma destacada
            print("\n\n✅ Resumo da Análise Automática do Commit:")
            print("-" * 50)
            print(summary_result)
            print("-" * 50)
        else:
            print("Alerta: O arquivo de análise final está vazio. Resumo não foi gerado.")

