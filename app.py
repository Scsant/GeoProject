import streamlit as st
import pandas as pd
from filters import apply_filters
from exporter import to_excel
from style import set_style
from painel import mostrar_painel

# Aplicar estilo
set_style()

# Carregar dados do CSV
@st.cache_data

def carregar_dados_csv():
    return pd.read_csv("dados.csv", parse_dates=["data_cto", "data_inicio_operacao"])

# Carregar dados
with st.spinner('Carregando dados...'):
    df = carregar_dados_csv()

    # Aplicar filtros
    # Carregar e filtrar
    df = apply_filters(df)

    if df.empty:
        st.warning("Nenhum dado encontrado com os filtros aplicados.")
        st.stop()

    # ✅ Mostrar novo painel
    mostrar_painel(df)

    # ✅ Exibir dados e exportar
    st.dataframe(df, use_container_width=True, hide_index=True)

    excel_file = to_excel(df)
    st.download_button(
        label=' Baixar Excel',
        data=excel_file,
        file_name='baldeio_ativos.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


