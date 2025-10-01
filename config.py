import os
import dotenv
from pathlib import Path

# Загружаем .env из текущей рабочей директории (или можно указать другой путь)
dotenv.load_dotenv(Path('.env'))

# MySQL
MYSQL_CONFIG = {
    "host": os.environ.get("MYSQL_HOST"),
    "user": os.environ.get("MYSQL_USER"),
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": os.environ.get("MYSQL_DATABASE"),
}

# MongoDB
MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.environ.get("MONGO_COLLECTION_NAME")

# Прочее
RESULTS_PAGE_SIZE = int(os.environ.get("RESULTS_PAGE_SIZE", 10))
