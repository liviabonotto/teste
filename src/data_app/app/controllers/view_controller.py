from flask import jsonify, Blueprint
from services.clickhouse_client_service import fetch_store_regions_data

view_blueprint = Blueprint('view', __name__)
    
@view_blueprint.route('/regions', methods=['GET'])
def get_store_regions_data():
    try:
        df = fetch_store_regions_data()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500