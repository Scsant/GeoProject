import streamlit as st
import pandas as pd

def mostrar_painel(df):
    total_operacoes = len(df)
    total_fazendas = df['nom_projeto'].nunique()
    total_talhoes = len(df['cd_talhao'])  # Com repetição
    total_municipios = df['dcr_municipio'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Operações Registradas", total_operacoes)
    with col2:
        st.metric("Fazendas Diferentes", total_fazendas)
    with col3:
        st.metric("Talhões (ocorrências)", total_talhoes)
    with col4:
        st.metric("Municípios", total_municipios)

    # Resumo por município
    with st.expander("📍 Detalhamento por município"):
        resumo = (
            df.groupby('dcr_municipio')
              .agg(fazendas=('nom_projeto', 'nunique'),
                   registros=('cd_talhao', 'count'))
              .sort_values(by='registros', ascending=False)
              .reset_index()
        )
        st.dataframe(resumo, use_container_width=True, hide_index=True)







