from pathlib import Path
import streamlit as st
import pandas as pd
from exporter import to_excel
from datetime import date
from style import set_style

set_style()

@st.cache_data
def carregar_dados():
    return pd.read_csv("dados.csv", parse_dates=["data_inicio_operacao", "data_cto"])

df = carregar_dados()


# Filtro exatamente como na versão com banco
df = df[
    (df['dcr_operacao'] == 'BALDEIO FORWARDER') &
    (df['data_inicio_operacao'].notnull()) &
    (df['data_cto'].isnull()) &
    (df['flag_cto_executado'] == 'N')
]

# Marcar se a fazenda já teve baldeio executado com CTO
historico = pd.read_csv("dados.csv")  # Usa o mesmo arquivo completo
executadas = historico[historico['flag_cto_executado'] == 'S']['nom_projeto'].unique()
df['fazenda_ja_executada'] = df['nom_projeto'].isin(executadas)

st.sidebar.header("🔎 Filtros")
regioes = st.sidebar.multiselect("Região", df['dcr_regiao'].unique())
projetos = st.sidebar.multiselect("Fazenda (Projeto)", df['nom_projeto'].unique())
municipios = st.sidebar.multiselect("Município", df['dcr_municipio'].unique())

data_min = df['data_inicio_operacao'].min().date() if not df.empty else date.today()
data_max = df['data_inicio_operacao'].max().date() if not df.empty else date.today()
data_inicio = st.sidebar.date_input("Data Inicial", data_min)
data_fim = st.sidebar.date_input("Data Final", data_max)

df_filtrado = df.copy()
if regioes:
    df_filtrado = df_filtrado[df_filtrado['dcr_regiao'].isin(regioes)]
if projetos:
    df_filtrado = df_filtrado[df_filtrado['nom_projeto'].isin(projetos)]
if municipios:
    df_filtrado = df_filtrado[df_filtrado['dcr_municipio'].isin(municipios)]
df_filtrado = df_filtrado[
    (df_filtrado['data_inicio_operacao'] >= pd.to_datetime(data_inicio)) &
    (df_filtrado['data_inicio_operacao'] <= pd.to_datetime(data_fim))
]

if df_filtrado.empty:
    st.warning("Nenhum registro encontrado com os filtros selecionados.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Talhões", len(df_filtrado))
with col2:
    st.metric("Fazendas Únicas", df_filtrado['nom_projeto'].nunique())
with col3:
    st.metric("Municípios", df_filtrado['dcr_municipio'].nunique())
with col4:
    st.metric("Já Executadas", df_filtrado['fazenda_ja_executada'].sum())

st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

with st.expander("📂 Mostrar Talhões com CTO (Histórico das Fazendas Executadas)"):
    fazendas_executadas = df_filtrado[df_filtrado['fazenda_ja_executada']]['nom_projeto'].unique().tolist()
    if fazendas_executadas:
        cto_df = historico[
            (historico['flag_cto_executado'] == 'S') &
            (historico['nom_projeto'].isin(fazendas_executadas)) &
            (historico['data_cto'].notnull())
        ][['nom_projeto', 'cd_talhao', 'data_cto']]
        st.dataframe(cto_df, use_container_width=True, hide_index=True)
        if not cto_df.empty:
            excel_cto = to_excel(cto_df)
            st.download_button(
                label="Baixar Histórico CTO",
                data=excel_cto,
                file_name="historico_cto_fazendas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("Nenhuma fazenda com histórico de CTO encontrada nos filtros atuais.")

excel_data = to_excel(df_filtrado)
st.download_button(
    label=" Baixar Excel",
    data=excel_data,
    file_name="baldeio_sem_cto_com_inicio.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

