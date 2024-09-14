import pytest
from unittest import mock
from botocore.exceptions import ClientError, NoCredentialsError
import os
from services.s3_client_service import create_bucket_if_not_exists, list_s3_files, download_s3_file, upload_s3_file

def mock_aws_credentials():
    os.environ['AWS_ACCESS_KEY_ID'] = 'mock_access_key'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'mock_secret_key'
    os.environ['AWS_SESSION_TOKEN'] = 'mock_session_token'
    os.environ['BUCKET_NAME'] = 'mock_bucket'

def test_create_bucket_if_not_exists(mocker):
    mock_aws_credentials()
    
    mock_s3_client = mocker.patch('services.s3_client_service.s3_client')
    
    mock_s3_client.head_bucket.return_value = None
    
    create_bucket_if_not_exists('mock_bucket')
    
    mock_s3_client.head_bucket.assert_called_once_with(Bucket='mock_bucket')
    mock_s3_client.create_bucket.assert_not_called()

def test_create_bucket_if_not_exists_bucket_not_found(mocker):
    mock_aws_credentials()
    
    mock_s3_client = mocker.patch('services.s3_client_service.s3_client')
    
    mock_s3_client.head_bucket.side_effect = ClientError(
        {'Error': {'Code': '404'}},
        'HeadBucket'
    )
    
    mock_s3_client.create_bucket.return_value = None
    
    create_bucket_if_not_exists('mock_bucket')
    
    mock_s3_client.create_bucket.assert_called_once_with(Bucket='mock_bucket')

def test_create_bucket_if_not_exists_client_error(mocker):
    mock_aws_credentials()
    
    mock_s3_client = mocker.patch('services.s3_client_service.s3_client')
    
    mock_s3_client.head_bucket.side_effect = ClientError(
        {'Error': {'Code': '500'}},
        'HeadBucket'
    )
    
    with pytest.raises(RuntimeError, match="Erro ao criar bucket 'mock_bucket'"):
        create_bucket_if_not_exists('mock_bucket')

def test_list_s3_files_success(mocker):
    mock_aws_credentials()
    
    mock_s3_client = mocker.patch('services.s3_client_service.s3_client')
    
    mock_s3_client.list_objects_v2.return_value = {
        'Contents': [
            {'Key': 'file1.csv'},
            {'Key': 'file2.txt'}
        ]
    }
    
    files = list_s3_files('dataset')
    
    assert files == ['file1.csv']
    mock_s3_client.list_objects_v2.assert_called_once_with(Bucket='lake-vizion', Prefix='dataset')

def test_download_s3_file_file_not_found(mocker):
    mock_aws_credentials()
    
    mock_s3_client = mocker.patch('services.s3_client_service.s3_client')
    
    mock_s3_client.download_file.side_effect = FileNotFoundError("File not found")
    
    with pytest.raises(FileNotFoundError, match="Arquivo 'local_path' não encontrado"):
        download_s3_file('s3_key', 'local_path')

def test_download_s3_file_no_credentials(mocker):
    mock_aws_credentials()
    
    mock_s3_client = mocker.patch('services.s3_client_service.s3_client')
    
    mock_s3_client.download_file.side_effect = NoCredentialsError()
    
    with pytest.raises(RuntimeError, match="Credenciais AWS não encontradas"):
        download_s3_file('s3_key', 'local_path')

def test_upload_s3_file_success(mocker):
    mock_aws_credentials()
    
    mock_s3_client = mocker.patch('services.s3_client_service.s3_client')
    
    mock_s3_client.upload_file.return_value = None
    
    upload_s3_file('s3_key', 'file_name')
    
    mock_s3_client.upload_file.assert_called_once_with('file_name', 'lake-vizion', 's3_key')

def test_upload_s3_file_file_not_found(mocker):
    mock_aws_credentials()
    
    mock_s3_client = mocker.patch('services.s3_client_service.s3_client')
    
    mock_s3_client.upload_file.side_effect = FileNotFoundError("File not found")
    
    with pytest.raises(FileNotFoundError, match="Arquivo 'file_name' não encontrado"):
        upload_s3_file('s3_key', 'file_name')

def test_upload_s3_file_no_credentials(mocker):
    mock_aws_credentials()
    
    mock_s3_client = mocker.patch('services.s3_client_service.s3_client')
    
    mock_s3_client.upload_file.side_effect = NoCredentialsError()
    
    with pytest.raises(RuntimeError, match="Credenciais AWS não encontradas"):
        upload_s3_file('s3_key', 'file_name')
