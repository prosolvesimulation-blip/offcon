# Página de Análises do Sistema Offcon

import streamlit as st
import pandas as pd
from database import Database
from utils import *
from config import *

def render():
    """Renderiza a página de análises"""
    db = Database()
    
    st.header("🔍 Análises de Dados")
    
    # Análise de medições
    st.subheader("📊 Análise de Medições")
    medicoes = db.listar_medicoes()
    
    if medicoes:
        df_medicoes = pd.DataFrame(medicoes, columns=['ID', 'Projeto_ID', 'Tipo', 'Valor', 'Unidade', 'Data', 'Projeto_Nome'])
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            tipos_disponiveis = df_medicoes['Tipo'].unique()
            tipo_filtro = st.selectbox("Filtrar por Tipo", ["Todos"] + list(tipos_disponiveis))
        
        with col2:
            projetos_disponiveis = df_medicoes['Projeto_Nome'].unique()
            projeto_filtro = st.selectbox("Filtrar por Projeto", ["Todos"] + list(projetos_disponiveis))
        
        # Aplicar filtros
        filters = {}
        if tipo_filtro != "Todos":
            filters['Tipo'] = tipo_filtro
        if projeto_filtro != "Todos":
            filters['Projeto_Nome'] = projeto_filtro
        
        df_filtrada = filter_dataframe(df_medicoes, filters)
        
        # Estatísticas
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Medições", len(df_filtrada))
        with col2:
            st.metric("Valor Médio", f"{df_filtrada['Valor'].mean():.2f}")
        with col3:
            st.metric("Valor Máximo", f"{df_filtrada['Valor'].max():.2f}")
        
        # Gráficos
        st.markdown("---")
        st.subheader("📈 Visualizações")
        
        # Gráfico de linha por tempo
        df_filtrada['Data'] = pd.to_datetime(df_filtrada['Data'])
        df_timeline = df_filtrada.groupby('Data')['Valor'].mean().reset_index()
        st.line_chart(df_timeline.set_index('Data'))
        
        # Gráfico de barras por tipo
        df_tipo = create_chart_data(df_filtrada, 'Tipo', 'Valor', 'sum')
        st.bar_chart(df_tipo.set_index('Tipo'))
        
        # Tabela detalhada
        st.markdown("---")
        st.subheader("📋 Dados Detalhados")
        st.dataframe(df_filtrada[['Data', 'Projeto_Nome', 'Tipo', 'Valor', 'Unidade']], width='stretch')
    else:
        show_info_message("Nenhuma medição encontrada. Cadastre projetos e medições primeiro.")
    
    # Upload de arquivos
    st.markdown("---")
    st.subheader("📁 Importar Dados")
    uploaded_file = st.file_uploader("Carregue um arquivo CSV para importar medições", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df_import = pd.read_csv(uploaded_file)
            show_success_message(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")
            st.dataframe(df_import.head())
            
            if st.button("📥 Importar Medições"):
                show_info_message("Funcionalidade de importação em desenvolvimento.")
        except Exception as e:
            show_error_message(f"Erro ao ler o arquivo: {e}")
