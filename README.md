# 🧬 Buscador Científico Inteligente

[![Python Version](https.img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-ff69b4.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Acesse a aplicação em funcionamento:** [Buscador de Artigos Online](https://buscador-de-artigos-gzdephkfr3dkrnd4fdglzo.streamlit.app/)

O **Buscador Científico Inteligente** é uma aplicação web que utiliza o poder de Grandes Modelos de Linguagem (LLMs) para revolucionar a forma como pesquisadores e estudantes encontram artigos científicos. Em vez de buscas manuais e demoradas, a ferramenta automatiza a busca, análise e classificação de artigos, entregando apenas os resultados mais relevantes para o usuário.

## 🚀 Funcionalidades

*   **Busca Inteligente:** Utiliza um LLM para gerar variações otimizadas de termos de busca, aumentando a precisão dos resultados.
*   **Múltiplas Fontes:** Realiza buscas simultâneas em bases de dados acadêmicas renomadas como **ArXiv** e **Semantic Scholar**.
*   **Análise por IA:** Cada artigo encontrado é analisado por um modelo de IA que atua como um "Pesquisador Sênior" para:
    *   Traduzir títulos e resumos para o português.
    *   Atribuir uma **nota de relevância** (0 a 10) baseada no tema da pesquisa.
    *   Explicar a utilidade e o potencial do artigo para o usuário.
*   **Interface Intuitiva:** Apresenta os resultados de forma clara e organizada, separando os artigos mais relevantes para fácil visualização.
*   **Acesso Direto:** Fornece links diretos para o PDF dos artigos, quando disponíveis.

## ⚙️ Como Funciona

O fluxo de trabalho da aplicação é orquestrado por um agente de IA, seguindo os passos abaixo:

1.  **Entrada do Usuário:** O usuário insere um tema de pesquisa na interface web.
2.  **Geração de Queries:** A IA gera até 5 variações de busca em inglês, usando termos técnicos e sinônimos para maximizar a cobertura.
3.  **Busca Multi-Fonte:** O sistema consulta as APIs do ArXiv e Semantic Scholar com as queries geradas.
4.  **Análise e Classificação:** Os artigos coletados são enviados a um LLM, que analisa cada um e gera um "card" de informações contendo o título traduzido, resumo em português, nota de relevância, utilidade, ano e link.
5.  **Exibição dos Resultados:** A interface renderiza os cards, priorizando os artigos com nota de relevância mais alta (acima de 7).

## 🛠️ Tecnologias Utilizadas

*   **Backend:** Python
*   **Inteligência Artificial:** Google Gemini
*   **Interface Web:** Streamlit
*   **Fontes de Dados:** ArXiv, Semantic Scholar
*   **Bibliotecas Principais:** `google-genai`, `requests`, `arxiv`, `python-dotenv`

## 🏁 Como Executar o Projeto Localmente

Siga os passos abaixo para ter o projeto rodando em sua máquina.

### Pré-requisitos

*   Python 3.9 ou superior
*   Git

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Schinor/Buscador-de-Artigos.git
    cd Buscador-de-Artigos
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate

    # Para Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure sua chave de API:**
    *   Renomeie o arquivo `.env.example` para `.env`.
    *   Abra o arquivo `.env` e substitua `SUA_CHAVE_DE_API_AQUI` pela sua chave da API do Google Gemini.
      ```
      CHAVE_API=SUA_CHAVE_DE_API_AQUI
      ```

### Execução

Com o ambiente ativado e a chave configurada, inicie a aplicação com o seguinte comando:

```bash
streamlit run app.py
```

A aplicação estará disponível em seu navegador no endereço `http://localhost:8501`.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Sobre o Autor

**Marcio Gabriel Schinor Mazega**

*   **LinkedIn:** [www.linkedin.com/in/marcio-mazega](https://www.linkedin.com/in/marcio-mazega)
*   **GitHub:** [https://github.com/Schinor](https://github.com/Schinor)

---
*Este projeto foi desenvolvido como uma demonstração de como a IA pode ser usada para criar ferramentas poderosas e eficientes.*
