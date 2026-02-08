# Página Dashboard do Sistema Offcon

import streamlit as st
import pandas as pd
from database import Database
from utils import *
from config import *

def render():
    """Renderiza a página de dashboard"""
    db = Database()
    
    st.header("📊 Dashboard")
    
    # Obter dados reais do banco
    projetos = db.listar_projetos()
    medicoes = db.listar_medicoes()
    equipamentos = db.listar_equipamentos()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Projetos", len(projetos))
    
    with col2:
        st.metric("Total de Medições", len(medicoes))
    
    with col3:
        projetos_ativos = len([p for p in projetos if p[3] == 'ativo'])
        st.metric("Projetos Ativos", projetos_ativos)
    
    with col4:
        equipamentos_ativos = len([e for e in equipamentos if e[5] == 'ativo'])
        st.metric("Equipamentos Ativos", equipamentos_ativos)
    
    st.markdown("---")
    
    # Tabela de projetos recentes
    st.subheader("📁 Projetos Recentes")
    if projetos:
        df_projetos = pd.DataFrame(projetos, columns=['ID', 'Nome', 'Descrição', 'Status', 'Criação', 'Atualização'])
        st.dataframe(df_projetos[['ID', 'Nome', 'Status', 'Criação']].head(5), width='stretch')
    else:
        st.info("Nenhum projeto cadastrado ainda.")
    
    # Tabela de equipamentos recentes
    st.subheader("🔧 Equipamentos Recentes")
    if equipamentos:
        df_equipamentos = pd.DataFrame(equipamentos, columns=['Serial', 'Modelo', 'Fabricante', 'Categoria', 'Instalação', 'Status'])
        st.dataframe(df_equipamentos[['Serial', 'Modelo', 'Fabricante', 'Status']].head(5), width='stretch')
    else:
        st.info("Nenhum equipamento cadastrado.")
    
    # Gráfico de medições recentes
    if medicoes:
        st.subheader("📈 Medições Recentes")
        df_medicoes = pd.DataFrame(medicoes, columns=['ID', 'Projeto_ID', 'Tipo', 'Valor', 'Unidade', 'Data', 'Projeto_Nome'])
        
        # Agrupar por tipo de medição
        medicoes_por_tipo = df_medicoes.groupby('Tipo')['Valor'].sum().reset_index()
        st.bar_chart(medicoes_por_tipo.set_index('Tipo'))
