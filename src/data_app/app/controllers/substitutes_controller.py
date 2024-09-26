# from services.substitutes_service import sugerir_substituto_com_estoque
# from flask import Blueprint, jsonify, request

# substitute_blueprint = Blueprint('substitute', __name__)

# @substitute_blueprint.route('/get_product_substitute', methods=['POST'])
# def get_product_substitute():
#     product_input = request.get_json()
#     cod_prod_informado = product_input.get('cod_prod')
#     cod_loja = product_input.get('cod_loja')

#     if not cod_prod_informado or not cod_loja:
#         return jsonify({'error': 'Código do produto ou código da loja não informado'}), 400

#     substitutos = sugerir_substituto_com_estoque(cod_prod_informado, cod_loja)
    
#     if isinstance(substitutos, str):
#         return jsonify({'message': substitutos}), 200

#     result = substitutos.to_dict(orient='records')
#     return jsonify(result), 200



import logging
from flask import Blueprint, jsonify, request
from services.substitutes_service import sugerir_substituto_com_estoque

# Initialize Blueprint for substitutes
substitute_blueprint = Blueprint('substitute', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the route for getting product substitutes
@substitute_blueprint.route('/get_product_substitute', methods=['POST'])
def get_product_substitute():
    try:
        # Parse request data (Product ID and Store ID)
        product_input = request.get_json()
        cod_prod_informado = product_input.get('cod_prod')
        cod_loja = product_input.get('cod_loja')

        # Validate input data
        if not cod_prod_informado or not cod_loja:
            return jsonify({'error': 'Código do produto ou código da loja não informado'}), 400

        # Call the service function to get product substitutes
        substitutos = sugerir_substituto_com_estoque(cod_prod_informado, cod_loja)

        # Handle case where no substitutes are found
        if isinstance(substitutos, str):
            return jsonify({'message': substitutos}), 200

        # Convert the dataframe to a dictionary for JSON response
        result = substitutos.to_dict(orient='records')
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Erro no servidor: {str(e)}", exc_info=True)
        return jsonify({'error': 'Erro interno do servidor'}), 500
