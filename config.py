# Configurações do Sistema Offcon

# Configurações do Banco de Dados
DATABASE_NAME = "sistema_offcon.db"

# Configurações da Aplicação
APP_NAME = "Sistema Offcon"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sistema de Gestão de Containers Offshore"

# Configurações do Streamlit
PAGE_CONFIG = {
    "page_title": f"{APP_NAME} - Containers Offshore",
    "page_icon": "🚢",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Cores da Marca (baseado no site Offcon)
COLORS = {
    "primary": "#1e3a8a",  # Azul offshore
    "secondary": "#2563eb",  # Azul marinho
    "accent": "#3b82f6",  # Azul claro
    "success": "#10b981",  # Verde segurança
    "warning": "#f59e0b",  # Laranja alerta
    "danger": "#ef4444",  # Vermelho perigo
    "dark_bg": "#0f172a",  # Azul escuro
    "light_bg": "#f8fafc"  # Branco azulado
}

# Configurações de Páginas
PAGES = [
    {"name": "🏠 Início", "key": "home"},
    {"name": "📊 Dashboard", "key": "dashboard"},
    {"name": "� Containers", "key": "containers"},
    {"name": "🔧 Equipamentos", "key": "equipment"},
    {"name": "� Inspeções", "key": "inspections"},
    {"name": "📄 Relatórios", "key": "reports"}
]

# Configurações de Dados
DEFAULT_EQUIPMENT_COUNT = 20

# Tipos de Containers Offshore
CONTAINER_TYPES = [
    "Container 10FT Dry",
    "Container 10FT Open Top", 
    "Container 20FT Dry",
    "Container 20FT Open Top",
    "Caçamba / Waste Skip - 01",
    "Caixa Metalizada"
]

# Fabricantes (baseado no mercado offshore)
EQUIPMENT_MANUFACTURERS = ["Offcon Systems", "DNV Certified", "CIMC", "Singamas", "Maersk Container"]

# Categorias de Equipamentos
EQUIPMENT_CATEGORIES = ["Container Dry", "Container Open Top", "Caçamba Waste", "Caixa Metalizada", "Kit de Içamento"]

# Status de Containers
CONTAINER_STATUS = ["Disponível", "Alugado", "Em Manutenção", "Em Inspeção", "Inativo"]

# Tipos de Inspeção
INSPECTION_TYPES = [
    "Inspeção Periódica DNV",
    "Inspeção de Recebimento",
    "Inspeção de Entrega",
    "Inspeção de Manutenção",
    "Inspeção Extraordinária"
]

# Tipos de Serviços
SERVICE_TYPES = [
    "Projetos Customizados",
    "Locação",
    "Inspeção Periódica", 
    "Reparo e Manutenção",
    "Certificação DNV"
]

# Tipos de Medições
MEASUREMENT_TYPES = ["Temperatura", "Pressão", "Umidade", "Integridade Estrutural", "Corrosão"]

# Tipos de Relatórios
REPORT_TYPES = [
    "Relatório de Inspeção DNV",
    "Relatório de Manutenção",
    "Relatório de Locação", 
    "Relatório de Disponibilidade",
    "Relatório Completo"
]

# Certificações
CERTIFICATIONS = ["DNV 2.7.1", "DNV 2.7.3", "IMO MSC/Circ.860", "ISO 9001"]
