from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv

import os
import boto3
import logging

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY_ID'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
    region_name='us-east-1'
)

s3_client = session.client('s3')
bucket_name = os.getenv('BUCKET_NAME')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_bucket_if_not_exists(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        logger.info(f"Bucket '{bucket_name}' já existe.")
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            s3_client.create_bucket(Bucket=bucket_name)
            logger.info(f"Bucket '{bucket_name}' criado com sucesso!")
        else:
            logger.error(f"Erro ao verificar ou criar bucket: {e}", exc_info=True)
            raise RuntimeError(f"Erro ao criar bucket '{bucket_name}'") from e
    except Exception as e:
        logger.error(f"Erro inesperado ao criar bucket '{bucket_name}': {e}", exc_info=True)
        raise RuntimeError(f"Erro ao criar bucket '{bucket_name}'") from e

def list_s3_files(prefix):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        csv_files = [item['Key'] for item in response.get('Contents', []) if item['Key'].endswith('.csv')]
        logger.info(f"Arquivos CSV encontrados: {csv_files}")
        return csv_files
    except ClientError as e:
        logger.error(f"Erro ao listar arquivos no bucket '{bucket_name}': {e}", exc_info=True)
        raise RuntimeError(f"Erro ao listar arquivos no bucket '{bucket_name}'") from e
    except Exception as e:
        logger.error(f"Erro inesperado ao listar arquivos no bucket '{bucket_name}': {e}", exc_info=True)
        raise RuntimeError(f"Erro ao listar arquivos no bucket '{bucket_name}'") from e

def download_s3_file(s3_key, local_path):
    try:
        s3_client.download_file(bucket_name, s3_key, local_path)
        logger.info(f"Arquivo '{s3_key}' baixado com sucesso para '{local_path}'!")
    except FileNotFoundError as e:
        logger.error(f"Arquivo '{local_path}' não encontrado: {e}", exc_info=True)
        raise FileNotFoundError(f"Arquivo '{local_path}' não encontrado") from e
    except NoCredentialsError as e:
        logger.error(f"Credenciais não encontradas: {e}", exc_info=True)
        raise RuntimeError("Credenciais AWS não encontradas") from e
    except ClientError as e:
        logger.error(f"Erro ao baixar o arquivo '{s3_key}' do bucket '{bucket_name}': {e}", exc_info=True)
        raise RuntimeError(f"Erro ao baixar o arquivo '{s3_key}' do bucket '{bucket_name}'") from e
    except Exception as e:
        logger.error(f"Erro inesperado ao baixar o arquivo '{s3_key}': {e}", exc_info=True)
        raise RuntimeError(f"Erro ao baixar o arquivo '{s3_key}' do bucket '{bucket_name}'") from e

def upload_s3_file(s3_key, file_name):
    try:
        s3_client.upload_file(file_name, bucket_name, s3_key)
        logger.info(f"Arquivo '{file_name}' enviado com sucesso!")
    except FileNotFoundError as e:
        logger.error(f"Arquivo '{file_name}' não encontrado: {e}", exc_info=True)
        raise FileNotFoundError(f"Arquivo '{file_name}' não encontrado") from e
    except NoCredentialsError as e:
        logger.error(f"Credenciais não encontradas: {e}", exc_info=True)
        raise RuntimeError("Credenciais AWS não encontradas") from e
    except ClientError as e:
        logger.error(f"Erro ao enviar arquivo para o bucket '{bucket_name}': {e}", exc_info=True)
        raise RuntimeError(f"Erro ao enviar arquivo '{file_name}' para o bucket '{bucket_name}'") from e
    except Exception as e:
        logger.error(f"Erro inesperado ao enviar arquivo '{file_name}' para o bucket '{bucket_name}': {e}", exc_info=True)
        raise RuntimeError(f"Erro ao enviar arquivo '{file_name}' para o bucket '{bucket_name}'") from e