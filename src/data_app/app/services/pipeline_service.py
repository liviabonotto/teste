from flask import Flask, jsonify
from services.clickhouse_client_service import get_client, insert_dataframe
from services.data_processing_service import prepare_dataframe_for_insert
from services.utils_service import create_custom_temp_dir, convert_csv_to_parquet, get_table_name_from_filename, get_csv_encoding, get_csv_separator
from services.s3_client_service import list_s3_files, download_s3_file, upload_s3_file
from services.logging_service import send_log_to_elasticsearch
from prefect import flow

import os
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@flow
def process_data_from_s3():
    log_message = []

    try:
        prefix = os.getenv('PREFIX')
        logger.info(f"Prefixo obtido: {prefix}")
        log_message.append(f"Prefixo obtido: {prefix} \n")

        csv_files = list_s3_files(prefix)
        logger.info(f"Arquivos CSV encontrados: {csv_files}")
        log_message.append(f"Arquivos CSV encontrados: {csv_files} \n")

        if not csv_files:
            logger.warning("Nenhum arquivo CSV encontrado no bucket S3")
            log_message.append("Nenhum arquivo CSV encontrado no bucket S3 \n")
            return jsonify({"error": "Nenhum arquivo CSV encontrado no bucket S3"}), 400

        temp_dir = create_custom_temp_dir()
        logger.info(f"Diretório temporário criado: {temp_dir}")
        log_message.append(f"Diretório temporário criado: {temp_dir} \n")

        for csv_file in csv_files:
            try:
                local_csv_file = os.path.join(temp_dir, os.path.basename(csv_file))
                logger.info(f"Baixando arquivo CSV: {csv_file} para {local_csv_file}")
                log_message.append(f"Baixando arquivo CSV: {csv_file} para {local_csv_file} \n")
                download_s3_file(csv_file, local_csv_file)

                encoding = get_csv_encoding(local_csv_file)
                logger.info(f"Encoding do arquivo CSV: {encoding}")
                log_message.append(f"Encoding do arquivo CSV: {encoding} \n")
                
                sep = get_csv_separator(local_csv_file, encoding)
                logger.info(f"Separador do arquivo CSV: {sep}")
                log_message.append(f"Separador do arquivo CSV: {sep} \n")

                parquet_file_path, parquet_file_name = convert_csv_to_parquet(local_csv_file, encoding, sep)
                print(f"Arquivo CSV convertido para Parquet: {parquet_file_path}")
                log_message.append(f"Arquivo CSV convertido para Parquet: {parquet_file_path} \n")

                upload_s3_file(f"raw-data/{parquet_file_name}", parquet_file_path)
                logger.info(f"Arquivo Parquet enviado para o bucket S3")
                log_message.append(f"Arquivo Parquet enviado para o bucket S3 \n")

                table_name = get_table_name_from_filename(csv_file)
                logger.info(f"Nome da tabela derivado do arquivo: {table_name}")
                log_message.append(f"Nome da tabela derivado do arquivo: {table_name} \n")

                df_prepared = prepare_dataframe_for_insert(pd.read_parquet(parquet_file_path), table_name)
                logger.info(f"DataFrame preparado para inserção na tabela '{table_name}'")
                log_message.append(f"DataFrame preparado para inserção na tabela '{table_name}' \n")

                client = get_client()
                insert_dataframe(client, 'working_data', df_prepared)
                logger.info(f"DataFrame inserido na tabela 'working_data' no ClickHouse")
                log_message.append(f"DataFrame inserido na tabela 'working_data' no ClickHouse \n")

                os.remove(local_csv_file)
                os.remove(parquet_file_path)
                logger.info(f"Arquivos temporários removidos: {local_csv_file} e {parquet_file_path}")
                log_message.append(f"Arquivos temporários removidos: {local_csv_file} e {parquet_file_path} \n")

            except Exception as e:
                logger.error(f"Erro ao processar o arquivo {csv_file}: {e}", exc_info=True)
                log_message.append(f"Erro ao processar o arquivo {csv_file}: {e} \n")
                raise RuntimeError(f"Erro ao processar o arquivo {csv_file}") from e
            
        status_code = 200
        return jsonify({"message": "Dados processados e inseridos no ClickHouse com sucesso"}), status_code

    except Exception as e:
        logger.critical(f"Erro crítico ao receber e processar dados: {e}", exc_info=True)
        log_message.append(f"Erro crítico ao receber e processar dados: {e} \n")

        status_code = 500
        return jsonify({"error": str(e)}), status_code
    
    finally:
        send_log_to_elasticsearch(log_message, "process_data_from_s3", status_code)