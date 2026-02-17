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