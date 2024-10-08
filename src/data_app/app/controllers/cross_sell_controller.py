from flask import Blueprint, jsonify, request
from services.cross_sell import get_similar_products

import logging


cross_sell_blueprint = Blueprint('cross-sell', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@cross_sell_blueprint.route('/get_similar_products', methods=['POST'])
def similar_products():
    try:
        input_cod_prod = request.json.get('cod_prod')
        input_cod_loja = request.json.get('cod_loja')

        cross_sell = get_similar_products(input_cod_loja, input_cod_prod)

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
