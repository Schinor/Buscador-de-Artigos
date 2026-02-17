import arxiv
import requests
import time

def buscar_arxiv(tema: str, max_results: int = 3) -> list:
    """Busca especializada em Exatas/Computação"""
    print(f"📡 Consultando ArXiv para: {tema}...")
    client = arxiv.Client()
    search = arxiv.Search(
        query=tema,
        max_results=int(max_results),
        sort_by=arxiv.SortCriterion.Relevance,
    )
    results = []
    try:
        for r in client.results(search):
            results.append({
                "titulo": r.title,
                "resumo": r.summary.replace("\n", " "), # Limpa quebras de linha
                "link": r.pdf_url,
                "data": r.published.strftime("%Y-%m-%d"),
                "fonte": "ArXiv"
            })
    except Exception:
        pass # Se falhar, apenas retorna lista vazia
    return results

def buscar_semantic_scholar(tema: str, max_results: int = 3) -> list:
    """
    Busca generalista (Medicina, Biologia, Humanas).
    A API é gratuita para baixo volume.
    """
    print(f"🌍 Consultando Semantic Scholar para: {tema}...")
    
    # Endpoint de busca por relevância
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    params = {
        "query": tema,
        "limit": int(max_results),
        # Pedimos campos específicos para não vir lixo
        "fields": "title,abstract,url,year,openAccessPdf"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            papers = []
            
            if 'data' not in data:
                return []

            for p in data['data']:
                link = None
        
            # 1. Tenta pegar o PDF aberto direto
            if p.get('openAccessPdf'):
                link = p['openAccessPdf'].get('url')
            
            # 2. Se não tiver, pega a URL oficial do paper
            if not link:
                link = p.get('url')
                
            # 3. Se ainda não tiver, tenta montar o link do Semantic Scholar
            if not link and p.get('paperId'):
                link = f"https://www.semanticscholar.org/paper/{p['paperId']}"

            papers.append({
                "titulo": p.get('title'),
                "resumo": p.get('abstract'),
                "link": link if link else "N/D", # Garante que vai algo
                "data": str(p.get('year', 'N/D')),
                "fonte": "Semantic Scholar"
            })
            return papers
    except Exception as e:
        print(f"Erro no S2: {e}")
        return []
    return []

def buscar_unificada(tema: str, max_por_fonte: int = 3) -> list:
    """
    O Orquestrador: Chama todo mundo e mistura os resultados.
    """
    resultados_finais = []
    
    # 1. Busca no ArXiv (Melhor para Tech/IA/Física)
    resultados_finais.extend(buscar_arxiv(tema, max_por_fonte))
    
    # 2. Busca no Semantic Scholar (Melhor para Medicina/Geral)
    # Dica: Às vezes o S2 retorna coisas do ArXiv também, então duplicatas podem ocorrer
    resultados_finais.extend(buscar_semantic_scholar(tema, max_por_fonte))
    
    return resultados_finais