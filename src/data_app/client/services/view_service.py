import pandas as pd
import requests

BASE_URL = "http://flask-app:5000/view"

def fetch_data(endpoint):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados: {str(e)}")
        return pd.DataFrame()
