# Página de Projetos do Sistema Offcon

import streamlit as st
import pandas as pd
from database import Database
from utils import *
from config import *

def render():
    """Renderiza a página de projetos"""
    db = Database()
    
    st.header("📁 Gestão de Projetos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Adicionar Novo Projeto")
        nome_projeto = st.text_input("Nome do Projeto")
        desc_projeto = st.text_area("Descrição")
        
        if st.button("💾 Criar Projeto"):
            if nome_projeto:
                projeto_id = db.adicionar_projeto(nome_projeto, desc_projeto)
                show_success_message(f"Projeto '{nome_projeto}' criado com ID: {projeto_id}")
                st.rerun()
            else:
                show_error_message("Por favor, informe o nome do projeto.")
    
    with col2:
        st.subheader("Adicionar Medição")
        projetos = db.listar_projetos()
        if projetos:
            projeto_options = {f"{p[1]} (ID: {p[0]})": p[0] for p in projetos}
            projeto_selecionado = st.selectbox("Selecione o Projeto", list(projeto_options.keys()))
            
            tipo_medicao = st.selectbox("Tipo de Medição", MEASUREMENT_TYPES)
            valor_medicao = st.number_input("Valor", value=0.0)
            unidade_medicao = st.text_input("Unidade", placeholder="kWh, °C, bar, etc.")
            
            if st.button("📊 Adicionar Medição"):
                projeto_id = projeto_options[projeto_selecionado]
                db.adicionar_medicao(projeto_id, tipo_medicao, valor_medicao, unidade_medicao)
                show_success_message("Medição adicionada com sucesso!")
                st.rerun()
        else:
            show_info_message("Cadastre um projeto primeiro para adicionar medições.")
    
    # Lista de projetos
    st.markdown("---")
    st.subheader("📋 Todos os Projetos")
    projetos = db.listar_projetos()
    if projetos:
        df_projetos = pd.DataFrame(projetos, columns=['ID', 'Nome', 'Descrição', 'Status', 'Criação', 'Atualização'])
        st.dataframe(df_projetos, width='stretch')
    else:
        show_info_message("Nenhum projeto cadastrado.")
