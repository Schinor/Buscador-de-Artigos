import streamlit as st
from core.config import settings
from core.search import buscar_artigos_arxiv
from core.ai_processor import gerar_resumo_ia
from core.parser import parsear_resposta_ia

# Config e Validação
st.set_page_config(page_title="Agente Científico Modular", layout="wide")

try:
    settings.validate()
except ValueError as e:
    st.error(f"Erro de Configuração: {e}")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    modelo = st.selectbox("Modelo", ["gemini-3.0-flash", "gemini-2.5-flash", "gemini-2.0-flash"])
    max_results = st.slider("Resultados", 1, 10, 5)

# Main
st.title("🧬 Buscador Modular")
tema = st.text_input("Tema da pesquisa:", placeholder="Digite um tema para pesquisar...")

if st.button("Pesquisar"):
    if not tema:
        st.warning("Digite um tema.")
    else:
        with st.status("Executando Agente...", expanded=True):
            st.write("📡 Buscando no ArXiv...")
            # Chama a função do módulo search
            dados = buscar_artigos_arxiv(tema, max_results)
            
            if not dados:
                st.error("Nenhum dado encontrado.")
                st.stop()
                
            st.write("🧠 Processando artigos encontrados...")
            # Chama a função do módulo ai_processor
            texto_ia = gerar_resumo_ia(tema, dados, modelo)
            
            # Chama a função do módulo parser
            resultados = parsear_resposta_ia(texto_ia)
            
        # Exibição
        for item in resultados:
            st.markdown(f"### {item['titulo']}")
            st.markdown(f"**Resumo:** {item['resumo']}")
            st.caption(f"Ano: {item['ano']} | Relevância: {item['nota']}")
            st.link_button("PDF", item['link'])
            st.divider()