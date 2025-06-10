import streamlit as st

def mostrar_painel(df):
    # Contagem geral
    total_talhoes = df['cd_talhao'].nunique()
    
    # Contagem por operação
    baldeio_count = df[df['dcr_operacao'].str.contains('BALDEIO', na=False)]['cd_talhao'].nunique()
    corte_count = df[df['dcr_operacao'].str.contains('CORTE', na=False)]['cd_talhao'].nunique()
    
    # Painel com 3 colunas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total de Talhões", value=total_talhoes)
    with col2:
        st.metric(label="Talhões - Baldeio", value=baldeio_count)

        
def mostrar_talhoes_pendentes(df):
    corte_talhoes = set(df[df['dcr_operacao'].str.contains('CORTE', na=False)]['cd_talhao'])
    baldeio_talhoes = set(df[df['dcr_operacao'].str.contains('BALDEIO', na=False)]['cd_talhao'])

    # Talhões que têm CORTE, mas ainda não têm BALDEIO
    pendentes = corte_talhoes - baldeio_talhoes

    st.info(f"🔎 Talhões com CORTE mas ainda sem BALDEIO: **{len(pendentes)}**")

    # Mostrar os registros filtrados
    df_pendentes = df[df['cd_talhao'].isin(pendentes) & df['dcr_operacao'].str.contains('CORTE', na=False)]

    st.dataframe(df_pendentes, use_container_width=True)
