from google import genai
from core.config import settings

def gerar_resumo_ia(tema: str, lista_artigos: list, modelo: str = settings.DEFAULT_MODEL) -> str:
    if not lista_artigos:
        return ""

    client = genai.Client(api_key=settings.API_KEY)

    texto_contexto = f"Tema Pesquisado: '{tema}'.\n\nArtigos Encontrados:\n"
    
    for i, art in enumerate(lista_artigos):
        # Tratamento para evitar erro se algum campo vier vazio
        titulo = art.get('titulo', 'Sem título')
        fonte = art.get('fonte', 'Desconhecida')
        resumo = art.get('resumo', 'Sem resumo disponível')
        link = art.get('link', 'Sem link')
        data = art.get('data', 'N/D')

        texto_contexto += f"--- Artigo {i+1} ({fonte}) ---\n"
        texto_contexto += f"Titulo: {titulo}\n"
        texto_contexto += f"Data: {data}\n"
        texto_contexto += f"Resumo Original: {resumo}\n"
        texto_contexto += f"Link: {link}\n"
        texto_contexto += "-------------------\n"

    # O Prompt continua o mesmo, focado em qualidade
    prompt = f"""
    {texto_contexto}
    
    ATUE COMO: Pesquisador Sênior.
    TAREFA: Analise os artigos acima. Selecione os melhores para o tema '{tema}'.
    
    IMPORTANTE:
    - Se houver artigos de MEDICINA ou BIOLOGIA, dê preferência a eles se o tema pedir.
    - Ignore artigos que pareçam incompletos ou sem resumo.
    
    FORMATO DE SAÍDA (Obrigatório):
    
    Titulo: [Titulo Traduzido]
    Fonte: [ArXiv ou Semantic Scholar]
    Ano: [Ano]
    Link: [Link]
    Resumo: [Resumo em PT-BR]
    Utilidade: [Por que é útil]
    Relevancia: [Nota 0-10]
    ---
    """
    
    try:
        response = client.models.generate_content(
            model=modelo,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Erro na IA: {e}"

# Adicione isso em core/ai_processor.py

def gerar_queries_pesquisa(tema: str, modelo: str = settings.DEFAULT_MODEL) -> list:
    """
    Usa a IA para transformar um tema simples em 5 queries de busca acadêmica otimizadas (em Inglês).
    """
    client = genai.Client(api_key=settings.API_KEY)
    
    prompt = f"""
    ATUE COMO: Especialista em Bibliometria e Pesquisa Acadêmica.
    OBJETIVO: O usuário quer pesquisar sobre '{tema}'. Gere 5 variações de busca otimizadas para APIs acadêmicas (ArXiv/Semantic Scholar).
    
    REGRAS:
    1. AS QUERIES DEVEM SER EM INGLÊS (Língua padrão da ciência).
    2. Use termos técnicos precisos e palavras-chave.
    3. Varie os enfoques (Ex: Tecnologias específicas, Impacto, Visão Geral, Estado da Arte).
    4. NÃO numere as linhas, apenas retorne uma query por linha.
    5. NÃO use aspas nas queries, apenas texto puro.
    
    Exemplo de Saída para 'IA na Medicina':
    Artificial Intelligence in Medicine review
    Machine Learning diagnostic accuracy
    Deep Learning healthcare applications
    AI clinical decision support systems
    Natural Language Processing electronic health records
    """

    try:
        response = client.models.generate_content(
            model=modelo,
            contents=prompt
        )
        # Limpa e transforma em lista
        queries = [q.strip() for q in response.text.split('\n') if q.strip()]
        return queries[:5] # Garante no máximo 5
    except Exception as e:
        print(f"Erro ao gerar queries: {e}")
        return [tema] # Fallback: retorna o próprio tema se der erro