import streamlit as st
from core.config import settings
from core.ai_processor import gerar_resumo_ia, gerar_queries_pesquisa
from core.parser import parsear_resposta_ia
from core.search import buscar_unificada


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

st.title("🧬 Buscador Científico Multi-Fontes")
st.markdown("Pesquisa integrada: **ArXiv** (Exatas/Tech) + **Semantic Scholar** (Medicina/Geral).")

tema = st.text_input("Tema da pesquisa:", placeholder="Insira o tema aqui...")

if st.button("Pesquisar"):
    if not tema:
        st.warning("Digite um tema.", placeholder="Insira a pesquisa aqui...")
    else:
        with st.status("🤖 Agente Científico Trabalhando...", expanded=True) as status:
            
            # 1. GERAÇÃO DE QUERIES
            st.write("🧠 Gerando estratégias de busca otimizadas...")
            queries_geradas = gerar_queries_pesquisa(tema, modelo)
            
            # Mostra as queries geradas para o usuário (Transparência)
            st.markdown("**Estratégias geradas:**")
            for q in queries_geradas:
                st.code(q, language="text")
            
            # 2. BUSCA MULTI-FONTE
            st.write(f"📡 Buscando artigos nas bases (ArXiv + Semantic Scholar)...")
            
            # Passamos a lista de queries agora
            dados = buscar_unificada(queries_geradas, max_por_fonte=2)
            
            if not dados:
                status.update(label="Nenhum artigo encontrado.", state="error")
                st.stop()
            
            st.write(f"🔎 Encontrados {len(dados)} artigos únicos. Lendo e analisando...")
            
            # 3. ANÁLISE FINAL
            # Passamos o tema original para a IA focar na resposta ao usuário
            texto_ia = gerar_resumo_ia(tema, dados, modelo)
            resultados = parsear_resposta_ia(texto_ia)
            
            status.update(label="Concluído!", state="complete")
            
        # Exibição
        st.subheader(f"Curadoria para: {tema}")
        for item in resultados:
            with st.container(border=True): # Borda visual bonita
                c1, c2 = st.columns([3, 1])
                c1.markdown(f"### {item['titulo']}")
                
                # Badges coloridos dependendo da fonte
                fonte_cor = "blue" if "ArXiv" in item['fonte'] else "green"
                c1.markdown(f":{fonte_cor}[{item['fonte']}] | 📅 {item['ano']}")
                
                c2.metric("Relevância", f"{item['nota']}/10")
                
                st.markdown(f"**Resumo:** {item['resumo']}")
                st.info(f"💡 {item['utilidade']}")
                st.link_button("Ler Artigo Completo", item['link'])
                st.divider()