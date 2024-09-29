from services.cross_sell import get_similar_products_by
from services.pipeline_service import process_data_from_s3
from flask import Blueprint, jsonify, request

import logging


pipeline_blueprint = Blueprint('pipeline', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pipeline_blueprint.route('/s3', methods=['GET'])
def data_pipeline_s3():
    process_data_from_s3()
    return jsonify({"message": "Dados recebidos, armazenados e processados com sucesso!"}), 200

@pipeline_blueprint.route('/get_similar_products', methods=['POST'])
def similar_products():
    try:
        input_cod_prod = request.json.get('cod_prod')
        input_cod_loja = request.json.get('cod_loja')

        cross_sell = get_similar_products_by(input_cod_loja, input_cod_prod)

        formatted_cross_sell = []
        for product in cross_sell:
            formatted_cross_sell.append({
                "recommendation": product.get("recommendation"),  
                "frequency": product.get("frequency"),
                "quantidade": product.get("quantidade"),
                "preco": product.get("preco"),
                "nome": product.get("nome_abrev"),
                "descricao": product.get("descricao"),
                "cod_loja": input_cod_loja  
            })

        result = {
            "status": 200,
            "data": formatted_cross_sell
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "status": 500,
            "error": str(e)  
        }), 500
