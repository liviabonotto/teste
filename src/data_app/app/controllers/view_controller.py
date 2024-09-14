from flask import jsonify, Blueprint
from services.clickhouse_client_service import fetch_cost_data, fetch_price_data, fetch_store_regions_data, fetch_margin_data

view_blueprint = Blueprint('view', __name__)

@view_blueprint.route('/cost', methods=['GET'])
def get_cost_data():
    try:
        df = fetch_cost_data()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@view_blueprint.route('/price', methods=['GET'])
def get_price_data():
    try:
        df = fetch_price_data()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@view_blueprint.route('/margin', methods=['GET'])
def get_margin_data():
    try:
        df = fetch_margin_data()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@view_blueprint.route('/regions', methods=['GET'])
def get_store_regions_data():
    try:
        df = fetch_store_regions_data()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500