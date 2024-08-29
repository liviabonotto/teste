from flask import Flask
from controllers.ingestion_controller import ingestion_blueprint
from services.clickhouse_client_service import execute_sql_script

app = Flask(__name__)


app.register_blueprint(ingestion_blueprint, url_prefix='/ingestion')

if __name__ == '__main__':
    execute_sql_script('sql/create_working.sql')
    execute_sql_script('sql/create_view_price.sql')
    app.run(host='0.0.0.0', port=5000)