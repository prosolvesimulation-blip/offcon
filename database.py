import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_name="sistema_offcon.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de containers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS containers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                tipo_container TEXT NOT NULL,
                fabricante TEXT,
                ano_fabricacao INTEGER,
                certificacao TEXT,
                status TEXT DEFAULT 'Disponível',
                cliente_id INTEGER,
                data_locacao TEXT,
                data_devolucao TEXT,
                data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cnpj TEXT,
                contato TEXT,
                email TEXT,
                telefone TEXT,
                endereco TEXT,
                data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de inspeções
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inspecoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                container_id INTEGER,
                tipo_inspecao TEXT NOT NULL,
                data_inspecao TEXT DEFAULT CURRENT_TIMESTAMP,
                resultado TEXT,
                proxima_inspecao TEXT,
                inspetor TEXT,
                certificado TEXT,
                observacoes TEXT,
                FOREIGN KEY (container_id) REFERENCES containers (id)
            )
        ''')
        
        # Tabela de manutenções
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS manutencoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                container_id INTEGER,
                tipo_manutencao TEXT NOT NULL,
                data_inicio TEXT,
                data_fim TEXT,
                descricao TEXT,
                custo REAL,
                status TEXT DEFAULT 'Pendente',
                tecnico TEXT,
                FOREIGN KEY (container_id) REFERENCES containers (id)
            )
        ''')
        
        # Tabela de equipamentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS equipamentos (
                serial TEXT PRIMARY KEY,
                modelo TEXT NOT NULL,
                fabricante TEXT,
                categoria TEXT,
                data_instalacao TEXT DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'ativo'
            )
        ''')
        
        # Tabela de projetos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projetos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                status TEXT DEFAULT 'ativo',
                data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de medições
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                projeto_id INTEGER,
                tipo_medicao TEXT NOT NULL,
                valor REAL NOT NULL,
                unidade TEXT,
                data_medicao TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (projeto_id) REFERENCES projetos (id)
            )
        ''')
        
        # Tabela de relatórios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relatorios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                projeto_id INTEGER,
                tipo_relatorio TEXT NOT NULL,
                conteudo TEXT,
                data_geracao TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (projeto_id) REFERENCES projetos (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def adicionar_projeto(self, nome, descricao=""):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projetos (nome, descricao, data_criacao, data_atualizacao)
            VALUES (?, ?, ?, ?)
        ''', (nome, descricao, datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
        projeto_id = cursor.lastrowid
        conn.close()
        return projeto_id
    
    def listar_projetos(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projetos ORDER BY data_criacao DESC')
        projetos = cursor.fetchall()
        conn.close()
        return projetos
    
    def adicionar_medicao(self, projeto_id, tipo_medicao, valor, unidade=""):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO medicoes (projeto_id, tipo_medicao, valor, unidade, data_medicao)
            VALUES (?, ?, ?, ?, ?)
        ''', (projeto_id, tipo_medicao, valor, unidade, datetime.now().isoformat()))
        conn.commit()
        medicao_id = cursor.lastrowid
        conn.close()
        return medicao_id
    
    def listar_medicoes(self, projeto_id=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        if projeto_id:
            cursor.execute('''
                SELECT m.*, p.nome as projeto_nome 
                FROM medicoes m 
                JOIN projetos p ON m.projeto_id = p.id 
                WHERE m.projeto_id = ? 
                ORDER BY m.data_medicao DESC
            ''', (projeto_id,))
        else:
            cursor.execute('''
                SELECT m.*, p.nome as projeto_nome 
                FROM medicoes m 
                JOIN projetos p ON m.projeto_id = p.id 
                ORDER BY m.data_medicao DESC
            ''')
        medicoes = cursor.fetchall()
        conn.close()
        return medicoes
    
    def gerar_relatorio(self, projeto_id, tipo_relatorio, conteudo):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO relatorios (projeto_id, tipo_relatorio, conteudo, data_geracao)
            VALUES (?, ?, ?, ?)
        ''', (projeto_id, tipo_relatorio, conteudo, datetime.now().isoformat()))
        conn.commit()
        relatorio_id = cursor.lastrowid
        conn.close()
        return relatorio_id
    
    def listar_relatorios(self, projeto_id=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        if projeto_id:
            cursor.execute('''
                SELECT r.*, p.nome as projeto_nome 
                FROM relatorios r 
                JOIN projetos p ON r.projeto_id = p.id 
                WHERE r.projeto_id = ? 
                ORDER BY r.data_geracao DESC
            ''', (projeto_id,))
        else:
            cursor.execute('''
                SELECT r.*, p.nome as projeto_nome 
                FROM relatorios r 
                JOIN projetos p ON r.projeto_id = p.id 
                ORDER BY r.data_geracao DESC
            ''')
        relatorios = cursor.fetchall()
        conn.close()
        return relatorios
    
    def adicionar_equipamento(self, serial, modelo, fabricante="", categoria="", status="ativo"):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO equipamentos (serial, modelo, fabricante, categoria, data_instalacao, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (serial, modelo, fabricante, categoria, datetime.now().isoformat(), status))
        conn.commit()
        conn.close()

    def listar_equipamentos(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM equipamentos ORDER BY data_instalacao DESC')
        equipamentos = cursor.fetchall()
        conn.close()
        return equipamentos

    def popular_equipamentos_aleatorios(self, quantidade=20):
        """Popula o banco com dados aleatórios para equipamentos"""
        import random
        from utils import generate_serial_number
        from config import EQUIPMENT_CATEGORIES
        
        modelos = [
            "OFFCON-1000", "OFFCON-2000", "OFFCON-3000X", "OFFCON-4000PRO",
            "SMART-METER-01", "SMART-METER-02", "POWER-SENSOR-A", "POWER-SENSOR-B",
            "ENERGY-MON-1", "ENERGY-MON-2", "GRID-CONNECT-500", "GRID-CONNECT-1000"
        ]

        fabricantes = ["Offcon Systems", "TechEnergy", "PowerTech", "SmartGrid", "EcoEnergy"]
        categorias = EQUIPMENT_CATEGORIES

        for i in range(quantidade):
            serial = generate_serial_number()
            modelo = random.choice(modelos)
            fabricante = random.choice(fabricantes)
            categoria = random.choice(categorias)
            status = random.choice(["ativo", "inativo"])

            self.adicionar_equipamento(serial, modelo, fabricante, categoria, status)
    
    def popular_dados_aleatorios(self, quantidade=20):
        """Popula o banco com dados aleatórios para containers offshore"""
        import random
        from config import CONTAINER_TYPES, EQUIPMENT_MANUFACTURERS, CONTAINER_STATUS, CERTIFICATIONS
        
        # Popular containers
        for i in range(quantidade):
            codigo = f"OFF{random.randint(1000, 9999)}-{random.randint(100, 999)}"
            tipo_container = random.choice(CONTAINER_TYPES)
            fabricante = random.choice(EQUIPMENT_MANUFACTURERS)
            ano_fabricacao = random.randint(2015, 2024)
            certificacao = random.choice(CERTIFICATIONS)
            status = random.choice(CONTAINER_STATUS)
            
            self.adicionar_container(codigo, tipo_container, fabricante, ano_fabricacao, certificacao, status)
        
        # Popular clientes
        nomes_clientes = [
            "Petrobras", "Shell Brasil", "Chevron Brasil", "Equinor Brasil", 
            "TotalEnergies", "BP Brasil", "Repsol Sinopec", "Enauta"
        ]
        
        for nome in nomes_clientes:
            cnpj = f"{random.randint(10, 99)}.{random.randint(100, 999)}.{random.randint(100, 999)}/0001-{random.randint(10, 99)}"
            self.adicionar_cliente(nome, cnpj, f"Contato {nome}", f"contato@{nome.lower().replace(' ', '')}.com.br", f"+55 21 {random.randint(3000, 9999)}-{random.randint(1000, 9999)}")
    
    def adicionar_container(self, codigo, tipo_container, fabricante="", ano_fabricacao=None, certificacao="", status="Disponível"):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO containers (codigo, tipo_container, fabricante, ano_fabricacao, certificacao, status, data_criacao, data_atualizacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (codigo, tipo_container, fabricante, ano_fabricacao, certificacao, status, datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def listar_containers(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM containers ORDER BY data_criacao DESC')
        containers = cursor.fetchall()
        conn.close()
        return containers
    
    def adicionar_cliente(self, nome, cnpj="", contato="", email="", telefone="", endereco=""):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nome, cnpj, contato, email, telefone, endereco, data_cadastro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, cnpj, contato, email, telefone, endereco, datetime.now().isoformat()))
        conn.commit()
        cliente_id = cursor.lastrowid
        conn.close()
        return cliente_id
    
    def listar_clientes(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes ORDER BY nome')
        clientes = cursor.fetchall()
        conn.close()
        return clientes
    
    def adicionar_inspecao(self, container_id, tipo_inspecao, resultado="", proxima_inspecao="", inspetor="", certificado="", observacoes=""):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO inspecoes (container_id, tipo_inspecao, data_inspecao, resultado, proxima_inspecao, inspetor, certificado, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (container_id, tipo_inspecao, datetime.now().isoformat(), resultado, proxima_inspecao, inspetor, certificado, observacoes))
        conn.commit()
        inspecao_id = cursor.lastrowid
        conn.close()
        return inspecao_id
    
    def listar_inspecoes(self, container_id=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        if container_id:
            cursor.execute('''
                SELECT i.*, c.codigo as container_codigo 
                FROM inspecoes i 
                JOIN containers c ON i.container_id = c.id 
                WHERE i.container_id = ? 
                ORDER BY i.data_inspecao DESC
            ''', (container_id,))
        else:
            cursor.execute('''
                SELECT i.*, c.codigo as container_codigo 
                FROM inspecoes i 
                JOIN containers c ON i.container_id = c.id 
                ORDER BY i.data_inspecao DESC
            ''')
        inspecoes = cursor.fetchall()
        conn.close()
        return inspecoes
        import random
        
        modelos = [
            "OFFCON-1000", "OFFCON-2000", "OFFCON-3000X", "OFFCON-4000PRO",
            "SMART-METER-01", "SMART-METER-02", "POWER-SENSOR-A", "POWER-SENSOR-B",
            "ENERGY-MON-1", "ENERGY-MON-2", "GRID-CONNECT-500", "GRID-CONNECT-1000"
        ]
        
        fabricantes = ["Offcon Systems", "TechEnergy", "PowerTech", "SmartGrid", "EcoEnergy"]
        categorias = ["Medidor", "Sensor", "Inversor", "Controlador", "Monitor"]
        
        for i in range(quantidade):
            serial = f"OFF{random.randint(10000, 99999)}{random.randint(100, 999)}"
            modelo = random.choice(modelos)
            fabricante = random.choice(fabricantes)
            categoria = random.choice(categorias)
            
            self.adicionar_equipamento(serial, modelo, fabricante, categoria)

# Inicialização do banco
db = Database()

# Popular dados aleatórios na primeira execução
containers_existentes = db.listar_containers()
if len(containers_existentes) == 0:
    db.popular_dados_aleatorios(20)
    print("Dados aleatórios de containers offshore criados com sucesso!")
