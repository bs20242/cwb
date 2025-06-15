
CodeWise- é uma ferramenta de linha de comando que utiliza o poder de modelos de linguagem (via CrewAI) para automatizar a criação e o enriquecimento de Pull Requests no GitHub.

## Funcionalidades Principais
- **Geração de Título:** Cria títulos de PR claros e concisos seguindo o padrão *Conventional Commits*.
- **Geração de Descrição:** Escreve descrições detalhadas baseadas nas alterações do código.
- **Análise Técnica:** Posta um comentário no PR com um resumo executivo das melhorias de arquitetura, aderência a princípios S.O.L.I.D. e outros pontos de qualidade.
- **Automação Completa:** Integra-se ao seu fluxo de trabalho Git para rodar automaticamente a cada `git push`.

## Pré-requisitos

Antes de começar, garanta que você tenha as seguintes ferramentas instaladas em seu sistema:
1.  **Python** (versão 3.11 ou superior)
2.  **Git**
3.  **GitHub CLI (`gh`)**: Após instalar, autentique-se com o GitHub executando `gh auth login` no seu terminal.

####################### Instalação (Apenas uma vez) #########################################

Para instalar a ferramenta CodeWise-PR e suas dependências no seu computador, siga estes passos:

1.  Clone este repositório:
    ```bash
    git clone [https://github.com/bs20242/cwb.git](https://github.com/bs20242/cwb.git) CodeWise
    ```
2.  Navegue até a pasta do projeto:
    ```bash
    win: cd C:\Users\SeuUsuario\CodeWise
    linux: cd /c/Users/SeuUsuario/CodeWise

2.1  Crie e ative o ambiente virtual:
    ```bash
    # Cria a pasta do ambiente virtual
    py -m venv .venv

    # Ativa o ambiente (o prompt do seu terminal deve mudar)
    # No Windows (PowerShell/CMD):
    .\.venv\Scripts\activate
    ```
    ```
3.  Instale as dependências e a ferramenta:
    ```bash
    # Instala pacotes como CrewAI, etc.
    py -m pip install -r requirements.txt

    # Instala a ferramenta e os comandos 'codewise-pr' e 'codewise-init'
    py -m pip install -e .
    ```
## se quiser criar um novo repositorio na máquina pelo prompt:
( mkdir MeuNovoProjeto 
cd MeuNovoProjeto
git init
gh repo create MeuNovoProjeto --public --source=. --remote=origin
# (Crie seu primeiro arquivo, ex: README.md)
git add .
git commit -m "Primeiro commit"
git push --set-upstream origin main (ou master, dependendo do seu Git)
)
#############################################################################################################################################
Após estes passos, a ferramenta estará instalada e pronta para ser configurada em qualquer um dos seus projetos.

######################## Como Usar #######################################

Para cada repositório Git em que você desejar usar a automação, basta fazer uma configuração inicial de 10 segundos.

#### **Passo 1: Navegue até o seu Repositório**

```bash
# Exemplo: configurando para o projeto C_lib
cd /caminho/para/seu/C_lib
```

#### **Passo 2: Ative a Automação**

# Para ativar AMBAS as automações (Recomendado)
codewise-init --all
```
Você verá uma mensagem de sucesso confirmando que a automação está ativa.
*(**Opcional:** use `--commit` para ativar apenas a análise rápida ou `--push` para ativar apenas a automação de PR).*

## Fluxo de Trabalho do Dia a Dia
Com a configuração concluída, seu fluxo de trabalho se torna mais inteligente:

1.  Trabalhe normalmente em uma branch separada (ex: `minha-feature`).
2.  Adicione suas alterações para o próximo commit:
    ```bash
    git add .
    ```
3.  Faça o commit:
    ```bash
    git commit -m "feat: implementa novo recurso X"
    ```
    Neste momento, o **hook `pre-commit` será ativado**. Você verá a análise rápida do `codewise-lint` aparecer no seu terminal com sugestões de melhoria antes mesmo de o commit ser finalizado.

4.  Envie suas alterações para o GitHub:
    ```bash
    git push
    ```
    Agora, o **hook `pre-push` será ativado**. O `codewise-pr` irá criar ou atualizar seu Pull Request no GitHub com título, descrição e um comentário de análise técnica, tudo gerado por IA.

---
*Este projeto foi desenvolvido como uma ferramenta para otimizar o processo de code review e documentação de software.*