import subprocess
import os

# Caminho até o seu main.py
base_dir = os.path.join("docs", "code_wise", "codewise", "src", "codewise")
main_py = os.path.join(base_dir, "main.py")
resposta_path = os.path.join(base_dir, "resposta.txt")

# Descobre a branch atual via git
branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
print(f"➡️ Branch atual: {branch}")

# Executa o main.py
print("🚀 Rodando Codewise...")
subprocess.run(["py", "-3.11", main_py, "--repo", ".", "--branch", branch], check=True)

# Verifica se resposta.txt foi gerado
if not os.path.exists(resposta_path):
    print("❌ resposta.txt não encontrado!")
    exit(1)

# Lê o número do PR
pr_number = subprocess.check_output(["gh", "pr", "view", "--json", "number", "-q", ".number"]).decode().strip()

# Posta comentário no PR
print(f"📝 Comentando no PR #{pr_number}...")
with open(resposta_path, encoding="utf-8") as f:
    body = f.read()
    subprocess.run(["gh", "pr", "comment", pr_number, "--body", body[:65000]], check=True)

print("✅ Comentário postado com sucesso.")
