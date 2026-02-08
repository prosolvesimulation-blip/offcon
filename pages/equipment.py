# Página de Equipamentos do Sistema Offcon

import streamlit as st
import pandas as pd
import plotly.express as px
from database import Database
from utils import *
from config import *

def render():
    """Renderiza a página de equipamentos"""
    db = Database()

    st.header("🔧 Gestão de Equipamentos")

    # Abas para organização
    tab1, tab2 = st.tabs(["📊 Dashboard", "📝 Cadastro"])

    with tab1:
        # Dashboard com métricas e gráficos
        st.subheader("📈 Dashboard de Equipamentos")
        
        # Métricas principais
        equipamentos = db.listar_equipamentos()
        
        if equipamentos:
            df_equip = pd.DataFrame(equipamentos, columns=['Serial', 'Modelo', 'Fabricante', 'Categoria', 'Instalação', 'Status'])
            
            # Converter data de instalação para datetime
            df_equip['Instalação'] = pd.to_datetime(df_equip['Instalação'])
            
            # Métricas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total = len(df_equip)
                st.metric("Total Equipamentos", total)
                
            with col2:
                ativos = len(df_equip[df_equip['Status'] == 'ativo'])
                st.metric("Ativos", ativos)
                
            with col3:
                inativos = len(df_equip[df_equip['Status'] == 'inativo'])
                st.metric("Inativos", inativos)
                
            with col4:
                taxa_ativacao = f"{(ativos/total*100):.1f}%" if total > 0 else "0%"
                st.metric("Taxa de Ativação", taxa_ativacao)
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico por status
                st.markdown("**Distribuição por Status:**")
                status_counts = df_equip['Status'].value_counts()
                fig_status = px.pie(values=status_counts.values, names=status_counts.index, title="Status dos Equipamentos")
                st.plotly_chart(fig_status, width='stretch')
                
            with col2:
                # Gráfico por categoria
                st.markdown("**Distribuição por Categoria:**")
                categoria_counts = df_equip['Categoria'].value_counts()
                fig_categoria = px.bar(x=categoria_counts.index, y=categoria_counts.values, 
                                      title="Equipamentos por Categoria", 
                                      labels={'x': 'Categoria', 'y': 'Quantidade'})
                st.plotly_chart(fig_categoria, width='stretch')
            
            # Gráfico de evolução temporal
            st.markdown("**Evolução de Cadastro de Equipamentos ao Longo do Tempo:**")
            df_temporal = df_equip.groupby(df_equip['Instalação'].dt.date).size().reset_index(name='Quantidade')
            fig_temporal = px.line(df_temporal, x='Instalação', y='Quantidade', 
                                  title="Novos Equipamentos por Data",
                                  labels={'Instalação': 'Data', 'Quantidade': 'Número de Equipamentos'})
            st.plotly_chart(fig_temporal, width='stretch')
            
        else:
            show_info_message("Nenhum equipamento cadastrado.")

    with tab2:
        # Seção de cadastro
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Adicionar Novo Equipamento")
            serial = st.text_input("Serial (único)", placeholder="OFF123456789")
            modelo = st.text_input("Modelo")
            fabricante = st.text_input("Fabricante")
            categoria = st.selectbox("Categoria", EQUIPMENT_CATEGORIES + ["Outro"])
            status = st.selectbox("Status", ["ativo", "inativo"])

            if st.button("💾 Adicionar Equipamento"):
                if serial and modelo:
                    try:
                        db.adicionar_equipamento(serial, modelo, fabricante, categoria, status)
                        show_success_message(f"Equipamento '{modelo}' adicionado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        show_error_message(f"Erro ao adicionar equipamento: {e}")
                else:
                    show_error_message("Preencha pelo menos Serial e Modelo.")

        with col2:
            st.subheader("Estatísticas")
            equipamentos = db.listar_equipamentos()

            if equipamentos:
                df_equip = pd.DataFrame(equipamentos, columns=['Serial', 'Modelo', 'Fabricante', 'Categoria', 'Instalação', 'Status'])

                total = len(df_equip)
                ativos = len(df_equip[df_equip['Status'] == 'ativo'])

                st.metric("Total Equipamentos", total)
                st.metric("Equipamentos Ativos", ativos)
                st.metric("Taxa de Ativação", f"{(ativos/total*100):.1f}%" if total > 0 else "0%")

                # Gráfico por categoria
                st.markdown("**Equipamentos por Categoria:**")
                categoria_counts = df_equip['Categoria'].value_counts()
                st.bar_chart(categoria_counts)
            else:
                show_info_message("Nenhum equipamento cadastrado.")

        # Tabela completa de equipamentos
        st.markdown("---")
        st.subheader("📋 Todos os Equipamentos")
        equipamentos = db.listar_equipamentos()

        if equipamentos:
            df_equipamentos = pd.DataFrame(equipamentos, columns=['Serial', 'Modelo', 'Fabricante', 'Categoria', 'Instalação', 'Status'])

            # Filtros
            col1, col2, col3 = st.columns(3)
            with col1:
                filtro_fabricante = st.selectbox("Filtrar por Fabricante", ["Todos"] + list(df_equipamentos['Fabricante'].unique()), key="filtro_fab_eq")
            with col2:
                filtro_categoria = st.selectbox("Filtrar por Categoria", ["Todos"] + list(df_equipamentos['Categoria'].unique()), key="filtro_cat_eq")
            with col3:
                filtro_status = st.selectbox("Filtrar por Status", ["Todos"] + list(df_equipamentos['Status'].unique()), key="filtro_status_eq")

            # Aplicar filtros
            filters = {}
            if filtro_fabricante != "Todos":
                filters['Fabricante'] = filtro_fabricante
            if filtro_categoria != "Todos":
                filters['Categoria'] = filtro_categoria
            if filtro_status != "Todos":
                filters['Status'] = filtro_status

            df_filtrada = filter_dataframe(df_equipamentos, filters)
            
            # Adicionar coluna de ações
            if not df_filtrada.empty:
                st.markdown("**Tabela de Equipamentos com Ações:**")
                
                # Mostrar tabela com botões de deletar
                for index, row in df_filtrada.iterrows():
                    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 2, 2, 1, 1])
                    
                    with col1:
                        st.write(row['Serial'])
                    with col2:
                        st.write(row['Modelo'])
                    with col3:
                        st.write(row['Fabricante'])
                    with col4:
                        st.write(row['Categoria'])
                    with col5:
                        st.write(row['Instalação'])
                    with col6:
                        st.write(row['Status'])
                    with col7:
                        if st.button("🗑️", key=f"delete_{row['Serial']}", help="Deletar Equipamento"):
                            if st.session_state.get(f'confirm_delete_{row["Serial"]}', False):
                                try:
                                    db.deletar_equipamento(row['Serial'])
                                    show_success_message(f"Equipamento '{row['Serial']}' deletado com sucesso!")
                                    st.rerun()
                                except Exception as e:
                                    show_error_message(f"Erro ao deletar equipamento: {e}")
                            else:
                                st.session_state[f'confirm_delete_{row["Serial"]}'] = True
                                show_warning_message(f"Clique novamente para confirmar a exclusão do equipamento '{row['Serial']}'")
                                st.rerun()
                
                st.markdown("---")
                st.markdown("**Tabela Completa (para visualização):**")
            
            st.dataframe(df_filtrada, width='stretch')

            # Botão para popular dados aleatórios
            st.markdown("---")
            if st.button("🎲 Popular com Dados Aleatórios (20 equipamentos)"):
                db.popular_equipamentos_aleatorios(20)
                show_success_message("20 equipamentos aleatórios adicionados!")
                st.rerun()
        else:
            show_info_message("Nenhum equipamento cadastrado. Clique no botão abaixo para adicionar dados de exemplo.")
            if st.button("🎲 Gerar Dados de Exemplo"):
                db.popular_equipamentos_aleatorios(20)
                show_success_message("20 equipamentos aleatórios criados!")
                st.rerun()
