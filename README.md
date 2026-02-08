# Sistema Offcon

Sistema web para gestão de containers offshore e equipamentos industriais, desenvolvido com Streamlit.

## 🚀 Funcionalidades

- **Gestão de Containers**: Cadastro e controle de containers offshore (10FT, 20FT, Open Top, etc.)
- **Locação**: Controle de contratos de aluguel e disponibilidade
- **Inspeções**: Agendamento e registro de inspeções DNV
- **Clientes**: Gestão de clientes e contratos
- **Dashboard**: Métricas em tempo real e relatórios
- **Relatórios**: Geração de relatórios de conformidade e manutenção

## 🛠️ Tecnologias

- **Frontend**: Streamlit
- **Banco de Dados**: SQLite
- **Linguagem**: Python 3.12
- **Estilização**: CSS customizado

## 📋 Pré-requisitos

- Python 3.12+
- pip

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/yourusername/sistema-offcon.git
cd sistema-offcon
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
streamlit run main.py
```

## 📁 Estrutura do Projeto

```
sistemaOffcon/
├── main.py          # Aplicação principal (nova arquitetura)
├── app.py           # Aplicação legada
├── config.py        # Configurações e constantes
├── database.py      # Classe de gerenciamento do banco
├── utils.py         # Funções utilitárias
├── styles.css       # Estilos CSS customizados
├── pages/           # Módulos de páginas
│   ├── home.py
│   ├── dashboard.py
│   ├── containers.py
│   ├── equipment.py
│   ├── inspections.py
│   └── reports.py
└── README.md        # Este arquivo
```

## 🎯 Certificações e Compliance

- DNV 2.7.1, DNV 2.7.3
- IMO MSC/Circ.860
- ISO 9001

## 📊 Features

- Dashboard interativo com métricas em tempo real
- Gestão completa de containers offshore
- Sistema de locação com controle de disponibilidade
- Inspeções periódicas e relatórios de conformidade
- Exportação de dados em CSV
- Interface responsiva e moderna

## 🔧 Configuração

O sistema utiliza um arquivo `.env` para configurações:

```env
DATABASE_NAME=sistema_offcon.db
APP_NAME=Sistema Offcon
APP_VERSION=1.0.0
```

## 📝 Desenvolvimento

O projeto está em transição de uma arquitetura monolítica (`app.py`) para uma arquitetura modular (`main.py` + `pages/`).

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adicionando nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👥 Autor

Offcon Systems - Gestão de Containers Offshore

## 📞 Contato

- Email: contato@offcon.com.br
- Website: www.offcon.com.br
