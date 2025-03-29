from pymongo import MongoClient
from FallenRobot import MONGO_DB_URI

client = MongoClient(MONGO_DB_URI)
db = client.FallenRobot

# Collections
karma = db.karma  # Karma collection