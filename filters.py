#filters.py
import streamlit as st
import pandas as pd
from datetime import date

def apply_filters(df):
    df_filtered = df.copy()
    df_filtered['data_cto'] = pd.to_datetime(df_filtered['data_cto'], errors='coerce')
    df_filtered = df_filtered.dropna(subset=['data_cto'])

    st.sidebar.header('Filtros')

    regioes = st.sidebar.multiselect('Região', df_filtered['dcr_regiao'].unique())
    projetos = st.sidebar.multiselect('Projeto', df_filtered['nom_projeto'].unique())
    operacoes = st.sidebar.multiselect('Operação', df_filtered['dcr_operacao'].unique())

    if not df_filtered.empty:
        data_min_value = df_filtered['data_cto'].min().date()
        data_max_value = df_filtered['data_cto'].max().date()
    else:
        data_min_value = data_max_value = date.today()

    data_min = st.sidebar.date_input('Data Inicial', data_min_value)
    data_max = st.sidebar.date_input('Data Final', data_max_value)

    if data_min > data_max:
        st.sidebar.error("A data inicial não pode ser maior que a data final.")
        return df_filtered[0:0]

    if regioes:
        df_filtered = df_filtered[df_filtered['dcr_regiao'].isin(regioes)]
    if projetos:
        df_filtered = df_filtered[df_filtered['nom_projeto'].isin(projetos)]
    if operacoes:
        df_filtered = df_filtered[df_filtered['dcr_operacao'].isin(operacoes)]

    df_filtered = df_filtered[
        (df_filtered['data_cto'] >= pd.to_datetime(data_min)) &
        (df_filtered['data_cto'] <= pd.to_datetime(data_max))
    ]

    return df_filtered


