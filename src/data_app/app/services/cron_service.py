import time
import threading
import logging

from croniter import croniter
from datetime import datetime
from services.pipeline_service import process_data_from_s3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cron_job():
    cron_expression = "59 23 * * *"
    base_time = datetime.now()

    while True:
        cron = croniter(cron_expression, base_time)
        next_run = cron.get_next(datetime)
        sleep_time = (next_run - datetime.now()).total_seconds()

        if sleep_time <= 0:
            sleep_time = 1 

        next_run_time = next_run.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Cron irá rodar em {sleep_time:.2f} segundos. Próxima execução agendada para {next_run_time}.")
        
        time.sleep(sleep_time)

        process_data_from_s3()

def start_cron_job():
    cron_thread = threading.Thread(target=cron_job)
    cron_thread.daemon = True 
    cron_thread.start()
