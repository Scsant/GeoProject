from sqlalchemy import create_engine
#import psycopg2
import pandas as pd
from sqlalchemy.sql import text
 
#  Conexão com o banco
db_connection_str = 'postgresql://tscarano:Bilbo_2301@172.28.3.183:5432/bracell_dwh'
engine = create_engine(db_connection_str)
conn = engine.connect()
 
#  Busca metadados das colunas
query_meta = text('''
select vcctc.cd_uso_solo,
vcctc.cd_regiao,
vcctc.dcr_regiao,
vcctc.id_projeto,
vcctc.nom_projeto,
vcctc.cd_talhao,
vcctc.data_cto,
vcctc.dcr_operacao,
    CASE
        WHEN dcr_operacao = 'BALDEIO FORWARDER' THEN 'BALDEIO'
        WHEN dcr_operacao = 'CORTE HARVESTER' THEN 'CORTE'
        WHEN dcr_operacao = 'CORTE FELLER' THEN 'CORTE'
        WHEN dcr_operacao = 'ARRASTE SKIDDER' THEN 'BALDEIO'
        ELSE 'NA'
    END AS operacao
from iforestry.vw_cubo_col_talhoes_cto vcctc
where cd_regiao in (10, 11)
and dcr_operacao in ('BALDEIO FORWARDER', 'CORTE HARVESTER', 'CORTE FELLER', 'ARRASTE SKIDDER')
 
''')
 
df_meta = pd.read_sql_query(query_meta, engine)
print(df_meta)