
from services.clickhouse_client_service import get_product_brands, get_product_categories, get_product_subcategories
from services.profit_margin import get_similar_product_by_margin_from_bronze, get_similar_product_by_margin_from_silver
from flask import Blueprint, jsonify, request

margin_blueprint = Blueprint('margin', __name__)

@margin_blueprint.route('/get_similar_product_by_margin_bronze', methods=['POST'])
def get_product_by_margin_bronze():
    product_input = request.get_json()

    produtos_similares = get_similar_product_by_margin_from_bronze(product_input, product_input['preco_max'], product_input['preco_min'])

    result = produtos_similares.to_dict(orient='records')
    return jsonify(result), 200

@margin_blueprint.route('/get_similar_product_by_margin_silver', methods=['POST'])
def get_product_by_margin_silver():
    product_input = request.get_json()

    produtos_similares = get_similar_product_by_margin_from_silver(product_input)

    result = produtos_similares.to_dict(orient='records')
    return jsonify(result), 200

@margin_blueprint.route('/get_product_categories', methods=['GET'])
def get_categories():
    try:
        categories = get_product_categories()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@margin_blueprint.route('/get_product_subcategories', methods=['GET'])
def get_subcategories():
    try:
        subcategories = get_product_subcategories()
        return jsonify(subcategories), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@margin_blueprint.route('/get_product_brands', methods=['GET'])
def get_brands():
    try:
        brands = get_product_brands()
        return jsonify(brands), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500