from flask import Flask
from controllers.pipeline_controller import pipeline_blueprint
from controllers.margin_controller import margin_blueprint
from controllers.view_controller import view_blueprint
from services.clickhouse_client_service import execute_sql_script
from services.cron_service import start_cron_job 
from controllers.substitutes_controller import substitute_blueprint


app = Flask(__name__)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               


app.register_blueprint(pipeline_blueprint, url_prefix='/pipeline')
app.register_blueprint(margin_blueprint, url_prefix='/margin')
app.register_blueprint(view_blueprint, url_prefix='/view')
app.register_blueprint(substitute_blueprint)


if __name__ == '__main__':
    execute_sql_script('app/sql/create_working.sql')
    execute_sql_script('app/sql/create_view_margin.sql')
    execute_sql_script('app/sql/create_view_store_regions.sql')
    execute_sql_script('app/sql/create_view_product.sql')
    execute_sql_script('app/sql/create_view_remuneracao_gerente.sql')
    
    start_cron_job()
    app.run(host='0.0.0.0', port=5000)
    