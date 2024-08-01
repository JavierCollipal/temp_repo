from mongoengine import connect
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DATABASE_NAME", "mydatabase")

def init_db():
    connect(db=MONGO_DB_NAME, host=MONGO_URI)