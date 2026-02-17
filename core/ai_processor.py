from google import genai
from core.config import settings

def gerar_queries_pesquisa(tema: str, modelo: str = settings.DEFAULT_MODEL) -> list:
    """
    Gera variações de busca em inglês para melhorar a cobertura.
    """
    client = genai.Client(api_key=settings.API_KEY)
    
    prompt = f"""
    ATUE COMO: Especialista em Pesquisa Acadêmica.
    OBJETIVO: O usuário quer pesquisar sobre '{tema}'. Gere 5 variações de busca otimizadas (Keywords) para APIs acadêmicas.
    
    REGRAS:
    1. AS QUERIES DEVEM SER EM INGLÊS.
    2. Use termos técnicos precisos.
    3. NÃO numere, apenas uma query por linha.
    4. NÃO use aspas.
    """

    try:
        response = client.models.generate_content(
            model=modelo,
            contents=prompt
        )
        # Limpa e transforma em lista
        queries = [q.strip() for q in response.text.split('\n') if q.strip()]
        return queries[:4] # Limita a 4 para não demorar demais
    except Exception:
        return [tema] 

# --- FUNÇÃO DE RESUMO (MANTIDA IGUAL, SÓ O PROMPT AJUSTADO) ---
def gerar_resumo_ia(tema: str, lista_artigos: list, modelo: str = settings.DEFAULT_MODEL) -> str:
    if not lista_artigos:
        return ""

    client = genai.Client(api_key=settings.API_KEY)

    texto_contexto = f"Tema Pesquisado: '{tema}'.\n\nArtigos Encontrados:\n"
    
    for i, art in enumerate(lista_artigos):
        # ... (código de extração igual ao anterior) ...
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

    prompt = f"""
    {texto_contexto}
    
    ATUE COMO: Pesquisador Sênior.
    TAREFA: Analise os artigos.
    
    FORMATO DE SAÍDA (Obrigatório):
    
    Titulo: [Titulo Traduzido]
    Fonte: [ArXiv ou Semantic Scholar]
    Ano: [Ano]
    Link: [Apenas a URL pura, ex: https://arxiv.org/pdf/...]
    Resumo: [Resumo em PT-BR]
    Utilidade: [Por que é útil]
    Relevancia: [Nota numérica de 0 a 10 baseada na conexão com '{tema}']
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