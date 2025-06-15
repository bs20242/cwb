# que é o comando padrão do Python Launcher no Windows.
PYTHON = py

# O alvo 'auto' que você usa.
# Ele apenas executa o script principal. O script Python agora é autossuficiente.
auto:
	@echo "================================================="
	@echo "==    Iniciando a automação de PR do CodeWise  =="
	@echo "================================================="
	$(PYTHON) scripts/codewise_review_win.py

# Define 'auto' como o alvo padrão para que 'make' funcione sozinho.
.DEFAULT_GOAL := auto

# Comando 'clean' para limpar os arquivos temporários caso algo dê errado
clean:
	@echo "Limpando arquivos temporários..."
	-@del /Q titulo_pr.txt descricao_pr.txt analise_tecnica.txt > nul 2>&1

# Evita conflitos com nomes de arquivos.
.PHONY: auto clean