import os
from dotenv import load_dotenv
from pathlib import Path
from pymongo import MongoClient

# Загружаем переменные из .env
load_dotenv(Path('.env'))

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("MONGO_DB_NAME", "ich_edit")
COLLECTION_NAME = os.environ.get("MONGO_COLLECTION_NAME", "final_project_250425-ptm_OlgaSolo")

# Подключаемся к MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def get_last_searches(limit=5):
    cursor = collection.find().sort("timestamp", -1).limit(limit)
    return list(cursor)

def get_top_searches(limit=5):
    pipeline = [
        {"$group": {"_id": "$query", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    return list(collection.aggregate(pipeline))

def close_connection():
    client.close()

if __name__ == "__main__":
    print("Last search queries:")
    for item in get_last_searches():
        print(item)

    print("\nTop search queries:")
    for item in get_top_searches():
        print(item)

    close_connection()
