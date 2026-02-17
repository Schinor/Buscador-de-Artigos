import arxiv

def buscar_artigos_arxiv(tema: str, max_resultados: int = 5) -> list:
    """
    Busca metadados brutos no ArXiv.
    Retorna uma lista de dicionários.
    """
    client = arxiv.Client()
    
    search = arxiv.Search(
        query=tema,
        max_results=int(max_resultados),
        sort_by=arxiv.SortCriterion.Relevance,
    )

    resultados = []
    try:
        # O generator do arxiv só é consumido aqui
        for result in client.results(search):
            resultados.append({
                "titulo": result.title,
                "resumo": result.summary,
                "link": result.pdf_url,
                "publicado_em": result.published.strftime("%Y-%m-%d")
            })
    except Exception as e:
        # Em produção, você usaria logging aqui, não print
        print(f"Erro na conexão com ArXiv: {e}")
        return []
        
    return resultados