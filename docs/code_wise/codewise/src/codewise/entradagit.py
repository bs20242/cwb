from git import Repo

def gerar_entrada_automatica(caminho_repo=".", caminho_saida="entrada.txt"):
    repo = Repo(caminho_repo)
    head_commit = repo.head.commit
    parent_commit = head_commit.parents[0] if head_commit.parents else None

    entrada = []
    entrada.append("Mensagem do commit:")
    entrada.append(f"\"{head_commit.message.strip()}\"\n")

    if parent_commit:
        diffs = parent_commit.diff(head_commit, create_patch=True)
        for diff in diffs:
            if diff.change_type == "D":
                continue
            arquivo = diff.b_path or diff.a_path
            entrada.append(f"Código atual:\n# Arquivo: {arquivo}")
            try:
                blob_antigo = parent_commit.tree / arquivo
                entrada.append(blob_antigo.data_stream.read().decode("utf-8"))
            except Exception:
                entrada.append("# Arquivo novo")

            entrada.append(f"\nCódigo alterado:\n# Arquivo: {arquivo}")
            try:
                blob_novo = head_commit.tree / arquivo
                entrada.append(blob_novo.data_stream.read().decode("utf-8"))
            except Exception:
                entrada.append("# Arquivo deletado")

            entrada.append("\n" + "=" * 80 + "\n")
    else:
        entrada.append("Nenhum commit anterior encontrado.")

    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(entrada))
    print(f"entrada.txt gerado a partir do último commit.")
