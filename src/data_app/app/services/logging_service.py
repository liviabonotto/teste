from elasticsearch import Elasticsearch
from datetime import datetime
from flask import request

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

index_name_prefix = "system-log"

def connect_to_elasticsearch_client():
    try:
        es = Elasticsearch(["http://elasticsearch:9200"])
        logger.info(f"Conexão com o Elasticsearch estabelecida com sucesso.")
        logger.info(es.info())
        return es
    except Exception as e:
        logger.error(f"Erro ao conectar com o Elasticsearch: {str(e)}")
        return None

def send_log_to_elasticsearch(log_message, object_name, status_code):
    try:
        es = connect_to_elasticsearch_client()

        current_date = datetime.now().strftime("%Y-%m-%d")
        index_name = f"{index_name_prefix}-{current_date}"
        client_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        http_method = request.method
        request_url = request.url

        if status_code == 200:
            success = True
        else:
            success = False

        log_entry = {
            "timestamp": datetime.now(),
            "message": log_message,
            "object_name": object_name,
            "client_ip": client_ip,
            "user_agent": user_agent,
            "http_method": http_method,
            "request_url": request_url,
            "status_code": status_code,
            "success": success
        }

        logger.info(f"Enviando log para o Elasticsearch: {log_entry}")

        res = es.index(index=index_name, body=log_entry)
        logger.info(f"Log enviado para o Elasticsearch: {res}")

        return res

    except Exception as e:
        print(f"Erro ao enviar log para Elasticsearch: {str(e)}")
        return None
