# Arquivo principal do Sistema Offcon

import streamlit as st
import pandas as pd
import numpy as np
from database import Database
from config import *
from utils import *

# Importar páginas
from pages.home import render as render_home
from pages.dashboard import render as render_dashboard
from pages.containers import render as render_containers
from pages.equipment import render as render_equipment
from pages.inspections import render as render_inspections
from pages.reports import render as render_reports

# Configuração da página
st.set_page_config(**PAGE_CONFIG)

# Carregar CSS personalizado
def load_css():
    try:
        with open("styles.css", "r") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Arquivo CSS não encontrado. Usando estilo padrão.")

load_css()

# Inicializar banco de dados
@st.cache_resource
def init_database():
    return Database()

db = init_database()

# Sidebar
st.sidebar.title("🚀 Navegação")
st.sidebar.markdown("---")

# Verificar se há uma página selecionada no session state
selected_page = safe_get_session_state("selected_page")
if selected_page:
    page_index = [p["name"] for p in PAGES].index(selected_page) if selected_page in [p["name"] for p in PAGES] else 0
else:
    page_index = 0

pagina = st.sidebar.selectbox(
    "Escolha uma página:",
    options=[p["name"] for p in PAGES],
    index=page_index
)

# Limpar session state da página selecionada
if "selected_page" in st.session_state:
    del st.session_state.selected_page

# Mapeamento de páginas para funções
PAGE_RENDERERS = {
    "🏠 Início": render_home,
    "📊 Dashboard": render_dashboard,
    "� Containers": render_containers,
    "🔧 Equipamentos": render_equipment,
    "� Inspeções": render_inspections,
    "📄 Relatórios": render_reports
}

# Renderizar a página selecionada
if pagina in PAGE_RENDERERS:
    try:
        PAGE_RENDERERS[pagina]()
    except Exception as e:
        st.error(f"Erro ao carregar a página: {str(e)}")
        st.write("Por favor, recarregue a página e tente novamente.")
else:
    st.error("Página não encontrada")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; opacity: 0.7; margin-top: 2rem;">
    <p>⚡ {APP_NAME} v{APP_VERSION} | {APP_DESCRIPTION}</p>
    <p>© 2024 Offcon Systems. Todos os direitos reservados.</p>
</div>
""", unsafe_allow_html=True)
