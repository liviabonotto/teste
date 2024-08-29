import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY_ID'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
    region_name='us-east-1'
)

s3_client = session.client('s3')
bucket_name = os.getenv('BUCKET_NAME')

def create_bucket_if_not_exists(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' já existe.")
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' criado com sucesso!")
        else:
            print(f"Erro ao verificar ou criar bucket: {e}")
            raise RuntimeError(f"Erro ao criar bucket '{bucket_name}'") from e
    except Exception as e:
        print(f"Erro inesperado ao criar bucket '{bucket_name}': {e}")
        raise RuntimeError(f"Erro ao criar bucket '{bucket_name}'") from e

def list_csv_files(prefix):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        csv_files = [item['Key'] for item in response.get('Contents', []) if item['Key'].endswith('.csv')]
        return csv_files
    except ClientError as e:
        print(f"Erro ao listar arquivos no bucket '{bucket_name}': {e}")
        raise RuntimeError(f"Erro ao listar arquivos no bucket '{bucket_name}'") from e
    except Exception as e:
        print(f"Erro inesperado ao listar arquivos no bucket '{bucket_name}': {e}")
        raise RuntimeError(f"Erro ao listar arquivos no bucket '{bucket_name}'") from e

def download_csv_file(s3_key, local_path):
    try:
        s3_client.download_file(bucket_name, s3_key, local_path)
        print(f"Arquivo '{s3_key}' baixado com sucesso para '{local_path}'!")
    except FileNotFoundError as e:
        print(f"Arquivo '{local_path}' não encontrado: {e}")
        raise FileNotFoundError(f"Arquivo '{local_path}' não encontrado") from e
    except NoCredentialsError as e:
        print(f"Credenciais não encontradas: {e}")
        raise RuntimeError("Credenciais AWS não encontradas") from e
    except ClientError as e:
        print(f"Erro ao baixar o arquivo '{s3_key}' do bucket '{bucket_name}': {e}")
        raise RuntimeError(f"Erro ao baixar o arquivo '{s3_key}' do bucket '{bucket_name}'") from e
    except Exception as e:
        print(f"Erro inesperado ao baixar o arquivo '{s3_key}': {e}")
        raise RuntimeError(f"Erro ao baixar o arquivo '{s3_key}' do bucket '{bucket_name}'") from e

def upload_file(bucket_name, file_name, file_path):
    try:
        s3_client.upload_file(file_path, bucket_name, file_name)
        print(f"Arquivo '{file_name}' enviado com sucesso!")
    except FileNotFoundError as e:
        print(f"Arquivo '{file_path}' não encontrado: {e}")
        raise FileNotFoundError(f"Arquivo '{file_path}' não encontrado") from e
    except NoCredentialsError as e:
        print(f"Credenciais não encontradas: {e}")
        raise RuntimeError("Credenciais AWS não encontradas") from e
    except ClientError as e:
        print(f"Erro ao enviar arquivo para o bucket '{bucket_name}': {e}")
        raise RuntimeError(f"Erro ao enviar arquivo '{file_name}' para o bucket '{bucket_name}'") from e
    except Exception as e:
        print(f"Erro inesperado ao enviar arquivo '{file_name}' para o bucket '{bucket_name}': {e}")
        raise RuntimeError(f"Erro ao enviar arquivo '{file_name}' para o bucket '{bucket_name}'") from e

def get_file(bucket_name, file_name, download_path):
    try:
        s3_client.download_file(bucket_name, file_name, download_path)
        print(f"Busca do arquivo '{file_name}' feita com sucesso!")
    except FileNotFoundError as e:
        print(f"Diretório de destino '{download_path}' não encontrado: {e}")
        raise FileNotFoundError(f"Diretório de destino '{download_path}' não encontrado") from e
    except NoCredentialsError as e:
        print(f"Credenciais não encontradas: {e}")
        raise RuntimeError("Credenciais AWS não encontradas") from e
    except ClientError as e:
        print(f"Erro ao fazer busca do arquivo '{file_name}': {e}")
        raise RuntimeError(f"Erro ao fazer busca do arquivo '{file_name}'") from e
    except Exception as e:
        print(f"Erro inesperado ao fazer download do arquivo '{file_name}': {e}")
        raise RuntimeError(f"Erro ao fazer download do arquivo '{file_name}'") from e
