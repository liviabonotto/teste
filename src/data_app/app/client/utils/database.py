import clickhouse_connect
import pandas as pd
import os
from dotenv import load_dotenv 

load_dotenv()

CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST')
CLICKHOUSE_PORT = os.getenv('CLICKHOUSE_PORT')
CLICKHOUSE_USERNAME = os.getenv('CLICKHOUSE_USERNAME')
CLICKHOUSE_PASSWORD = os.getenv('CLICKHOUSE_PASSWORD')

def get_clickhouse_client():
    client = clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        username=CLICKHOUSE_USERNAME,
        password=CLICKHOUSE_PASSWORD
    )
    return client

def fetch_price_data():
    client = get_clickhouse_client()
    query = "SELECT * FROM price_view"
    
    result = client.query(query)
    
    df = pd.DataFrame(result.result_rows, columns=result.column_names)
    
    client.close()
    
    return df