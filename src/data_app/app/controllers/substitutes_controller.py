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

        # Modify this part to ensure a consistent JSON response:
        if isinstance(substitutos, str):
            return jsonify({'error': substitutos}), 404  # Return a 404 when product is not found or no substitutes

        # Handle if substitutos is a list or dataframe
        if isinstance(substitutos, list):
            result = substitutos  # Directly return the list if it's already in the correct format
        else:
            # If it's a DataFrame, convert it to a dictionary for JSON response
            result = substitutos.to_dict(orient='records')

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Erro no servidor: {str(e)}", exc_info=True)
        return jsonify({'error': 'Erro interno do servidor'}), 500
