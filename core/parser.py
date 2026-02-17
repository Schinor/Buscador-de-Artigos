import re

def parsear_resposta_ia(texto_resposta: str) -> list:
    """
    Converte o texto formatado da IA em uma lista de objetos estruturados.
    """
    artigos_processados = []
    if not texto_resposta:
        return []

    blocos = texto_resposta.split("---")
    
    for bloco in blocos:
        if "Titulo:" not in bloco: continue
        
        try:
            artigo = {}
            # Regex robusto para capturar conteúdo após os rótulos
            artigo['titulo'] = re.search(r'Titulo: (.*)', bloco).group(1).strip()
            
            # Tratamento de erro específico para Ano
            match_ano = re.search(r'Ano: (.*)', bloco)
            artigo['ano'] = match_ano.group(1).strip() if match_ano else "N/D"
            
            artigo['link'] = re.search(r'Link: (.*)', bloco).group(1).strip()
            artigo['resumo'] = re.search(r'Resumo: (.*)', bloco).group(1).strip()
            artigo['utilidade'] = re.search(r'Utilidade: (.*)', bloco).group(1).strip()
            
            match_nota = re.search(r'Relevancia:.*?(\d+)', bloco)
            artigo['nota'] = int(match_nota.group(1)) if match_nota else 0
            
            artigos_processados.append(artigo)
        except AttributeError:
            # Se o regex falhar em um campo, pula o artigo ou loga o erro
            continue
            
    return artigos_processados