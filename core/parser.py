import re

def parsear_resposta_ia(texto_resposta: str) -> list:
    artigos_processados = []
    if not texto_resposta:
        return []

    blocos = texto_resposta.split("---")
    
    for bloco in blocos:
        if "Titulo:" not in bloco: continue
        
        try:
            artigo = {}
            # Regex com tratamento de erro mais suave (.get)
            artigo['titulo'] = _extrair(r'Titulo: (.*)', bloco)
            artigo['fonte'] = _extrair(r'Fonte: (.*)', bloco) # Novo campo
            artigo['ano'] = _extrair(r'Ano: (.*)', bloco)
            artigo['link'] = _extrair(r'Link: (.*)', bloco)
            artigo['resumo'] = _extrair(r'Resumo: (.*)', bloco)
            artigo['utilidade'] = _extrair(r'Utilidade: (.*)', bloco)
            
            match_nota = re.search(r'Relevancia:.*?(\d+)', bloco)
            artigo['nota'] = int(match_nota.group(1)) if match_nota else 0
            
            artigos_processados.append(artigo)
        except Exception:
            continue
            
    return artigos_processados

def _extrair(regex, texto):
    """Função auxiliar para deixar o código limpo"""
    match = re.search(regex, texto)
    return match.group(1).strip() if match else "N/D"