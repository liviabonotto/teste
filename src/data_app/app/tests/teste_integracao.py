import pytest
from moto import mock_s3
import boto3
from app import app
from services.s3_client import upload_file_to_s3

@pytest.fixture
def mock_s3_bucket():
    with mock_s3():
        s3 = boto3.client('s3')
        s3.create_bucket(Bucket='my-test-bucket')
        yield s3

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_pipeline_route_with_s3(client, mock_s3_bucket):
    upload_file_to_s3('testfile.txt', 'my-test-bucket', 'testfile.txt')
    response = client.get('/pipeline')
    assert response.status_code == 200
    assert b'Pipeline execution successful' in response.data

    objects = mock_s3_bucket.list_objects_v2(Bucket='my-test-bucket')
    assert 'Contents' in objects
    assert any(obj['Key'] == 'testfile.txt' for obj in objects['Contents'])
