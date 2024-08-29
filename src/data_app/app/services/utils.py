import os
import pandas as pd
from pathlib import Path

def create_custom_temp_dir():
    temp_dir = "temporary"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir

def convert_csv_to_parquet(csv_file_path, parquet_file_path=None, encoding='latin1'):
    df = pd.read_csv(csv_file_path, encoding=encoding)

    if parquet_file_path is None:
        parquet_file_path = csv_file_path.replace('.csv', '.parquet')

    df.to_parquet(parquet_file_path)

    return parquet_file_path

def get_table_name_from_filename(filename):
    basename = os.path.basename(filename)
    table_name = os.path.splitext(basename)[0]
    return table_name