from services.substitutes_service import sugerir_substituto_com_estoque
from flask import Blueprint, jsonify, request

substitute_blueprint = Blueprint('substitute', __name__)

@substitute_blueprint.route('/get_product_substitute', methods=['POST'])
def get_product_substitute():
    product_input = request.get_json()
    cod_prod_informado = product_input.get('cod_prod')
    cod_loja = product_input.get('cod_loja')

    if not cod_prod_informado or not cod_loja:
        return jsonify({'error': 'Código do produto ou código da loja não informado'}), 400

    substitutos = sugerir_substituto_com_estoque(cod_prod_informado, cod_loja)
    
    if isinstance(substitutos, str):
        return jsonify({'message': substitutos}), 200

    result = substitutos.to_dict(orient='records')
    return jsonify(result), 200
