from services.utils_service import convert_csv_to_parquet, create_custom_temp_dir, get_csv_encoding, get_csv_separator
from services.s3_client_service import download_s3_file, list_s3_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from services.logging_service import send_log_to_elasticsearch

import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def has_overlay(row):
    return (row['data_inicio_x'] <= row['data_fim_y']) and (row['data_inicio_y'] <= row['data_fim_x'])

def load_data(file_name):
    try:
        temp_dir = create_custom_temp_dir()
        local_csv_path = os.path.join(temp_dir, os.path.basename(file_name))
        
        download_s3_file(file_name, local_csv_path)
        encoding = get_csv_encoding(local_csv_path)
        sep = get_csv_separator(local_csv_path, encoding)
        
        parquet_file_path, parquet_file_name = convert_csv_to_parquet(local_csv_path, encoding, sep)
        return pd.read_parquet(parquet_file_path)
    
    except Exception as e:
        logger.error(f"Erro ao carregar os dados do arquivo {file_name}: {e}", exc_info=True)
        raise RuntimeError(f"Erro ao carregar os dados do arquivo {file_name}: {str(e)}")

def transform_margin_data():
    log_message = []

    try:
        prefix = os.getenv('PREFIX')
        logger.info(f"Prefixo obtido: {prefix}")
        log_message.append(f"Prefixo obtido: {prefix} \n")

        csv_files = list_s3_files(prefix)
        logger.info(f"Arquivos CSV encontrados: {csv_files}")
        log_message.append(f"Arquivos CSV encontrados: {csv_files} \n")

        sku_dataset, price_dataset, cost_dataset = None, None, None
        
        for file_name in csv_files:
            try:
                if 'sku_dataset.csv' in file_name:
                    sku_dataset = load_data(file_name)
                    logger.info(f"Arquivo {file_name} carregado com sucesso.")
                    log_message.append(f"Arquivo {file_name} carregado com sucesso. \n")
                elif 'sku_price.csv' in file_name:
                    price_dataset = load_data(file_name)
                    logger.info(f"Arquivo {file_name} carregado com sucesso.")
                    log_message.append(f"Arquivo {file_name} carregado com sucesso. \n")
                elif 'sku_cost.csv' in file_name:
                    cost_dataset = load_data(file_name)
                    logger.info(f"Arquivo {file_name} carregado com sucesso.")
                    log_message.append(f"Arquivo {file_name} carregado com sucesso. \n")
            except Exception as e:
                logger.error(f"Erro ao processar o arquivo {file_name}: {e}", exc_info=True)
                log_message.append(f"Erro ao processar o arquivo {file_name}: {str(e)} \n")

        if sku_dataset is None or price_dataset is None or cost_dataset is None:
            raise ValueError("Um ou mais datasets não foram encontrados no S3.")
        
        merged_dataset = pd.merge(sku_dataset, price_dataset, on='cod_prod', how='inner')
        merged_dataset = pd.merge(merged_dataset, cost_dataset, on='cod_prod', how='inner')
        logger.info("Datasets mesclados com sucesso.")
        log_message.append("Datasets mesclados com sucesso. \n")

        merged_dataset['data_inicio_x'] = pd.to_datetime(merged_dataset['data_inicio_x'])
        merged_dataset['data_fim_x'] = pd.to_datetime(merged_dataset['data_fim_x'])
        merged_dataset['data_inicio_y'] = pd.to_datetime(merged_dataset['data_inicio_y'])
        merged_dataset['data_fim_y'] = pd.to_datetime(merged_dataset['data_fim_y'])
        logger.info("Datasets convertidos para datetime com sucesso.")
        log_message.append("Datasets convertidos para datetime com sucesso. \n")

        merged_dataset = merged_dataset[merged_dataset.apply(has_overlay, axis=1)]

        reference_date = pd.to_datetime('2023-09-01')
        
        merged_dataset = merged_dataset[
            (merged_dataset['data_inicio_x'] <= reference_date) &
            (merged_dataset['data_fim_x'] >= reference_date) &
            (merged_dataset['data_inicio_y'] <= reference_date) &
            (merged_dataset['data_fim_y'] >= reference_date)
        ]
        logger.info("Datasets filtrados com sucesso.")
        log_message.append("Datasets filtrados com sucesso. \n")
        
        merged_dataset['margem_lucro_bruto'] = ((merged_dataset['preco'] - merged_dataset['custo']) / merged_dataset['preco']) * 100
        merged_dataset['lucro_bruto_financeiro'] = (merged_dataset['preco'] - merged_dataset['custo']) / merged_dataset['preco']
        logger.info("Margem de lucro bruto calculada com sucesso.")
        log_message.append("Margem de lucro bruto calculada com sucesso. \n")

        unused_columns = ['conteudo_medida', 'conteudo_medida', 'data_inicio_x', 'data_fim_x', 'data_inicio_y', 'data_fim_y']
        merged_dataset.drop(columns=unused_columns, inplace=True)
        logger.info("Colunas desnecessárias removidas com sucesso.")
        log_message.append("Colunas desnecessárias removidas com sucesso. \n")
        status_code = 200
        
        return merged_dataset
    
    except Exception as e:
        logger.error(f"Erro ao transformar os dados de margem: {e}", exc_info=True)
        log_message.append(f"Erro ao transformar os dados de margem: {str(e)} \n")
        status_code = 500

        raise RuntimeError(f"Erro ao transformar os dados de margem: {str(e)}")
    
    finally:
        send_log_to_elasticsearch(log_message, "get_similar_product", status_code)

def get_similar_product(description_input, merged_dataset):
    log_message = []

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors_description = vectorizer.fit_transform(merged_dataset['descricao'])
        logger.info("Vetores de descrição criados com sucesso.")
        log_message.append("Vetores de descrição criados com sucesso. \n")

        input_vector = vectorizer.transform([description_input])
        similarities = cosine_similarity(input_vector, vectors_description).flatten()
        logger.info("Similaridades calculadas com sucesso.")
        log_message.append("Similaridades calculadas com sucesso. \n")

        merged_dataset['similaridade'] = similarities

        similar_products = merged_dataset.nlargest(3, 'similaridade')
        ordered_products = similar_products.sort_values(by='margem_lucro_bruto', ascending=False)
        logger.info("Produtos similares ordenados com sucesso.")
        log_message.append("Produtos similares ordenados com sucesso. \n")
        status_code = 200

        return ordered_products[['cod_prod', 'descricao', 'margem_lucro_bruto', 'similaridade']]
    
    except Exception as e:
        logger.error(f"Erro ao buscar produtos similares: {e}", exc_info=True)
        log_message.append(f"Erro ao buscar produtos similares: {str(e)} \n")
        status_code = 500

        raise RuntimeError(f"Erro ao buscar produtos similares: {str(e)}")
    
    finally:
        send_log_to_elasticsearch(log_message, "get_similar_product", status_code)
    
def get_similar_product_by_margin(description_input):
    try:
        merged_dataset = transform_margin_data()

        return get_similar_product(description_input, merged_dataset)

    except Exception as e:
        logger.error(f"Erro ao processar o produto por margem: {e}", exc_info=True)
        raise RuntimeError(f"Erro ao processar o produto por margem: {str(e)}")