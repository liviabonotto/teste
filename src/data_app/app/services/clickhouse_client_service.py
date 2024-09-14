from dotenv import load_dotenv 
from services.logging_service import send_log_to_elasticsearch

import clickhouse_connect
import os
import pandas as pd
import logging

load_dotenv()

CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST')
CLICKHOUSE_PORT = os.getenv('CLICKHOUSE_PORT')
CLICKHOUSE_USERNAME = os.getenv('CLICKHOUSE_USERNAME')
CLICKHOUSE_PASSWORD = os.getenv('CLICKHOUSE_PASSWORD')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_client():
    try:
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USERNAME,
            password=CLICKHOUSE_PASSWORD
        )
        logger.info("Conexão com o ClickHouse estabelecida com sucesso.")
        return client
    
    except Exception as e:
        logger.error(f"Erro ao conectar ao ClickHouse: {str(e)}", exc_info=True)
        raise ConnectionError("Não foi possível conectar ao ClickHouse") from e

def execute_sql_script(script_path):
    try:
        client = get_client()
        with open(script_path, 'r') as file:
            sql_script = file.read()
        client.command(sql_script)

        logger.info(f"Script SQL executado com sucesso: {script_path}")

        return client
    
    except FileNotFoundError as e:
        logger.error(f"Arquivo SQL não encontrado: {str(e)}", exc_info=True)
        raise FileNotFoundError(f"O arquivo {script_path} não foi encontrado") from e
    except Exception as e:
        logger.error(f"Erro ao executar script SQL: {str(e)}", exc_info=True)
        raise RuntimeError("Falha ao executar o script SQL") from e

def insert_dataframe(client, table_name, df):
    try:
        client.insert_df(table_name, df)
        logger.info(f"DataFrame inserido na tabela '{table_name}' com sucesso.")
    
    except Exception as e:
        logger.error(f"Erro ao inserir dataframe na tabela {table_name}: {str(e)}", exc_info=True)
        raise RuntimeError(f"Falha ao inserir dados na tabela {table_name}") from e

def fetch_cost_data():
    log_message = []
    try:
        client = get_client()
        log_message.append("Conexão com o ClickHouse estabelecida com sucesso. \n")

        query = "SELECT * FROM cost_view"
        
        result = client.query(query)
        log_message.append(f"Query executada: {query} \n")
        
        df = pd.DataFrame(result.result_rows, columns=result.column_names)
        
        client.close()
        logger.info("Dados de custo buscados com sucesso.")
        log_message.append("Dados de custo buscados com sucesso. \n")
        
        status_code = 200
        return df

    except Exception as e:
        logger.error(f"Erro ao buscar dados de custo: {str(e)}", exc_info=True)
        log_message.append(f"Erro ao buscar dados de custo: {str(e)} \n")

        status_code = 500
        raise RuntimeError("Falha ao buscar dados de custo") from e

    finally:
        send_log_to_elasticsearch(log_message, "fetch_cost_data", status_code)

def fetch_price_data():
    log_message = []
    try:
        client = get_client()
        log_message.append("Conexão com o ClickHouse estabelecida com sucesso. \n")

        query = "SELECT * FROM price_view"
        
        result = client.query(query)
        log_message.append(f"Query executada: {query} \n")
        
        df = pd.DataFrame(result.result_rows, columns=result.column_names)
        
        client.close()
        logger.info("Dados de preço buscados com sucesso.")
        log_message.append("Dados de preço buscados com sucesso. \n")
        
        status_code = 200
        return df

    except Exception as e:
        logger.error(f"Erro ao buscar dados de preço: {str(e)}", exc_info=True)
        log_message.append(f"Erro ao buscar dados de preço: {str(e)} \n")

        status_code = 500
        raise RuntimeError("Falha ao buscar dados de preço") from e
    
    finally:
        send_log_to_elasticsearch(log_message, "fetch_price_data", status_code)
    
def fetch_store_regions_data():
    log_message = []
    try:
        client = get_client()
        log_message.append("Conexão com o ClickHouse estabelecida com sucesso. \n")

        query = "SELECT * FROM region_view"
        
        result = client.query(query)
        log_message.append(f"Query executada: {query} \n")
        
        df = pd.DataFrame(result.result_rows, columns=result.column_names)
        
        client.close()
        logger.info("Dados de regiões de loja buscados com sucesso.")
        log_message.append("Dados de regiões de loja buscados com sucesso. \n")
        
        status_code = 200
        return df

    except Exception as e:
        logger.error(f"Erro ao buscar dados de regiões de loja: {str(e)}", exc_info=True)
        log_message.append(f"Erro ao buscar dados de regiões de loja: {str(e)} \n")

        status_code = 500
        raise RuntimeError("Falha ao buscar dados de regiões de loja") from e
    
    finally:
        send_log_to_elasticsearch(log_message, "fetch_store_regions_data", status_code)

def fetch_margin_data():
    log_message = []
    try:
        client = get_client()
        log_message.append("Conexão com o ClickHouse estabelecida com sucesso. \n")

        query = "SELECT skd.categoria, skd.sub_categoria, yd.data_referencia, margem_lucro_bruto, lucro_bruto_financeiro, margem_lucro_bruto_regiao FROM margin_view  LIMIT 5000000 OFFSET 0;"     

        result = client.query(query)
        log_message.append(f"Query executada: {query} \n")
        
        df = pd.DataFrame(result.result_rows, columns=result.column_names)
        
        client.close()
        logger.info("Dados de margem buscados com sucesso.")
        log_message.append("Dados de margem buscados com sucesso. \n")
        
        status_code = 200
        return df

    except Exception as e:
        logger.error(f"Erro ao buscar dados de margem: {str(e)}", exc_info=True)
        log_message.append(f"Erro ao buscar dados de margem: {str(e)} \n")

        status_code = 500
        raise RuntimeError("Falha ao buscar dados de margem") from e
    
    finally:
        send_log_to_elasticsearch(log_message, "fetch_margin_data", status_code)
