from pymongo import MongoClient
from .configuration import MONGO_URI, MONGO_DB

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
products_collection = db["products"]
users_collection = db["users"]
# categories_collection = db["categories"]
