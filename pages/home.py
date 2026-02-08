# Página Inicial do Sistema Offcon

import streamlit as st
import pandas as pd
from database import Database
from utils import *
from config import *

def render():
    """Renderiza a página inicial"""
    db = Database()
    
    # Header principal
    st.markdown(f"""
    <div class="header-container">
        <h1 style="font-size: 3rem; margin-bottom: 1rem;">⚡ {APP_NAME}</h1>
        <p style="font-size: 1.5rem; margin-bottom: 2rem; opacity: 0.9;">
            {APP_DESCRIPTION}
        </p>
        <p style="font-size: 1.1rem; max-width: 600px; margin: 0 auto; opacity: 0.8;">
            Monitore, analise e otimize o consumo de energia com nossa solução completa 
            para gestão de projetos e equipamentos off-grid.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estatísticas principais
    projetos = db.listar_projetos()
    medicoes = db.listar_medicoes()
    equipamentos = db.listar_equipamentos()
    relatorios = db.listar_relatorios()
    
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_stat_card(len(projetos), "Projetos Ativos"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_stat_card(len(equipamentos), "Equipamentos", 
                                   "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_stat_card(len(medicoes), "Medições", 
                                   "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_stat_card(len(relatorios), "Relatórios", 
                                   "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recursos principais
    st.markdown('<h2 style="text-align: center; margin-bottom: 3rem;">🚀 Recursos Principais</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(create_feature_card(
            "�", "Gestão de Containers",
            "Controle completo da frota de containers offshore com certificação DNV 2.7.1/2.7.3 e rastreamento de status em tempo real."
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_feature_card(
            "🔧", "Manutenção e Reparos",
            "Gerencie manutenções preventivas e corretivas com histórico completo e controle de custos operacionais."
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_feature_card(
            "�", "Inspeções DNV",
            "Agendamento e controle de inspeções periódicas DNV com emissão de certificados e conformidade IMO."
        ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Ações rápidas
    st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">⚡ Ações Rápidas</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚢 Novo Container", type="secondary"):
            safe_set_session_state("selected_page", "� Containers")
            st.rerun()
    
    with col2:
        if st.button("📋 Agendar Inspeção", type="secondary"):
            safe_set_session_state("selected_page", "� Inspeções")
            st.rerun()
    
    with col3:
        if st.button("📊 Gerar Relatório", type="secondary"):
            safe_set_session_state("selected_page", "📄 Relatórios")
            st.rerun()
    
    with col4:
        if st.button("📈 Ver Dashboard", type="secondary"):
            safe_set_session_state("selected_page", "� Dashboard")
            st.rerun()
    
    # Footer
    st.markdown(f"""
    <div class="footer">
        <h3>⚡ {APP_NAME}</h3>
        <p>{APP_DESCRIPTION}</p>
        <p style="opacity: 0.7; margin-top: 1rem;">
            © 2024 Offcon Systems. Todos os direitos reservados.
        </p>
    </div>
    """, unsafe_allow_html=True)
