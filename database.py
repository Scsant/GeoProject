from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()  # carrega o .env

def get_connection():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    dbname = os.getenv('DB_NAME')

    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}')
    return engine.connect()


def carregar_dados(conn):
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
        WHERE vw_uso_solo_sde.nom_projeto = vcctc.nom_projeto
        LIMIT 1
    ) vuss ON TRUE
    WHERE vcctc.dcr_operacao IN ('BALDEIO FORWARDER', 'CORTE HARVESTER')
      AND vcctc.flag_cto_executado = 'S'
    """)
    return pd.read_sql_query(query, conn)
