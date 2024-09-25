from datetime import datetime
from prefect import task

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_data(data):
    try:
        df = pd.DataFrame([data])
        filename = f"raw_data_{datetime.now().strftime('%Y%m%d%H%M%S')}.parquet"
        table = pa.Table.from_pandas(df)
        pq.write_table(table, filename)
        logger.info(f"Dados processados e salvos em {filename}")
        return filename
    except Exception as e:
        logger.error(f"Erro ao processar os dados: {str(e)}", exc_info=True)
        return None

@task
def prepare_dataframe_for_insert(df, tag):
    try:
        df['ingestion_date'] = datetime.now()
        df['line_data'] = df.apply(lambda row: row.to_json(), axis=1)
        df['tag'] = tag
        logger.info(f"DataFrame preparado para inserção com tag '{tag}'")
        return df[['ingestion_date', 'line_data', 'tag']]
    except Exception as e:
        logger.error(f"Erro ao preparar o DataFrame para inserção: {str(e)}", exc_info=True)
        return None