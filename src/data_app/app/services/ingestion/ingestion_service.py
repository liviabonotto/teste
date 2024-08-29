from flask import Flask, request, jsonify
from services.clickhouse_client_service import get_client, insert_dataframe
from services.data_processing import prepare_dataframe_for_insert
from services.utils import create_custom_temp_dir, convert_csv_to_parquet, get_table_name_from_filename
from services.s3_client_service import list_csv_files, download_csv_file
import os
import pandas as pd

app = Flask(__name__)

def receive_data():
    try:
        prefix = os.getenv('PREFIX')
        print(f"Prefixo obtido: {prefix}")

        csv_files = list_csv_files(prefix)
        print(f"Arquivos CSV encontrados: {csv_files}")

        if not csv_files:
            print("Nenhum arquivo CSV encontrado no bucket S3")
            return jsonify({"error": "Nenhum arquivo CSV encontrado no bucket S3"}), 400

        temp_dir = create_custom_temp_dir()
        print(f"Diretório temporário criado: {temp_dir}")

        for csv_file in csv_files:
            try:
                local_csv_file = os.path.join(temp_dir, os.path.basename(csv_file))
                print(f"Baixando arquivo CSV: {csv_file} para {local_csv_file}")
                download_csv_file(csv_file, local_csv_file)

                parquet_file = convert_csv_to_parquet(local_csv_file)
                print(f"Arquivo CSV convertido para Parquet: {parquet_file}")

                table_name = get_table_name_from_filename(csv_file)
                print(f"Nome da tabela derivado do arquivo: {table_name}")

                df_prepared = prepare_dataframe_for_insert(pd.read_parquet(parquet_file), table_name)
                print(f"DataFrame preparado para inserção na tabela '{table_name}'")

                client = get_client()
                insert_dataframe(client, 'working_data', df_prepared)
                print(f"DataFrame inserido na tabela 'working_data' no ClickHouse")

                os.remove(local_csv_file)
                os.remove(parquet_file)
                print(f"Arquivos temporários removidos: {local_csv_file} e {parquet_file}")

            except Exception as e:
                print(f"Erro ao processar o arquivo {csv_file}: {e}")
                raise RuntimeError(f"Erro ao processar o arquivo {csv_file}") from e

        return jsonify({"message": "Dados processados e inseridos no ClickHouse com sucesso"}), 200

    except Exception as e:
        print(f"Erro crítico ao receber e processar dados: {e}")
        return jsonify({"error": str(e)}), 500