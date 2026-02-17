import streamlit as st
from core.config import settings
from core.ai_processor import gerar_resumo_ia, gerar_queries_pesquisa
from core.parser import parsear_resposta_ia
from core.search import buscar_unificada

# Configuração
st.set_page_config(page_title="Agente Científico Pro", layout="wide", page_icon="🧬")

try:
    settings.validate()
except ValueError as e:
    st.error(f"Erro: {e}")
    st.stop()

# --- FUNÇÃO DE UI PARA RENDERIZAR O CARD ---
def renderizar_cartao(item):
    """Renderiza um único artigo de forma visual."""
    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"### {item['titulo']}")
        
        fonte_cor = "blue" if "ArXiv" in item['fonte'] else "green"
        c1.markdown(f":{fonte_cor}[{item['fonte']}] | 📅 {item['ano']}")
        
        # Cor da nota
        nota = item['nota']
        cor_nota = "green" if nota > 7 else "orange"
        c2.markdown(f"Relevância: :{cor_nota}[**{nota}/10**]")
        
        st.markdown(f"**Resumo:** {item['resumo']}")
        st.info(f"💡 {item['utilidade']}")
        
        if item['link'] and item['link'].startswith("http"):
            st.link_button("📄 Ler PDF Completo", item['link'])
        else:
            st.button("🚫 PDF Indisponível", disabled=True, key=item['link']+item['titulo']) # Key única para evitar erro

# --- INTERFACE ---
with st.sidebar:
    st.header("⚙️ Configurações")
    modelo = st.selectbox("Modelo IA", ["gemini-3.0-flash", "gemini-2.5-flash", "gemini-2.0-flash"])
    max_results = st.slider("Resultados por Query", 1, 5, 2)

st.title("🧬 Buscador Científico Inteligente")
st.markdown("Geração de Queries + Busca Multi-Fonte + Análise de Relevância.")

tema = st.text_input("Tema da pesquisa:", placeholder="Ex: Machine Learning no Agronegócio")

if st.button("Pesquisar", type="primary"):
    if not tema:
        st.warning("Digite um tema.")
    else:
        with st.status("🔍 Executando agente de pesquisa...", expanded=True) as status:
            
            # 1. Gerar Queries
            st.write("🧠 Criando estratégias de busca...")
            queries = gerar_queries_pesquisa(tema, modelo)
            
            # Mostra as queries geradas num expander fechado para não poluir
            with st.expander("Ver estratégias de busca geradas"):
                st.write(queries)
            
            # 2. Busca
            st.write(f"📡 Consultando bases para {len(queries)} variações...")
            dados = buscar_unificada(queries, max_por_fonte=max_results)
            
            if not dados:
                status.update(label="Nada encontrado.", state="error")
                st.stop()
            
            st.write(f"🔎 Analisando {len(dados)} artigos...")
            
            # 3. Processamento IA
            texto_ia = gerar_resumo_ia(tema, dados, modelo)
            resultados = parsear_resposta_ia(texto_ia)
            
            status.update(label="Concluído!", state="complete")
            
        # --- SEPARAÇÃO DE RELEVÂNCIA ---
        alta_relevancia = [r for r in resultados if r['nota'] > 7]
        baixa_relevancia = [r for r in resultados if r['nota'] <= 7]

        # Exibe os TOP (Alta Relevância)
        if alta_relevancia:
            st.subheader("🔥 Artigos Altamente Relevantes")
            for item in alta_relevancia:
                renderizar_cartao(item)
        else:
            st.warning("Nenhum artigo de alta relevância (>7) encontrado.")

        # Exibe os OUTROS (Baixa Relevância) em um Expander
        if baixa_relevancia:
            st.markdown("---")
            with st.expander(f"📚 Ver outros {len(baixa_relevancia)} artigos relacionados (Menor Relevância)"):
                st.caption("Estes artigos podem ser úteis para contexto, mas têm menor conexão direta com o tema principal.")
                for item in baixa_relevancia:
                    renderizar_cartao(item)