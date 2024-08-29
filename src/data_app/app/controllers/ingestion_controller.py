from services.ingestion.ingestion_service import receive_data
from flask import Blueprint, jsonify

ingestion_blueprint = Blueprint('pipeline', __name__)

@ingestion_blueprint.route('/pipeline', methods=['GET'])
def margin_pipeline():
    receive_data()
    return jsonify({"message": "Dados recebidos, armazenados e processados com sucesso!"}), 200