CodeWise - Sugestão de Melhorias Arquiteturais via Commit

 Funcionalidade

nosso sistema utiliza agentes baseados na LLM (gemini/gemini-2.0-flash) para analisar uma mudança de código fornecida em um commit e gerar relatórios automatizados, incluindo:

- Estrutura do projeto
- Heurísticas de integração
- Análise baseada em princípios SOLID
- Padrões de projeto aplicáveis

Como funciona

1. O programa no momento recebe uma entrada.txt que pretende ser gerada com base no ultimo commit dado no repositório, com os dados a serem analisados, e então cada agente gera um arquivo markdown de sua análise, no final gerando uma resposta.txt com a unificação de todas as respostas dos agentes.

