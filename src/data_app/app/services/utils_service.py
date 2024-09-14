import os
import chardet
import pandas as pd
from collections import Counter

def create_custom_temp_dir():
    temp_dir = "temporary"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir


def get_csv_encoding(csv_file_path):
    with open(csv_file_path, 'rb') as f:
        rawdata = f.read(10000)
    return chardet.detect(rawdata)['encoding']

def get_csv_separator(csv_file_path, encoding):
    seps = [',', ';', '\t', '|']

    with open(csv_file_path, 'r', encoding=encoding) as f:
        first_line = f.readline()
    count = Counter({sep:first_line.count(sep) for sep in seps})
    seps_count = count.most_common(1)[0][0]
    return seps_count

def convert_csv_to_parquet(csv_file_path, encoding, sep, parquet_file_path=None):
    df = pd.read_csv(csv_file_path, encoding=encoding , sep=sep)

    if parquet_file_path is None:
        parquet_file_path = csv_file_path.replace('.csv', '.parquet')

    df.to_parquet(parquet_file_path)
    parquet_file_name = os.path.basename(parquet_file_path)

    return parquet_file_path, parquet_file_name

def get_table_name_from_filename(filename):
    basename = os.path.basename(filename)
    table_name = os.path.splitext(basename)[0]
    return table_name