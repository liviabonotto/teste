# import os
# import pandas as pd
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import TfidfVectorizer
# from services.s3_client_service import download_s3_file, list_s3_files
# from services.utils_service import convert_csv_to_parquet, create_custom_temp_dir, get_csv_encoding, get_csv_separator
# from services.logging_service import send_log_to_elasticsearch
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def load_data(file_name):
#     try:
#         temp_dir = create_custom_temp_dir()
#         local_csv_path = os.path.join(temp_dir, os.path.basename(file_name))
        
#         download_s3_file(file_name, local_csv_path)
#         encoding = get_csv_encoding(local_csv_path)
#         sep = get_csv_separator(local_csv_path, encoding)
        
#         parquet_file_path, parquet_file_name = convert_csv_to_parquet(local_csv_path, encoding, sep)
#         return pd.read_parquet(parquet_file_path)
    
#     except Exception as e:
#         logger.error(f"Erro ao carregar os dados do arquivo {file_name}: {e}", exc_info=True)
#         raise RuntimeError(f"Erro ao carregar os dados do arquivo {file_name}: {str(e)}")

# def sugerir_substituto_com_estoque(cod_prod_informado, cod_loja):
#     log_message = []

#     try:
#         # Carregar datasets do S3
#         prefix = os.getenv('PREFIX')
#         logger.info(f"Prefixo obtido: {prefix}")
#         log_message.append(f"Prefixo obtido: {prefix} \n")

#         csv_files = list_s3_files(prefix)
#         logger.info(f"Arquivos CSV encontrados: {csv_files}")
#         log_message.append(f"Arquivos CSV encontrados: {csv_files} \n")

#         df_produtos, df_estoque = None, None
        
#         for file_name in csv_files:
#             try:
#                 if 'sku_dataset.csv' in file_name:
#                     df_produtos = load_data(file_name)
#                     logger.info(f"Arquivo {file_name} carregado com sucesso.")
#                     log_message.append(f"Arquivo {file_name} carregado com sucesso. \n")
#                 elif 'daily_stock_dataset.csv' in file_name:
#                     df_estoque = load_data(file_name)
#                     logger.info(f"Arquivo {file_name} carregado com sucesso.")
#                     log_message.append(f"Arquivo {file_name} carregado com sucesso. \n")
#             except Exception as e:
#                 logger.error(f"Erro ao processar o arquivo {file_name}: {e}", exc_info=True)
#                 log_message.append(f"Erro ao processar o arquivo {file_name}: {str(e)} \n")

#         if df_produtos is None or df_estoque is None:
#             raise ValueError("Um ou mais datasets não foram encontrados no S3.")
        
#         # Filtrar o produto informado
#         produto_info = df_produtos[df_produtos['cod_prod'] == cod_prod_informado]

#         if produto_info.empty:
#             logger.warning(f"Produto com código {cod_prod_informado} não encontrado.")
#             log_message.append(f"Produto com código {cod_prod_informado} não encontrado. \n")
#             return "Produto não encontrado"

#         # Extrair informações relevantes do produto informado
#         categoria = produto_info['categoria'].values[0]
#         subcategoria = produto_info['sub_categoria'].values[0]
#         valor_ref = pd.to_numeric(produto_info['conteudo_valor'], errors='coerce').values[0]
#         conteudo_medida_ref = produto_info['conteudo_medida'].values[0]
#         descricao = produto_info['descricao'].values[0]

#         if np.isnan(valor_ref):
#             logger.warning(f"Conteúdo valor do produto {cod_prod_informado} não é numérico ou está faltando.")
#             log_message.append(f"Conteúdo valor do produto {cod_prod_informado} não é numérico ou está faltando. \n")
#             return "Conteúdo valor não é numérico ou está faltando"

#         logger.info(f"Produto {cod_prod_informado} encontrado: {descricao}, categoria: {categoria}, subcategoria: {subcategoria}.")
#         log_message.append(f"Produto {cod_prod_informado} encontrado com sucesso. \n")

#         # Filtrar produtos da mesma categoria, subcategoria e com valor/medida semelhantes
#         produtos_potenciais = df_produtos[
#             (df_produtos['categoria'] == categoria) &
#             (df_produtos['sub_categoria'] == subcategoria) &
#             pd.to_numeric(df_produtos['conteudo_valor'], errors='coerce').between(valor_ref * 0.9, valor_ref * 1.1) &
#             (df_produtos['conteudo_medida'] == conteudo_medida_ref) &
#             (df_produtos['cod_prod'] != cod_prod_informado)
#         ].copy()

#         if produtos_potenciais.empty:
#             logger.info(f"Nenhum produto substituto encontrado para o produto {cod_prod_informado}.")
#             log_message.append(f"Nenhum produto substituto encontrado para o produto {cod_prod_informado}. \n")
#             return "Nenhum produto substituto encontrado"

#         # Remover stop words da descrição
#         def remove_stop_words(text):
#             stop_words = set(["de", "o", "a", "e", "que", "do", "da", "em", "um", "para", "com", "não", "uma", "os", "no"])
#             words = text.lower().split()
#             return ' '.join([word for word in words if word not in stop_words])

#         descricoes = [descricao] + produtos_potenciais['descricao'].fillna("").tolist()
#         descricoes_sem_stopwords = [remove_stop_words(desc) for desc in descricoes]

#         # Criar uma matriz TF-IDF para calcular similaridade
#         vectorizer = TfidfVectorizer()
#         tfidf_matrix = vectorizer.fit_transform(descricoes_sem_stopwords)
#         similaridade = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

#         # Adicionar a similaridade ao dataframe de produtos potenciais
#         produtos_potenciais['similaridade'] = similaridade

#         # Ordenar produtos pela similaridade
#         produtos_potenciais = produtos_potenciais.sort_values(by='similaridade', ascending=False)

#         # Verificar estoque para os produtos potenciais
#         produtos_em_estoque = pd.DataFrame()
#         for _, produto_substituto in produtos_potenciais.iterrows():
#             cod_produto_substituto = produto_substituto['cod_prod']
#             estoque_produto = df_estoque[
#                 (df_estoque['cod_loja'] == cod_loja) & 
#                 (df_estoque['cod_prod'] == cod_produto_substituto)
#             ]

#             if not estoque_produto.empty and estoque_produto['quantidade'].values[0] > 0:
#                 produtos_em_estoque = pd.concat([produtos_em_estoque, produto_substituto.to_frame().T])

#             if len(produtos_em_estoque) >= 3:
#                 break

#         if not produtos_em_estoque.empty:
#             logger.info(f"Produtos substitutos encontrados para o produto {cod_prod_informado}.")
#             log_message.append(f"Produtos substitutos encontrados para o produto {cod_prod_informado}. \n")
#             status_code = 200
#             return produtos_em_estoque[['cod_prod', 'nome_completo', 'conteudo_valor', 'conteudo_medida', 'descricao', 'similaridade']]
#         else:
#             logger.info(f"Nenhum produto substituto disponível em estoque para o produto {cod_prod_informado}.")
#             log_message.append(f"Nenhum produto substituto disponível em estoque para o produto {cod_prod_informado}. \n")
#             status_code = 200
#             return "Nenhum produto substituto disponível em estoque"

#     except Exception as e:
#         logger.error(f"Erro ao sugerir substitutos: {e}", exc_info=True)
#         log_message.append(f"Erro ao sugerir substitutos: {str(e)} \n")
#         status_code = 500
#         raise RuntimeError(f"Erro ao sugerir substitutos: {str(e)}")
    
#     finally:
#         send_log_to_elasticsearch(log_message, "get_product_substitute", status_code)



import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from services.s3_client_service import download_s3_file, list_s3_files
from services.utils_service import convert_csv_to_parquet, create_custom_temp_dir, get_csv_encoding, get_csv_separator
from services.logging_service import send_log_to_elasticsearch
import logging

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

def sugerir_substituto_com_estoque(cod_prod_informado, cod_loja):
    log_message = []
    status_code = 500  # Inicializa status_code com 500, padrão para erros

    try:
        # Carregar datasets do S3
        prefix = os.getenv('PREFIX')
        if not prefix:
            raise ValueError("Prefixo do S3 não foi definido.")
        
        logger.info(f"Prefixo obtido: {prefix}")
        log_message.append(f"Prefixo obtido: {prefix} \n")

        csv_files = list_s3_files(prefix)
        logger.info(f"Arquivos CSV encontrados: {csv_files}")
        log_message.append(f"Arquivos CSV encontrados: {csv_files} \n")

        df_produtos, df_estoque = None, None
        
        # Carregar os datasets de produtos e estoque
        for file_name in csv_files:
            try:
                if 'sku_dataset.csv' in file_name:
                    df_produtos = load_data(file_name)
                    logger.info(f"Arquivo {file_name} carregado com sucesso.")
                    log_message.append(f"Arquivo {file_name} carregado com sucesso. \n")
                elif 'daily_stock_dataset.csv' in file_name:
                    df_estoque = load_data(file_name)
                    logger.info(f"Arquivo {file_name} carregado com sucesso.")
                    log_message.append(f"Arquivo {file_name} carregado com sucesso. \n")
            except Exception as e:
                logger.error(f"Erro ao processar o arquivo {file_name}: {e}", exc_info=True)
                log_message.append(f"Erro ao processar o arquivo {file_name}: {str(e)} \n")

        if df_produtos is None or df_estoque is None:
            raise ValueError("Um ou mais datasets não foram encontrados no S3.")
        
        # Filtrar o produto informado
        produto_info = df_produtos[df_produtos['cod_prod'] == cod_prod_informado]

        if produto_info.empty:
            logger.warning(f"Produto com código {cod_prod_informado} não encontrado.")
            log_message.append(f"Produto com código {cod_prod_informado} não encontrado. \n")
            status_code = 404  # Produto não encontrado
            return "Produto não encontrado"

        # Extrair informações relevantes do produto informado
        categoria = produto_info['categoria'].values[0]
        subcategoria = produto_info['sub_categoria'].values[0]
        valor_ref = pd.to_numeric(produto_info['conteudo_valor'], errors='coerce').values[0]
        conteudo_medida_ref = produto_info['conteudo_medida'].values[0]
        descricao = produto_info['descricao'].values[0]

        if np.isnan(valor_ref):
            logger.warning(f"Conteúdo valor do produto {cod_prod_informado} não é numérico ou está faltando.")
            log_message.append(f"Conteúdo valor do produto {cod_prod_informado} não é numérico ou está faltando. \n")
            status_code = 400  # Conteúdo valor inválido
            return "Conteúdo valor não é numérico ou está faltando"

        logger.info(f"Produto {cod_prod_informado} encontrado: {descricao}, categoria: {categoria}, subcategoria: {subcategoria}.")
        log_message.append(f"Produto {cod_prod_informado} encontrado com sucesso. \n")

        # Filtrar produtos da mesma categoria, subcategoria e com valor/medida semelhantes
        produtos_potenciais = df_produtos[
            (df_produtos['categoria'] == categoria) &
            (df_produtos['sub_categoria'] == subcategoria) &
            pd.to_numeric(df_produtos['conteudo_valor'], errors='coerce').between(valor_ref * 0.9, valor_ref * 1.1) &
            (df_produtos['conteudo_medida'] == conteudo_medida_ref) &
            (df_produtos['cod_prod'] != cod_prod_informado)
        ].copy()

        if produtos_potenciais.empty:
            logger.info(f"Nenhum produto substituto encontrado para o produto {cod_prod_informado}.")
            log_message.append(f"Nenhum produto substituto encontrado para o produto {cod_prod_informado}. \n")
            status_code = 404
            return "Nenhum produto substituto encontrado"

        # Remover stop words da descrição
        def remove_stop_words(text):
            stop_words = set(["de", "o", "a", "e", "que", "do", "da", "em", "um", "para", "com", "não", "uma", "os", "no"])
            words = text.lower().split()
            return ' '.join([word for word in words if word not in stop_words])

        descricoes = [descricao] + produtos_potenciais['descricao'].fillna("").tolist()
        descricoes_sem_stopwords = [remove_stop_words(desc) for desc in descricoes]

        # Criar uma matriz TF-IDF para calcular similaridade
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(descricoes_sem_stopwords)
        similaridade = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        # Adicionar a similaridade ao dataframe de produtos potenciais
        produtos_potenciais['similaridade'] = similaridade

        # Ordenar produtos pela similaridade
        produtos_potenciais = produtos_potenciais.sort_values(by='similaridade', ascending=False)

        # Verificar estoque para os produtos potenciais
        produtos_em_estoque = pd.DataFrame()
        for _, produto_substituto in produtos_potenciais.iterrows():
            cod_produto_substituto = produto_substituto['cod_prod']
            estoque_produto = df_estoque[
                (df_estoque['cod_loja'] == cod_loja) & 
                (df_estoque['cod_prod'] == cod_produto_substituto)
            ]

            if not estoque_produto.empty and estoque_produto['quantidade'].values[0] > 0:
                # Mock `preco` and `margem_lucro_bruto`
                produto_substituto['preco'] = 50.00  # Mocked price
                produto_substituto['margem_lucro_bruto'] = 25.0  # Mocked profit margin
                produtos_em_estoque = pd.concat([produtos_em_estoque, produto_substituto.to_frame().T])

            if len(produtos_em_estoque) >= 3:
                break

        # Return the structure including `preco` and `margem_lucro_bruto` (mocked values)
        if not produtos_em_estoque.empty:
            logger.info(f"Produtos substitutos encontrados para o produto {cod_prod_informado}.")
            log_message.append(f"Produtos substitutos encontrados para o produto {cod_prod_informado}. \n")
            status_code = 200
            
            # Format the output to match the required structure
            resultado = []
            for _, produto in produtos_em_estoque.iterrows():
                resultado.append({
                    "nome": produto['nome_completo'],  # Name of the product
                    "id": produto['cod_prod'],         # Product ID
                    "descricao": produto['descricao'], # Product description
                    "preco": "R$ 50,00",               # Mocked price
                    "margem": "25%"                    # Mocked margin
                })
            
            return resultado
        else:
            logger.info(f"Nenhum produto substituto disponível em estoque para o produto {cod_prod_informado}.")
            log_message.append(f"Nenhum produto substituto disponível em estoque para o produto {cod_prod_informado}. \n")
            status_code = 200
            return "Nenhum produto substituto disponível em estoque"


    except Exception as e:
        logger.error(f"Erro ao sugerir substitutos: {e}", exc_info=True)
        log_message.append(f"Erro ao sugerir substitutos: {str(e)} \n")
        status_code = 500
        raise RuntimeError(f"Erro ao sugerir substitutos: {str(e)}")
    
    finally:
        send_log_to_elasticsearch(log_message, "get_product_substitute", status_code)
