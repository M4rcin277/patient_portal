import os

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None


if load_dotenv:
    load_dotenv()


MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "patient_portal")
_mongo_client = None


def pobierz_klienta_mongo():
    global _mongo_client

    if MongoClient is None:
        raise RuntimeError("Brakuje biblioteki pymongo. Uruchom: pip install -r requirements.txt")

    if _mongo_client is None:
        _mongo_client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=2000)

    return _mongo_client


def pobierz_baze_mongo():
    klient = pobierz_klienta_mongo()
    return klient[MONGODB_DB_NAME]
