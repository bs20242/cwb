from git import Repo

def gerar_entrada_automatica(caminho_repo=".", caminho_saida="entrada.txt", quantidade=2, nome_branch="cwb"):
    repo = Repo(caminho_repo, search_parent_directories=True)    
    branch_local = repo.heads[nome_branch]
    branch_remota = repo.remotes.origin.refs[nome_branch]

    commits_pendentes = list(repo.iter_commits(f"{branch_remota}..{branch_local}"))

    if not commits_pendentes:
        print("Nenhum commit pendente de push encontrado.")
        return

    commits_selecionados = list(reversed(commits_pendentes[:quantidade]))

    entrada = []

    for commit_atual in commits_selecionados:
        commit_anterior = commit_atual.parents[0] if commit_atual.parents else None

        entrada.append("Mensagem do commit:")
        entrada.append(f"\"{commit_atual.message.strip()}\"\n")

        if commit_anterior:
            diffs = commit_anterior.diff(commit_atual, create_patch=True)
            for diff in diffs:
                if diff.change_type == "D":
                    continue
                arquivo = diff.b_path or diff.a_path

                entrada.append(f"Código atual:\n# Arquivo: {arquivo}")
                try:
                    blob_antigo = commit_anterior.tree / arquivo
                    entrada.append(blob_antigo.data_stream.read().decode("utf-8"))
                except Exception:
                    entrada.append("# Arquivo novo")

                entrada.append(f"\nCódigo alterado:\n# Arquivo: {arquivo}")
                try:
                    blob_novo = commit_atual.tree / arquivo
                    entrada.append(blob_novo.data_stream.read().decode("utf-8"))
                except Exception:
                    entrada.append("# Arquivo deletado")

                entrada.append("\n" + "=" * 80 + "\n")
        else:
            entrada.append("Nenhum commit anterior encontrado.\n")
            entrada.append("=" * 80 + "\n")

    with open(caminho_saida, "w", encoding="utf-8") as arquivo_saida:
        arquivo_saida.write("\n".join(entrada))

    print(f"{caminho_saida} gerado com os {len(commits_selecionados)} commits pendentes de push.") 
    return True