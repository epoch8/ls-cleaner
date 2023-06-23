import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from label_studio_sdk import Client

# Time tracker
start_time = time.time()

# Loading environments.
load_dotenv()

# Environment variables.
LS_URL = os.getenv("LS_URL", "http://url-for-labelstudio")
LS_API_KEY = os.getenv("LS_API_KEY", "TOKEN")
DAYS_FOR_DELETE = int(os.getenv("DAYS_FOR_DELETE", 7))

# Formed variables
FILTER_DATETIME = (datetime.now().date() - timedelta(days=DAYS_FOR_DELETE)).strftime("%Y-%m-%dT%H:%M:%S.%f%zZ")

# Initialize Label Studio Client.
ls = Client(url=LS_URL, api_key=LS_API_KEY)

# Get all LS projects.
ls_projects = ls.get_projects()

# Processing of each LS project.
for ls_project in ls_projects:
    # Get LS project task IDs with completed_at parameter less than FILTER_DATETIME ago.
    ls_project_tasks = ls_project.get_tasks(
        filters={
            "conjunction": "and",
            "items": [
                {
                    "filter": "filter:tasks:completed_at",
                    "operator": "less",
                    "value": FILTER_DATETIME,
                    "type": "Datetime",
                },
            ],
        },
        only_ids=True,
    )
    # Logging
    print(f"Проект: {ls_project.get_params().get('title')}. Количество удаляемых задач: {len(ls_project_tasks)}")
    # Delete collected LS project tasks.
    ls_project.delete_tasks(task_ids=ls_project_tasks)


end_time = time.time()
execution_time = end_time - start_time
print("Время выполнения: ", execution_time, "секунд")
