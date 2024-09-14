import pytest
import pandas as pd
import os
from unittest import mock
from services.utils_service import create_custom_temp_dir, convert_csv_to_parquet, get_table_name_from_filename

def test_create_custom_temp_dir(mocker):
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = False 

    mock_makedirs = mocker.patch('os.makedirs')

    result = create_custom_temp_dir()

    mock_makedirs.assert_called_once_with('temporary')

    assert result == 'temporary'

def test_create_custom_temp_dir_already_exists(mocker):
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = True

    mock_makedirs = mocker.patch('os.makedirs')

    result = create_custom_temp_dir()

    mock_makedirs.assert_not_called()

    assert result == 'temporary'

def test_convert_csv_to_parquet(mocker):
    csv_file_path = 'example.csv'
    parquet_file_path = 'example.parquet'

    mock_to_parquet = mocker.patch('pandas.DataFrame.to_parquet')

    mock_df = mocker.patch('pandas.read_csv', return_value=pd.DataFrame({'col1': [1, 2]}))

    result_path, result_name = convert_csv_to_parquet(csv_file_path)

    mock_to_parquet.assert_called_once_with(parquet_file_path)

    assert result_path == 'example.parquet'
    assert result_name == 'example.parquet'

def test_convert_csv_to_parquet_with_custom_path(mocker):
    csv_file_path = 'example.csv'
    parquet_file_path = 'custom_path.parquet'

    mock_to_parquet = mocker.patch('pandas.DataFrame.to_parquet')

    mock_df = mocker.patch('pandas.read_csv', return_value=pd.DataFrame({'col1': [1, 2]}))

    result_path, result_name = convert_csv_to_parquet(csv_file_path, parquet_file_path)

    mock_to_parquet.assert_called_once_with(parquet_file_path)

    assert result_path == 'custom_path.parquet'
    assert result_name == 'custom_path.parquet'

def test_get_table_name_from_filename():
    filename = 'table_name.csv'

    table_name = get_table_name_from_filename(filename)

    assert table_name == 'table_name'

def test_get_table_name_from_filename_without_extension():
    filename = 'table_name'

    table_name = get_table_name_from_filename(filename)

    assert table_name == 'table_name'
