import arxiv
import requests
import time

import arxiv
import requests
import time

def buscar_arxiv(tema: str, max_results: int = 3) -> list:
    # ... (Mantenha sua função buscar_arxiv atual aqui) ...
    # (O código é o mesmo do arquivo anterior, omiti para poupar espaço)
    print(f"📡 ArXiv: {tema}...")
    client = arxiv.Client()
    search = arxiv.Search(query=tema, max_results=int(max_results), sort_by=arxiv.SortCriterion.Relevance)
    results = []
    try:
        for r in client.results(search):
            results.append({
                "titulo": r.title, "resumo": r.summary.replace("\n", " "),
                "link": r.pdf_url, "data": r.published.strftime("%Y-%m-%d"), "fonte": "ArXiv"
            })
    except: pass
    return results

def buscar_semantic_scholar(tema: str, max_results: int = 3) -> list:
    # ... (Mantenha sua função buscar_semantic_scholar atual aqui) ...
    # Lembre-se de manter a lógica de correção de LINK que fizemos antes
    print(f"🌍 S2: {tema}...")
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": tema, "limit": int(max_results), "fields": "title,abstract,url,year,openAccessPdf"}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            papers = []
            if 'data' not in data: return []
            for p in data['data']:
                link = None
                if p.get('openAccessPdf'): link = p['openAccessPdf'].get('url')
                if not link: link = p.get('url')
                if not link and p.get('paperId'): link = f"https://www.semanticscholar.org/paper/{p['paperId']}"
                
                papers.append({
                    "titulo": p.get('title'), "resumo": p.get('abstract'),
                    "link": link if link else "N/D", "data": str(p.get('year', 'N/D')), "fonte": "Semantic Scholar"
                })
            return papers
    except: return []
    return []

# --- NOVA FUNÇÃO UNIFICADA (COM LISTA) ---
def buscar_unificada(lista_queries: list, max_por_fonte: int = 2) -> list:
    """Recebe LISTA de queries e remove duplicatas."""
    resultados_finais = []
    urls_vistas = set() 
    
    # Se por acaso passar uma string solta, converte para lista
    if isinstance(lista_queries, str):
        lista_queries = [lista_queries]

    for query in lista_queries:
        # Busca ArXiv
        for art in buscar_arxiv(query, max_results=max_por_fonte):
            if art['link'] not in urls_vistas:
                resultados_finais.append(art)
                urls_vistas.add(art['link'])
        
        # Busca Semantic Scholar
        for art in buscar_semantic_scholar(query, max_results=max_por_fonte):
            if art['link'] not in urls_vistas:
                resultados_finais.append(art)
                urls_vistas.add(art['link'])
                
    return resultados_finais