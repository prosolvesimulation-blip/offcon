# Página de Inspeções do Sistema Offcon

import streamlit as st
import pandas as pd
from database import Database
from utils import *
from config import *
from datetime import datetime, timedelta

def render():
    """Renderiza a página de inspeções"""
    db = Database()
    
    st.header("📋 Gestão de Inspeções DNV")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Agendar Nova Inspeção")
        
        containers = db.listar_containers()
        if containers:
            container_options = {f"{c[1]} ({c[2]})": c[0] for c in containers}
            container_selecionado = st.selectbox("Selecione o Container", list(container_options.keys()))
            
            tipo_inspecao = st.selectbox("Tipo de Inspeção", INSPECTION_TYPES)
            inspetor = st.text_input("Inspetor Responsável", placeholder="Nome do inspetor DNV")
            observacoes = st.text_area("Observações")
            
            if st.button("📋 Agendar Inspeção"):
                container_id = container_options[container_selecionado]
                proxima_inspecao = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
                
                inspecao_id = db.adicionar_inspecao(
                    container_id, tipo_inspecao, "Agendada", proxima_inspecao, inspetor, "", observacoes
                )
                show_success_message(f"Inspeção agendada com ID: {inspecao_id}")
                st.rerun()
        else:
            show_info_message("Nenhum container cadastrado. Cadastre containers primeiro.")
    
    with col2:
        st.subheader("Estatísticas de Inspeções")
        inspecoes = db.listar_inspecoes()
        
        if inspecoes:
            df_inspecoes = pd.DataFrame(inspecoes, columns=[
                'ID', 'Container_ID', 'Tipo', 'Data', 'Resultado', 'Próxima', 'Inspetor', 'Certificado', 'Observações', 'Container_Código'
            ])
            
            total = len(df_inspecoes)
            agendadas = len(df_inspecoes[df_inspecoes['Resultado'] == 'Agendada'])
            aprovadas = len(df_inspecoes[df_inspecoes['Resultado'] == 'Aprovada'])
            reprovadas = len(df_inspecoes[df_inspecoes['Resultado'] == 'Reprovada'])
            
            st.metric("Total Inspeções", total)
            st.metric("Agendadas", agendadas)
            st.metric("Aprovadas", aprovadas)
            st.metric("Reprovadas", reprovadas)
            
            # Gráfico por tipo
            st.markdown("**Inspeções por Tipo:**")
            tipo_counts = df_inspecoes['Tipo'].value_counts()
            st.bar_chart(tipo_counts)
        else:
            show_info_message("Nenhuma inspeção cadastrada.")
    
    # Lista de inspeções
    st.markdown("---")
    st.subheader("📋 Histórico de Inspeções")
    inspecoes = db.listar_inspecoes()
    
    if inspecoes:
        df_inspecoes = pd.DataFrame(inspecoes, columns=[
            'ID', 'Container_ID', 'Tipo', 'Data', 'Resultado', 'Próxima', 'Inspetor', 'Certificado', 'Observações', 'Container_Código'
        ])
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            filtro_tipo = st.selectbox("Filtrar por Tipo", ["Todos"] + list(df_inspecoes['Tipo'].unique()))
        with col2:
            filtro_resultado = st.selectbox("Filtrar por Resultado", ["Todos"] + list(df_inspecoes['Resultado'].unique()))
        
        # Aplicar filtros
        filters = {}
        if filtro_tipo != "Todos":
            filters['Tipo'] = filtro_tipo
        if filtro_resultado != "Todos":
            filters['Resultado'] = filtro_resultado
        
        df_filtrada = filter_dataframe(df_inspecoes, filters)
        
        # Formatar datas para exibição
        df_filtrada['Data'] = pd.to_datetime(df_filtrada['Data']).dt.strftime('%d/%m/%Y')
        if 'Próxima' in df_filtrada.columns:
            df_filtrada['Próxima'] = pd.to_datetime(df_filtrada['Próxima'], errors='coerce').dt.strftime('%d/%m/%Y')
        
        st.dataframe(df_filtrada[['ID', 'Container_Código', 'Tipo', 'Data', 'Resultado', 'Próxima', 'Inspetor']], width='stretch')
        
        # Opção de download
        st.markdown("---")
        if st.button("📥 Exportar Inspeções (CSV)"):
            create_download_button(df_filtrada, 'inspecoes_export.csv', 'Exportar Inspeções')
    else:
        show_info_message("Nenhuma inspeção encontrada.")
    
    # Inspeções próximas
    st.markdown("---")
    st.subheader("⏰ Inspeções Próximas")
    
    if inspecoes:
        df_inspecoes['Data'] = pd.to_datetime(df_inspecoes['Data'])
        df_inspecoes['Próxima'] = pd.to_datetime(df_inspecoes['Próxima'], errors='coerce')
        
        # Filtrar inspeções próximas (próximos 30 dias)
        hoje = datetime.now()
        proximas = df_inspecoes[
            (df_inspecoes['Próxima'] >= hoje) & 
            (df_inspecoes['Próxima'] <= hoje + timedelta(days=30))
        ].sort_values('Próxima')
        
        if not proximas.empty:
            proximas['Próxima'] = proximas['Próxima'].dt.strftime('%d/%m/%Y')
            st.dataframe(proximas[['Container_Código', 'Tipo', 'Próxima', 'Inspetor']], width='stretch')
        else:
            show_info_message("Nenhuma inspeção agendada para os próximos 30 dias.")
