
from services.profit_margin import get_similar_product_by_margin
from services.pipeline_service import process_data_from_s3
from flask import Blueprint, jsonify, request


pipeline_blueprint = Blueprint('pipeline', __name__)

@pipeline_blueprint.route('/s3', methods=['GET'])
def data_pipeline_s3():
    process_data_from_s3()
    return jsonify({"message": "Dados recebidos, armazenados e processados com sucesso!"}), 200

@pipeline_blueprint.route('/get_similar_product_by_margin', methods=['POST'])
def get_product_by_margin():
    data = request.get_json()
    input_descricao = data.get('descricao')

    if not input_descricao:
        return jsonify({"error": "Descrição do produto não fornecida."}), 400

    produtos_similares = get_similar_product_by_margin(input_descricao)

    result = produtos_similares.to_dict(orient='records')
    return jsonify(result), 200
