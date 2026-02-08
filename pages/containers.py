# Página de Containers do Sistema Offcon

import streamlit as st
import pandas as pd
from database import Database
from utils import *
from config import *

def render():
    """Renderiza a página de containers"""
    db = Database()
    
    st.header("🚢 Gestão de Containers Offshore")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Adicionar Novo Container")
        codigo = st.text_input("Código do Container", placeholder="OFF1234-567")
        tipo_container = st.selectbox("Tipo de Container", CONTAINER_TYPES)
        fabricante = st.selectbox("Fabricante", EQUIPMENT_MANUFACTURERS)
        ano_fabricacao = st.number_input("Ano de Fabricação", min_value=2000, max_value=2024, value=2023)
        certificacao = st.selectbox("Certificação", CERTIFICATIONS)
        status = st.selectbox("Status", CONTAINER_STATUS)
        
        if st.button("💾 Adicionar Container"):
            if codigo and tipo_container:
                try:
                    db.adicionar_container(codigo, tipo_container, fabricante, ano_fabricacao, certificacao, status)
                    show_success_message(f"Container '{codigo}' adicionado com sucesso!")
                    st.rerun()
                except Exception as e:
                    show_error_message(f"Erro ao adicionar container: {e}")
            else:
                show_error_message("Preencha pelo menos Código e Tipo do Container.")
    
    with col2:
        st.subheader("Estatísticas")
        containers = db.listar_containers()
        
        if containers:
            df_containers = pd.DataFrame(containers, columns=['ID', 'Código', 'Tipo', 'Fabricante', 'Ano', 'Certificação', 'Status', 'Cliente_ID', 'Locação', 'Devolução', 'Criação', 'Atualização'])
            
            total = len(df_containers)
            disponiveis = len(df_containers[df_containers['Status'] == 'Disponível'])
            alugados = len(df_containers[df_containers['Status'] == 'Alugado'])
            manutencao = len(df_containers[df_containers['Status'] == 'Em Manutenção'])
            
            st.metric("Total Containers", total)
            st.metric("Disponíveis", disponiveis)
            st.metric("Alugados", alugados)
            st.metric("Em Manutenção", manutencao)
            
            # Gráfico por status
            st.markdown("**Containers por Status:**")
            status_counts = df_containers['Status'].value_counts()
            st.bar_chart(status_counts)
        else:
            show_info_message("Nenhum container cadastrado.")
    
    # Tabela completa de containers
    st.markdown("---")
    st.subheader("📋 Todos os Containers")
    containers = db.listar_containers()
    
    if containers:
        df_containers = pd.DataFrame(containers, columns=['ID', 'Código', 'Tipo', 'Fabricante', 'Ano', 'Certificação', 'Status', 'Cliente_ID', 'Locação', 'Devolução', 'Criação', 'Atualização'])
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            filtro_tipo = st.selectbox("Filtrar por Tipo", ["Todos"] + list(df_containers['Tipo'].unique()))
        with col2:
            filtro_fabricante = st.selectbox("Filtrar por Fabricante", ["Todos"] + list(df_containers['Fabricante'].unique()))
        with col3:
            filtro_status = st.selectbox("Filtrar por Status", ["Todos"] + list(df_containers['Status'].unique()))
        
        # Aplicar filtros
        filters = {}
        if filtro_tipo != "Todos":
            filters['Tipo'] = filtro_tipo
        if filtro_fabricante != "Todos":
            filters['Fabricante'] = filtro_fabricante
        if filtro_status != "Todos":
            filters['Status'] = filtro_status
        
        df_filtrada = filter_dataframe(df_containers, filters)
        st.dataframe(df_filtrada[['ID', 'Código', 'Tipo', 'Fabricante', 'Ano', 'Certificação', 'Status']], width='stretch')
        
        # Botão para popular dados aleatórios
        st.markdown("---")
        if st.button("🎲 Popular com Dados Aleatórios (20 containers)"):
            db.popular_dados_aleatorios(20)
            show_success_message("20 containers aleatórios adicionados!")
            st.rerun()
    else:
        show_info_message("Nenhum container cadastrado. Clique no botão abaixo para adicionar dados de exemplo.")
        if st.button("🎲 Gerar Dados de Exemplo"):
            db.popular_dados_aleatorios(20)
            show_success_message("20 containers aleatórios criados!")
            st.rerun()
