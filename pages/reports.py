# Página de Relatórios do Sistema Offcon

import streamlit as st
import pandas as pd
from database import Database
from utils import *
from config import *

def render():
    """Renderiza a página de relatórios"""
    db = Database()
    
    st.header("📄 Relatórios")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Gerar Novo Relatório")
        
        projetos = db.listar_projetos()
        if projetos:
            projeto_options = {f"{p[1]} (ID: {p[0]})": p[0] for p in projetos}
            projeto_selecionado = st.selectbox("Selecione o Projeto", list(projeto_options.keys()))
            
            tipo_relatorio = st.selectbox("Tipo de Relatório", REPORT_TYPES)
            
            data_inicio = st.date_input("Data de Início")
            data_fim = st.date_input("Data de Fim")
            
            if st.button("📊 Gerar Relatório"):
                projeto_id = projeto_options[projeto_selecionado]
                
                # Gerar conteúdo do relatório
                medicoes_filtradas = db.listar_medicoes(projeto_id)
                df_medicoes = pd.DataFrame(medicoes_filtradas, columns=['ID', 'Projeto_ID', 'Tipo', 'Valor', 'Unidade', 'Data', 'Projeto_Nome'])
                
                if not df_medicoes.empty:
                    # Estatísticas
                    total_medicoes = len(df_medicoes)
                    valor_medio = df_medicoes['Valor'].mean()
                    valor_max = df_medioes['Valor'].max()
                    valor_min = df_medioes['Valor'].min()
                    
                    conteudo_relatorio = f"""
                    RELATÓRIO: {tipo_relatorio}
                    Projeto: {projeto_selecionado}
                    Período: {data_inicio} a {data_fim}
                    
                    ESTATÍSTICAS:
                    - Total de Medições: {total_medicoes}
                    - Valor Médio: {valor_medio:.2f}
                    - Valor Máximo: {valor_max:.2f}
                    - Valor Mínimo: {valor_min:.2f}
                    
                    DETALHES:
                    {df_medicoes.to_string()}
                    """
                    
                    relatorio_id = db.gerar_relatorio(projeto_id, tipo_relatorio, conteudo_relatorio)
                    show_success_message(f"Relatório gerado com ID: {relatorio_id}")
                    st.rerun()
                else:
                    show_warning_message("Nenhuma medição encontrada para este projeto no período selecionado.")
        else:
            show_info_message("Nenhum projeto cadastrado. Crie um projeto primeiro.")
    
    with col2:
        st.subheader("📋 Relatórios Salvos")
        relatorios = db.listar_relatorios()
        
        if relatorios:
            for relatorio in relatorios[:5]:  # Mostrar apenas 5 mais recentes
                with st.expander(f"{relatorio[2]} - {relatorio[4][:10]}"):
                    st.text(relatorio[3])
                    st.caption(f"Projeto: {relatorio[5]}")
        else:
            show_info_message("Nenhum relatório gerado ainda.")
    
    # Lista completa de relatórios
    st.markdown("---")
    st.subheader("📄 Todos os Relatórios")
    relatorios = db.listar_relatorios()
    
    if relatorios:
        df_relatorios = pd.DataFrame(relatorios, columns=['ID', 'Projeto_ID', 'Tipo', 'Conteúdo', 'Data', 'Projeto_Nome'])
        st.dataframe(df_relatorios[['ID', 'Projeto_Nome', 'Tipo', 'Data']], width='stretch')
        
        # Opção de download
        if st.button("📥 Exportar Relatórios (CSV)"):
            create_download_button(df_relatorios, 'relatorios_export.csv', 'Exportar Relatórios')
    else:
        show_info_message("Nenhum relatório encontrado.")
