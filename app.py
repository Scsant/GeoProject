import streamlit as st
from database import get_connection, carregar_dados
from filters import apply_filters
from exporter import to_excel
from style import set_style
from painel import mostrar_painel

# Configurações iniciais
set_style()

# Conexão com o banco
engine = get_connection()

# Carregar dados com conexão ativa
with engine.connect() as conn:
    with st.spinner('Carregando dados...'):
        df = carregar_dados(conn)

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


