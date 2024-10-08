from services.utils_service import convert_csv_to_parquet, create_custom_temp_dir, get_csv_encoding, get_csv_separator
from services.s3_client_service import download_s3_file, list_s3_files
from services.logging_service import send_log_to_elasticsearch

import pandas as pd
import os
import logging
from itertools import combinations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def get_cross_sell_product(cod_loja, cod_prod, merged_dataset, df_estoque, df_produtos, df_preco, n=5):
    log_message = []
    status_code = 200

    try:
        cod_prod = int(cod_prod)
        cod_loja = str(cod_loja)

        # Filtra produtos relacionados ao produto fornecido
        recommendations = merged_dataset[
            (merged_dataset['prod1'] == cod_prod) | (merged_dataset['prod2'] == cod_prod)
        ].sort_values(by='frequency', ascending=False).head(n)

        # Cria a recomendação de produto (prod1 ou prod2 dependendo de qual é o produto original)
        recommendations['recommendation'] = recommendations.apply(
            lambda row: row['prod2'] if row['prod1'] == cod_prod else row['prod1'], axis=1
        )

        # Remove possíveis duplicatas para garantir que cada recomendação seja única
        recommendations = recommendations.drop_duplicates(subset=['recommendation'])

        # Faz o merge das recomendações com o dataset de estoque para verificar disponibilidade
        recommendations = recommendations.merge(
            df_estoque[['cod_prod', 'quantidade', 'cod_loja']], 
            how='left', 
            left_on='recommendation', 
            right_on='cod_prod'
        )

        # Filtra apenas recomendações que possuem estoque disponível
        in_stock_recommendations = recommendations[recommendations['quantidade'] > 0]

        # Adiciona informações de preço (preço mais recente) e descrição
        in_stock_recommendations = in_stock_recommendations.merge(
            df_produtos[['cod_prod', 'nome_abrev', 'descricao']], 
            how='left', 
            left_on='recommendation', 
            right_on='cod_prod'
        )

        # Seleciona o preço mais recente para cada produto de recomendação
        df_preco_recent = (
            df_preco.sort_values('data_fim')
            .groupby('cod_prod')
            .tail(1)[['cod_prod', 'preco']]
        )

        # Faz o merge do preço com as recomendações
        in_stock_recommendations = in_stock_recommendations.merge(
            df_preco_recent, 
            how='left', 
            left_on='recommendation', 
            right_on='cod_prod'
        )

        # Verificação final para garantir que não há duplicatas e há diversidade nos resultados
        final_recommendations = in_stock_recommendations[['recommendation', 'frequency', 'quantidade', 'cod_loja', 'nome_abrev', 'descricao', 'preco']].drop_duplicates(subset=['recommendation']).head(5)

        return final_recommendations.to_dict(orient='records')

    except Exception as e:
        logger.error(f"Erro ao buscar produtos similares: {e}", exc_info=True)
        log_message.append(f"Erro ao buscar produtos similares: {str(e)} \n")
        status_code = 500
        raise RuntimeError(f"Erro ao buscar produtos similares: {str(e)}")

    finally:
        send_log_to_elasticsearch(log_message, "get_cross_sell_product", status_code)

def transform_cross_sell_data():
    log_message = []
    status_code = 200
    try:
        prefix = os.getenv('PREFIX')
        logger.info(f"Prefixo obtido: {prefix}")
        log_message.append(f"Prefixo obtido: {prefix} \n")

        csv_files = list_s3_files(prefix)
        logger.info(f"Arquivos CSV encontrados: {csv_files}")
        log_message.append(f"Arquivos CSV encontrados: {csv_files} \n")

        df_estoque, df_vendas, df_produtos, df_preco = None, None, None, None
        
        for file_name in csv_files:
            try:
                if 'daily_stock_dataset.csv' in file_name:
                    df_estoque = load_data(file_name)
                    logger.info(f"Arquivo {file_name} carregado com sucesso.")
                    log_message.append(f"Arquivo {file_name} carregado com sucesso. \n")
                elif 'transaction_fact_v6_2024.csv' in file_name:
                    df_vendas = load_data(file_name)
                    logger.info(f"Arquivo {file_name} carregado com sucesso.")
                    log_message.append(f"Arquivo {file_name} carregado com sucesso. \n")
                elif 'sku_dataset.csv' in file_name:  
                    df_produtos = load_data(file_name)
                    logger.info(f"Arquivo {file_name} carregado com sucesso.")
                    log_message.append(f"Arquivo {file_name} carregado com sucesso. \n")
                elif 'sku_price.csv' in file_name:  
                    df_preco = load_data(file_name)
                    logger.info(f"Arquivo {file_name} carregado com sucesso.")
                    log_message.append(f"Arquivo {file_name} carregado com sucesso. \n")
            except Exception as e:
                logger.error(f"Erro ao processar o arquivo {file_name}: {e}", exc_info=True)
                log_message.append(f"Erro ao processar o arquivo {file_name}: {str(e)} \n")

        if df_estoque is None or df_vendas is None or df_produtos is None or df_preco is None:
            raise ValueError("Um ou mais datasets não foram encontrados no S3.")

        # Processamento das combinações de cross-sell
        def generate_pairs(produtos):
            if len(produtos) > 1:
                return list(combinations(produtos, 2))
            else:
                return []

        df_vendas_agrupado = df_vendas.groupby('cod_transacao')['cod_prod'].apply(list).reset_index()
        df_vendas_agrupado['pares_produtos'] = df_vendas_agrupado['cod_prod'].apply(generate_pairs)

        df_pares_explodido = df_vendas_agrupado.explode('pares_produtos').dropna(subset=['pares_produtos'])
        df_pares_explodido['prod1'] = df_pares_explodido['pares_produtos'].apply(lambda x: x[0])
        df_pares_explodido['prod2'] = df_pares_explodido['pares_produtos'].apply(lambda x: x[1])

        df_cross_sell = df_pares_explodido.groupby(['prod1', 'prod2']).size().reset_index(name='frequency')
        merged_dataset = df_cross_sell.sort_values(by='frequency', ascending=False)

        df_preco_recente = df_preco.loc[df_preco.groupby('cod_prod')['data_fim'].idxmax()].reset_index(drop=True)

        logger.info("Datasets mesclados com sucesso.")
        log_message.append("Datasets mesclados com sucesso. \n")

        status_code = 200
        
        return merged_dataset, df_vendas, df_estoque, df_produtos, df_preco_recente
    
    except Exception as e:
        logger.error(f"Erro ao transformar os dados de cross-sell: {e}", exc_info=True)
        log_message.append(f"Erro ao transformar os dados de cross-sell: {str(e)} \n")
        status_code = 500
        raise RuntimeError(f"Erro ao transformar os dados de cross-sell: {str(e)}")
    
    finally:
        send_log_to_elasticsearch(log_message, "transform_cross_sell_data", status_code)

def get_similar_products(cod_loja, cod_produto):
    logger.info("Entrou na função get_similar_products")

    status_code = 200

    try:
        merged_dataset, _, df_estoque, df_produtos, df_preco_recente = transform_cross_sell_data()  
        return get_cross_sell_product(cod_loja, cod_produto, merged_dataset, df_estoque, df_produtos, df_preco_recente)

    except Exception as e:
        logger.error(f"Erro ao processar o produto por cross-sell: {e}", exc_info=True)
        status_code = 500  
        raise RuntimeError(f"Erro ao processar o produto por cross-sell: {str(e)}")
    
    finally:
        send_log_to_elasticsearch([], "get_similar_products", status_code)
