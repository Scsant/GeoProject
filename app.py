import streamlit as st
from database import get_connection, carregar_dados
from filters import apply_filters
from exporter import to_excel
from style import set_style
from painel import mostrar_painel, mostrar_talhoes_pendentes

# Aplicar estilo
set_style()

# Conexão com banco
conn = get_connection()

# Carregar dados
with st.spinner('Carregando dados...'):
    df = carregar_dados(conn)

# Aplicar filtros
df = apply_filters(df)



# Mostrar painel
mostrar_painel(df)
mostrar_talhoes_pendentes(df)

# Exibir DataFrame
st.dataframe(df, use_container_width=True, hide_index=True)

# Download Excel
excel_file = to_excel(df)
st.download_button(
    label=' Baixar Excel',
    data=excel_file,
    file_name='talhoes_baldeio.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
