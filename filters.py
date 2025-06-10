import streamlit as st
import pandas as pd
from datetime import date

def apply_filters(df):
    st.sidebar.header('Filtros')

    regioes = st.sidebar.multiselect('Região', df['dcr_regiao'].unique())
    projetos = st.sidebar.multiselect('Projeto', df['nom_projeto'].unique())
    operacoes = st.sidebar.multiselect('Operação', df['dcr_operacao'].unique())

    df['data_cto'] = pd.to_datetime(df['data_cto'], errors='coerce')
    df = df.dropna(subset=['data_cto'])

    if not df.empty:
        data_min_value = df['data_cto'].min().date()
        data_max_value = df['data_cto'].max().date()
    else:
        data_min_value = date.today()
        data_max_value = date.today()

    data_min = st.sidebar.date_input('Data Inicial', data_min_value)
    data_max = st.sidebar.date_input('Data Final', data_max_value)

    if regioes:
        df = df[df['dcr_regiao'].isin(regioes)]
    if projetos:
        df = df[df['nom_projeto'].isin(projetos)]
    if operacoes:
        df = df[df['dcr_operacao'].isin(operacoes)]

    df = df[(df['data_cto'] >= pd.to_datetime(data_min)) & (df['data_cto'] <= pd.to_datetime(data_max))]

    return df

