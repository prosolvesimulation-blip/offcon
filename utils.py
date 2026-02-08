# Utilitários do Sistema Offcon

import streamlit as st
import pandas as pd
from datetime import datetime
import random

def format_date(date_string):
    """Formata data string para formato brasileiro"""
    try:
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return date_obj.strftime('%d/%m/%Y %H:%M')
    except:
        return date_string

def format_number(value, decimal_places=2):
    """Formata número com casas decimais"""
    try:
        return f"{float(value):.{decimal_places}f}"
    except:
        return str(value)

def create_metric_card(title, value, delta=None, color="blue"):
    """Cria um card de métrica personalizado"""
    delta_html = f"<span style='color: {'green' if delta and delta > 0 else 'red'}'>{delta:+.1f}</span>" if delta else ""
    
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid {color};
        text-align: center;
    ">
        <h4 style="margin: 0; color: #666; font-size: 0.9rem;">{title}</h4>
        <h2 style="margin: 0.5rem 0; color: #333; font-size: 2rem;">{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_feature_card(icon, title, description):
    """Cria um card de recurso"""
    return f"""
    <div class="feature-card fade-in">
        <div class="feature-icon">{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
    </div>
    """

def create_stat_card(value, label, gradient="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"):
    """Cria um card de estatística"""
    return f"""
    <div class="stat-item" style="background: {gradient};">
        <h3 style="margin: 0; font-size: 2rem;">{value}</h3>
        <p style="margin: 0; opacity: 0.9;">{label}</p>
    </div>
    """

def generate_serial_number():
    """Gera um número de serial aleatório"""
    return f"OFF{random.randint(10000, 99999)}{random.randint(100, 999)}"

def validate_form_data(data, required_fields):
    """Valida dados de formulário"""
    errors = []
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"O campo '{field}' é obrigatório")
    return errors

def create_download_button(data, filename, button_text="Download"):
    """Cria botão de download para DataFrame"""
    csv = data.to_csv(index=False)
    st.download_button(
        label=button_text,
        data=csv,
        file_name=filename,
        mime='text/csv'
    )

def show_success_message(message):
    """Exibe mensagem de sucesso"""
    st.success(f"✅ {message}")

def show_error_message(message):
    """Exibe mensagem de erro"""
    st.error(f"❌ {message}")

def show_info_message(message):
    """Exibe mensagem informativa"""
    st.info(f"ℹ️ {message}")

def show_warning_message(message):
    """Exibe mensagem de aviso"""
    st.warning(f"⚠️ {message}")

def filter_dataframe(df, filters):
    """Aplica filtros a um DataFrame"""
    filtered_df = df.copy()
    
    for column, value in filters.items():
        if value and value != "Todos":
            filtered_df = filtered_df[filtered_df[column] == value]
    
    return filtered_df

def create_chart_data(df, group_column, value_column, aggregation='sum'):
    """Cria dados para gráficos"""
    if aggregation == 'sum':
        chart_data = df.groupby(group_column)[value_column].sum().reset_index()
    elif aggregation == 'mean':
        chart_data = df.groupby(group_column)[value_column].mean().reset_index()
    elif aggregation == 'count':
        chart_data = df.groupby(group_column)[value_column].count().reset_index()
    else:
        chart_data = df.groupby(group_column)[value_column].sum().reset_index()
    
    return chart_data

def safe_get_session_state(key, default=None):
    """Obtém valor do session state de forma segura"""
    return getattr(st.session_state, key, default)

def safe_set_session_state(key, value):
    """Define valor no session state de forma segura"""
    st.session_state[key] = value
