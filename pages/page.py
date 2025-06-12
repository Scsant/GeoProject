import streamlit as st
import pandas as pd
from database import get_connection
from sqlalchemy import text
from exporter import to_excel
from datetime import date
from style import set_style

# Configurações iniciais
set_style()


engine = get_connection()

with engine.connect() as conn:
    with st.spinner("🔄 Carregando dados..."):
        query = text("""
            SELECT 
                vcctc.dcr_regiao,
                vcctc.id_projeto,
                vcctc.nom_projeto,
                vcctc.cd_talhao,
                vcctc.data_cto,
                vcctc.dcr_operacao,
                vcctc.flag_cto_executado,
                vcctc.data_inicio_operacao,
                vuss.dcr_municipio,
                vuss.dcr_estado,
                vuss.vlr_area
            FROM iforestry.vw_cubo_col_talhoes_cto vcctc
            LEFT JOIN LATERAL (
                SELECT dcr_municipio, dcr_estado, vlr_area
                FROM iforestry.vw_uso_solo_sde
                WHERE nom_projeto = vcctc.nom_projeto
                LIMIT 1
            ) vuss ON TRUE
            WHERE vcctc.dcr_operacao = 'BALDEIO FORWARDER'
              AND vcctc.data_inicio_operacao IS NOT NULL
              AND vcctc.data_cto IS NULL
              AND vcctc.flag_cto_executado = 'N'
        """)
        df = pd.DataFrame(conn.execute(query).fetchall(), columns=[
            'dcr_regiao', 'id_projeto', 'nom_projeto', 'cd_talhao', 'data_cto',
            'dcr_operacao', 'flag_cto_executado', 'data_inicio_operacao',
            'dcr_municipio', 'dcr_estado', 'vlr_area'
        ])

        hist_query = text("""
            SELECT DISTINCT nom_projeto
            FROM iforestry.vw_cubo_col_talhoes_cto
            WHERE dcr_operacao = 'BALDEIO FORWARDER'
              AND flag_cto_executado = 'S'
        """)
        historico = pd.DataFrame(conn.execute(hist_query).fetchall(), columns=['nom_projeto'])

df['data_inicio_operacao'] = pd.to_datetime(df['data_inicio_operacao'], errors='coerce')
df['fazenda_ja_executada'] = df['nom_projeto'].isin(historico['nom_projeto'])

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
        query_cto = text(f'''
            SELECT 
                nom_projeto,
                cd_talhao,
                data_cto
            FROM iforestry.vw_cubo_col_talhoes_cto
            WHERE dcr_operacao = 'BALDEIO FORWARDER'
              AND flag_cto_executado = 'S'
              AND nom_projeto IN ({','.join([f"'{f}'" for f in fazendas_executadas])})
        ''')
        with engine.connect() as conn:
            cto_df = pd.DataFrame(conn.execute(query_cto).fetchall(), columns=[
                'nom_projeto', 'cd_talhao', 'data_cto'
            ])
        st.dataframe(cto_df, use_container_width=True, hide_index=True)
        # Inserir botão de download do histórico de CTO dentro do expander

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

