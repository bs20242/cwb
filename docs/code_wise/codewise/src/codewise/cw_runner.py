import os
import sys
from crew import Codewise
from entradagit import gerar_entrada_automatica
from crewai import Task, Crew, Process

class CodewiseRunner:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.caminho_entrada = os.path.join(self.BASE_DIR, "entrada.txt")
        self.arquivos_analise_intermediarios = [
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

    def _limpar_arquivos_intermediarios(self):
        """Deleta os arquivos .md individuais após a análise."""
        for caminho_md in self.arquivos_analise_intermediarios:
            if os.path.exists(caminho_md):
                os.remove(caminho_md)

    def executar(self, caminho_repo: str, nome_branch: str, modo: str, caminho_saida: str):
        """Orquestra a execução da análise ou da descrição com base no modo."""
        if not gerar_entrada_automatica(
            caminho_repo=caminho_repo,
            caminho_saida=self.caminho_entrada,
            nome_branch=nome_branch
        ):
            print("Execução abortada, pois não há commits pendentes para analisar.")
            sys.exit(0)

        git_diff_content = self._ler_arquivo(self.caminho_entrada)
        if not git_diff_content:
            print("Execução abortada, pois o arquivo de entrada gerado pelo git está vazio.")
            sys.exit(1)
            
        codewise_instance = Codewise(commit_message=git_diff_content)

        if modo == 'analise':
            print("\n>>> Iniciando MODO DE ANÁLISE TÉCNICA...")
            analysis_crew = codewise_instance.crew()
            analysis_crew.kickoff(inputs={"input": git_diff_content})
            
            print("\n>>> Gerando análise técnica detalhada...")
            
            relatorio_completo = ""
            for caminho_md in self.arquivos_analise_intermediarios:
                 if os.path.exists(caminho_md):
                    relatorio_completo += self._ler_arquivo(caminho_md) + "\n\n"

            resumo_agent = codewise_instance.summary_specialist()
            
            # --- PROMPT AJUSTADO PARA MAIOR DETALHE ---
            resumo_task = Task(
                description=f"""
                    Você é um Tech Lead sênior revisando um Pull Request.
                    Com base nos relatórios técnicos detalhados abaixo, e nos diffs de código originais, crie uma revisão de código construtiva.

                    **Sua resposta DEVE seguir este formato:**
                    1. Comece com um título: `### Análise Técnica e Sugestões de Melhoria`.
                    2. Para cada ponto importante, crie uma seção com um subtítulo em negrito (ex: **Refatoração da Estrutura**).
                    3. Na seção, explique o problema e a sugestão.
                    4. **Mais importante:** Sempre que sua sugestão se referir a uma mudança de código específica, cite o trecho de código relevante do 'diff' original para dar contexto. Use blocos de código markdown para isso.

                    **Relatórios para análise:**
                    {relatorio_completo}

                    **Diff de código original (para referência):**
                    {git_diff_content}
                """,
                expected_output="Uma revisão de código detalhada em markdown, com subtítulos, explicações e trechos de código relevantes.",
                agent=resumo_agent
            )

            resumo_crew = Crew(agents=[resumo_agent], tasks=[resumo_task], process=Process.sequential)
            resultado_final_analise = resumo_crew.kickoff()
            
            print("\n\n✅ Análise Técnica Detalhada gerada:")
            print("-" * 50); print(resultado_final_analise); print("-" * 50)
            
            with open(caminho_saida, "w", encoding="utf-8") as f:
                f.write(str(resultado_final_analise))
                
            print(f">>> Análise salva em: {caminho_saida}")
            self._limpar_arquivos_intermediarios()


        elif modo == 'descricao':
            print("\n>>> Iniciando MODO DE DESCRIÇÃO DE PR...")
            desc_agent = codewise_instance.summary_specialist()
            desc_task = Task(
                description=f"""
                    Baseado nos seguintes commits e mudanças, gere uma descrição de um parágrafo para um Pull Request.
                    O texto deve ser em Português do Brasil, objetivo e explicar o que foi feito.
                    Foque no propósito da mudança, não nos detalhes técnicos.

                    Dados para análise:
                    {git_diff_content}
                """,
                expected_output="Um único parágrafo de texto que resuma as mudanças para a descrição de um Pull Request.",
                agent=desc_agent
            )

            desc_crew = Crew(agents=[desc_agent], tasks=[desc_task], process=Process.sequential)
            resultado_descricao = desc_crew.kickoff()
            
            print("\n\n✅ Descrição do PR gerada:")
            print("-" * 50); print(resultado_descricao); print("-" * 50)

            with open(caminho_saida, "w", encoding="utf-8") as f:
                f.write(str(resultado_descricao))
            print(f">>> Descrição salva em: {caminho_saida}")
