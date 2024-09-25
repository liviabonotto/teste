from services.pipeline_service import process_data_from_s3
from flask import Blueprint, jsonify

import logging


pipeline_blueprint = Blueprint('pipeline', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pipeline_blueprint.route('/s3', methods=['GET'])
def data_pipeline_s3():
    process_data_from_s3()
    return jsonify({"message": "Dados recebidos, armazenados e processados com sucesso!"}), 200
