import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime

def process_data(data):
    try:
        df = pd.DataFrame([data])
        filename = f"raw_data_{datetime.now().strftime('%Y%m%d%H%M%S')}.parquet"
        table = pa.Table.from_pandas(df)
        pq.write_table(table, filename)
        return filename
    except Exception as e:
        print(f"Erro ao processar os dados: {str(e)}")
        return None

def prepare_dataframe_for_insert(df, tag):
    try:
        df['ingestion_date'] = datetime.now()
        df['line_data'] = df.apply(lambda row: row.to_json(), axis=1)
        df['tag'] = tag
        return df[['ingestion_date', 'line_data', 'tag']]
    except Exception as e:
        print(f"Erro ao preparar o DataFrame para inserção: {str(e)}")
        return None