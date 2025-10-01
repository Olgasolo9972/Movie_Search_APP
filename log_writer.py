from pymongo import MongoClient
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from pathlib import Path

# Загружаем переменные из .env
load_dotenv(Path('.env'))

# Получаем переменные окружения
MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.environ.get("MONGO_COLLECTION_NAME")

# Создаем клиент и коллекцию
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

def log_search(query_type, query_value, timestamp=None):
    # Записывает поисковый запрос в MongoDB
    if timestamp is None:
        timestamp = datetime.now(timezone.utc)

    document = {
        "query_type": query_type,
        "query": query_value,
        "timestamp": timestamp
    }

    try:
        collection.insert_one(document)
        print("Search query successfully logged.")
    except Exception as e:
        print(f"Failed to log search query: {e}")

def close_connection():
    # Закрывает подключение к MongoDB
    client.close()
    print("MongoDB connection closed.")

if __name__ == "__main__":
    log_search("keyword", "test_search", timestamp=datetime.now(timezone.utc))
    close_connection()
