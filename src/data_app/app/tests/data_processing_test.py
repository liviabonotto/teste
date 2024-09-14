import pytest
import pandas as pd
from unittest import mock
from services.data_processing_service import process_data, prepare_dataframe_for_insert

def test_process_data_success(mocker):
    mock_data = {
        'col1': 'value1',
        'col2': 'value2'
    }

    mock_pa_write_table = mocker.patch('pyarrow.parquet.write_table')

    filename = process_data(mock_data)

    assert filename.startswith('raw_data_')
    mock_pa_write_table.assert_called_once()

def test_process_data_parquet_error(mocker):
    mock_data = {
        'col1': 'value1',
        'col2': 'value2'
    }

    mocker.patch('pyarrow.parquet.write_table', side_effect=ValueError("Erro ao escrever Parquet"))

    result = process_data(mock_data)

    assert result is None

def test_prepare_dataframe_for_insert_success():
    data = {
        'col1': ['value1'],
        'col2': ['value2']
    }
    df = pd.DataFrame(data)

    result_df = prepare_dataframe_for_insert(df, 'test-tag')

    assert 'ingestion_date' in result_df.columns
    assert 'line_data' in result_df.columns
    assert 'tag' in result_df.columns
    assert result_df['tag'].iloc[0] == 'test-tag'

def test_prepare_dataframe_for_insert_failure():
    df = mock.Mock()
    df.apply.side_effect = Exception("Erro ao preparar o DataFrame")

    result_df = prepare_dataframe_for_insert(df, "test-tag")

    assert result_df is None
