import streamlit as st
import pandas as pd
import numpy as np
from database import Database

# Configuração da página
st.set_page_config(
    page_title="Sistema Offcon - Gestão de Energia",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar CSS personalizado
def load_css():
    with open("styles.css", "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css()

st.title("⚡ Sistema Offcon")
st.markdown("---")

# Inicializar banco de dados
db = Database()

# Sidebar
st.sidebar.title("🚀 Navegação")
st.sidebar.markdown("---")
pagina = st.sidebar.selectbox("Escolha uma página:", ["🏠 Início", "📊 Dashboard", "📁 Projetos", "🔧 Equipamentos", "📈 Análises", "📄 Relatórios"])

# Página Inicial
if pagina == "🏠 Início":
    # Header principal
    st.markdown("""
    <div class="header-container">
        <h1 style="font-size: 3rem; margin-bottom: 1rem;">⚡ Sistema Offcon</h1>
        <p style="font-size: 1.5rem; margin-bottom: 2rem; opacity: 0.9;">
            Plataforma Inteligente de Gestão de Energia
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
    
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-item">
            <h3 style="margin: 0; font-size: 2rem;">{len(projetos)}</h3>
            <p style="margin: 0; opacity: 0.9;">Projetos Ativos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-item" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3 style="margin: 0; font-size: 2rem;">{len(equipamentos)}</h3>
            <p style="margin: 0; opacity: 0.9;">Equipamentos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-item" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <h3 style="margin: 0; font-size: 2rem;">{len(medicoes)}</h3>
            <p style="margin: 0; opacity: 0.9;">Medições</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        relatorios = db.listar_relatorios()
        st.markdown(f"""
        <div class="stat-item" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <h3 style="margin: 0; font-size: 2rem;">{len(relatorios)}</h3>
            <p style="margin: 0; opacity: 0.9;">Relatórios</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recursos principais
    st.markdown('<h2 style="text-align: center; margin-bottom: 3rem;">🚀 Recursos Principais</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card fade-in">
            <div class="feature-icon">📊</div>
            <h3>Dashboard Inteligente</h3>
            <p>Visualize em tempo real todas as métricas importantes do seu sistema de energia com gráficos interativos e relatórios automáticos.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card fade-in">
            <div class="feature-icon">🔧</div>
            <h3>Gestão de Equipamentos</h3>
            <p>Controle todo o seu parque de equipamentos com informações detalhadas de serial, modelo e status de operação.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card fade-in">
            <div class="feature-icon">📈</div>
            <h3>Análise Avançada</h3>
            <p>Ferramentas poderosas para análise de dados, identificação de padrões e otimização do consumo energético.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Seção de ações rápidas
    st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">⚡ Ações Rápidas</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🆕 Novo Projeto", type="secondary"):
            st.session_state.selected_page = "📁 Projetos"
            st.rerun()
    
    with col2:
        if st.button("➕ Adicionar Equipamento", type="secondary"):
            st.session_state.selected_page = "🔧 Equipamentos"
            st.rerun()
    
    with col3:
        if st.button("📊 Gerar Relatório", type="secondary"):
            st.session_state.selected_page = "📄 Relatórios"
            st.rerun()
    
    with col4:
        if st.button("📈 Ver Análises", type="secondary"):
            st.session_state.selected_page = "📈 Análises"
            st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h3>⚡ Sistema Offcon</h3>
        <p>Solução completa para gestão de energia off-grid</p>
        <p style="opacity: 0.7; margin-top: 1rem;">
            © 2024 Offcon Systems. Todos os direitos reservados.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif pagina == "📊 Dashboard":
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

elif pagina == "📁 Projetos":
    st.header("📁 Gestão de Projetos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Adicionar Novo Projeto")
        nome_projeto = st.text_input("Nome do Projeto")
        desc_projeto = st.text_area("Descrição")
        
        if st.button("💾 Criar Projeto"):
            if nome_projeto:
                projeto_id = db.adicionar_projeto(nome_projeto, desc_projeto)
                st.success(f"Projeto '{nome_projeto}' criado com ID: {projeto_id}")
                st.rerun()
            else:
                st.error("Por favor, informe o nome do projeto.")
    
    with col2:
        st.subheader("Adicionar Medição")
        projetos = db.listar_projetos()
        if projetos:
            projeto_options = {f"{p[1]} (ID: {p[0]})": p[0] for p in projetos}
            projeto_selecionado = st.selectbox("Selecione o Projeto", list(projeto_options.keys()))
            
            tipo_medicao = st.selectbox("Tipo de Medição", ["Consumo", "Produção", "Eficiência", "Temperatura", "Pressão"])
            valor_medicao = st.number_input("Valor", value=0.0)
            unidade_medicao = st.text_input("Unidade", placeholder="kWh, °C, bar, etc.")
            
            if st.button("📊 Adicionar Medição"):
                projeto_id = projeto_options[projeto_selecionado]
                db.adicionar_medicao(projeto_id, tipo_medicao, valor_medicao, unidade_medicao)
                st.success("Medição adicionada com sucesso!")
                st.rerun()
        else:
            st.info("Cadastre um projeto primeiro para adicionar medições.")
    
    # Lista de projetos
    st.markdown("---")
    st.subheader("📋 Todos os Projetos")
    projetos = db.listar_projetos()
    if projetos:
        df_projetos = pd.DataFrame(projetos, columns=['ID', 'Nome', 'Descrição', 'Status', 'Criação', 'Atualização'])
        st.dataframe(df_projetos, width='stretch')
    else:
        st.info("Nenhum projeto cadastrado.")

elif pagina == "🔧 Equipamentos":
    st.header("🔧 Gestão de Equipamentos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Adicionar Novo Equipamento")
        serial = st.text_input("Serial (único)", placeholder="OFF123456789")
        modelo = st.text_input("Modelo")
        fabricante = st.text_input("Fabricante")
        categoria = st.selectbox("Categoria", ["Medidor", "Sensor", "Inversor", "Controlador", "Monitor", "Outro"])
        
        if st.button("💾 Adicionar Equipamento"):
            if serial and modelo:
                try:
                    db.adicionar_equipamento(serial, modelo, fabricante, categoria)
                    st.success(f"Equipamento '{modelo}' adicionado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao adicionar equipamento: {e}")
            else:
                st.error("Preencha pelo menos Serial e Modelo.")
    
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
            st.info("Nenhum equipamento cadastrado.")
    
    # Tabela completa de equipamentos
    st.markdown("---")
    st.subheader("📋 Todos os Equipamentos")
    equipamentos = db.listar_equipamentos()
    
    if equipamentos:
        df_equipamentos = pd.DataFrame(equipamentos, columns=['Serial', 'Modelo', 'Fabricante', 'Categoria', 'Instalação', 'Status'])
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            filtro_fabricante = st.selectbox("Filtrar por Fabricante", ["Todos"] + list(df_equipamentos['Fabricante'].unique()))
        with col2:
            filtro_categoria = st.selectbox("Filtrar por Categoria", ["Todos"] + list(df_equipamentos['Categoria'].unique()))
        with col3:
            filtro_status = st.selectbox("Filtrar por Status", ["Todos"] + list(df_equipamentos['Status'].unique()))
        
        # Aplicar filtros
        df_filtrada = df_equipamentos.copy()
        if filtro_fabricante != "Todos":
            df_filtrada = df_filtrada[df_filtrada['Fabricante'] == filtro_fabricante]
        if filtro_categoria != "Todos":
            df_filtrada = df_filtrada[df_filtrada['Categoria'] == filtro_categoria]
        if filtro_status != "Todos":
            df_filtrada = df_filtrada[df_filtrada['Status'] == filtro_status]
        
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
                                st.success(f"Equipamento '{row['Serial']}' deletado com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao deletar equipamento: {e}")
                        else:
                            st.session_state[f'confirm_delete_{row["Serial"]}'] = True
                            st.warning(f"Clique novamente para confirmar a exclusão do equipamento '{row['Serial']}'")
                            st.rerun()
            
            st.markdown("---")
            st.markdown("**Tabela Completa (para visualização):**")
        
        st.dataframe(df_filtrada, width='stretch')
        
        # Botão para popular dados aleatórios
        st.markdown("---")
        if st.button("🎲 Popular com Dados Aleatórios (20 equipamentos)"):
            db.popular_equipamentos_aleatorios(20)
            st.success("20 equipamentos aleatórios adicionados!")
            st.rerun()
    else:
        st.info("Nenhum equipamento cadastrado. Clique no botão abaixo para adicionar dados de exemplo.")
        if st.button("🎲 Gerar Dados de Exemplo"):
            db.popular_equipamentos_aleatorios(20)
            st.success("20 equipamentos aleatórios criados!")
            st.rerun()

elif pagina == "📈 Análises":
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
        df_filtrada = df_medicoes.copy()
        if tipo_filtro != "Todos":
            df_filtrada = df_filtrada[df_filtrada['Tipo'] == tipo_filtro]
        if projeto_filtro != "Todos":
            df_filtrada = df_filtrada[df_filtrada['Projeto_Nome'] == projeto_filtro]
        
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
        df_tipo = df_filtrada.groupby('Tipo')['Valor'].sum().reset_index()
        st.bar_chart(df_tipo.set_index('Tipo'))
        
        # Tabela detalhada
        st.markdown("---")
        st.subheader("📋 Dados Detalhados")
        st.dataframe(df_filtrada[['Data', 'Projeto_Nome', 'Tipo', 'Valor', 'Unidade']], width='stretch')
    else:
        st.info("Nenhuma medição encontrada. Cadastre projetos e medições primeiro.")
    
    # Upload de arquivos
    st.markdown("---")
    st.subheader("📁 Importar Dados")
    uploaded_file = st.file_uploader("Carregue um arquivo CSV para importar medições", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df_import = pd.read_csv(uploaded_file)
            st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")
            st.dataframe(df_import.head())
            
            if st.button("📥 Importar Medições"):
                # Lógica de importação (adaptar conforme colunas do CSV)
                st.info("Funcionalidade de importação em desenvolvimento.")
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

elif pagina == "📄 Relatórios":
    st.header("📄 Relatórios")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Gerar Novo Relatório")
        
        projetos = db.listar_projetos()
        if projetos:
            projeto_options = {f"{p[1]} (ID: {p[0]})": p[0] for p in projetos}
            projeto_selecionado = st.selectbox("Selecione o Projeto", list(projeto_options.keys()))
            
            tipo_relatorio = st.selectbox(
                "Tipo de Relatório:",
                ["Relatório de Consumo", "Relatório de Produção", "Relatório de Eficiência", "Relatório Completo"]
            )
            
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
                    valor_max = df_medicoes['Valor'].max()
                    valor_min = df_medicoes['Valor'].min()
                    
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
                    st.success(f"Relatório gerado com ID: {relatorio_id}")
                    st.rerun()
                else:
                    st.warning("Nenhuma medição encontrada para este projeto no período selecionado.")
        else:
            st.info("Nenhum projeto cadastrado. Crie um projeto primeiro.")
    
    with col2:
        st.subheader("📋 Relatórios Salvos")
        relatorios = db.listar_relatorios()
        
        if relatorios:
            for relatorio in relatorios[:5]:  # Mostrar apenas 5 mais recentes
                with st.expander(f"{relatorio[2]} - {relatorio[4][:10]}"):
                    st.text(relatorio[3])
                    st.caption(f"Projeto: {relatorio[5]}")
        else:
            st.info("Nenhum relatório gerado ainda.")
    
    # Lista completa de relatórios
    st.markdown("---")
    st.subheader("📄 Todos os Relatórios")
    relatorios = db.listar_relatorios()
    
    if relatorios:
        df_relatorios = pd.DataFrame(relatorios, columns=['ID', 'Projeto_ID', 'Tipo', 'Conteúdo', 'Data', 'Projeto_Nome'])
        st.dataframe(df_relatorios[['ID', 'Projeto_Nome', 'Tipo', 'Data']], width='stretch')
        
        # Opção de download
        if st.button("📥 Exportar Relatórios (CSV)"):
            df_relatorios.to_csv('relatorios_export.csv', index=False)
            st.success("Relatórios exportados para 'relatorios_export.csv'")
    else:
        st.info("Nenhum relatório encontrado.")

# Rodapé
st.markdown("---")
st.markdown("Desenvolvido com ❤️ usando Streamlit")
