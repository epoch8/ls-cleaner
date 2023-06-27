from datetime import datetime, timedelta
import os
import time
import logging

from dotenv import load_dotenv
from label_studio_sdk import Client

from sdk_utils import get_tasks_iter

# Time tracker
start_time = time.time()

# Loading environments.
load_dotenv()

# Setup Logging.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Environment variables.
LS_URL = os.getenv("LS_URL", "http://url-for-labelstudio")
LS_API_KEY = os.getenv("LS_API_KEY", "TOKEN")
RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", 7))

# Formed variables
FILTER_DATETIME = (datetime.now().date() - timedelta(days=RETENTION_DAYS)).strftime("%Y-%m-%dT%H:%M:%S.%f%zZ")

# Initialize Label Studio Client.
ls = Client(url=LS_URL, api_key=LS_API_KEY)

# Get all LS projects.
ls_projects = ls.get_projects()

# Processing of each LS project.
for ls_project in ls_projects:
    # Get LS project task IDs with completed_at parameter less than FILTER_DATETIME ago.
    filters = {
        "conjunction": "and",
        "items": [
            {
                "filter": "filter:tasks:completed_at",
                "operator": "less",
                "value": FILTER_DATETIME,
                "type": "Datetime",
            },
        ],
    }
    for ls_project_tasks_page in get_tasks_iter(project=ls_project, filters=filters, only_ids=True):
        # Logging
        logging.info(f"Проект: {ls_project.get_params().get('title')}. Кол-во удаляемых задач: {len(ls_project_tasks_page)}")
        # Delete collected LS project tasks.
        logging.info(ls_project.delete_tasks(task_ids=ls_project_tasks_page))


end_time = time.time()
execution_time = end_time - start_time
logging.info(f"Время выполнения: {execution_time} секунд")
