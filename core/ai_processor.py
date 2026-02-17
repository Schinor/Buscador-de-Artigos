from google import genai
from core.config import settings

def gerar_resumo_ia(tema: str, lista_artigos: list, modelo: str = settings.DEFAULT_MODEL) -> str:
    """
    Envia os dados para o Gemini e retorna o texto cru.
    """
    if not lista_artigos:
        return "Nenhum artigo para processar."

    # Inicializa o cliente com a config centralizada
    client = genai.Client(api_key=settings.API_KEY)

    texto_contexto = f"Tema: '{tema}'.\n\nArtigos:\n"
    for i, art in enumerate(lista_artigos):
        texto_contexto += f"--- Artigo {i+1} ---\nTitulo: {art['titulo']}\nResumo: {art['resumo']}\nLink: {art['link']}\nData: {art['publicado_em']}\n"

    prompt = f"""
    {texto_contexto}
    ATUE COMO: Pesquisador Sênior.
    TAREFA: Analise os artigos. Selecione os melhores para o tema '{tema}'.
    FORMATO OBRIGATÓRIO DE SAÍDA (Para cada artigo):
    
    Titulo: [Titulo Traduzido]
    Ano: [Ano]
    Link: [Link do PDF]
    Resumo: [Resumo explicativo em PT-BR]
    Utilidade: [Por que é útil]
    Relevancia: [Nota numérica de 0 a 10]
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