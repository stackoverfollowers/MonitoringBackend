import os

import dotenv

dotenv.load_dotenv()


class KafkaConfig:
    CONTEXT_FILE = "CA.perm"
    TOPIC = "zsmk-9433-dev-01"
    CLIENT_ID = "9433_reader"
    SECURITY_PROTOCOL = "SASL_SSL"
    SASL_MECHANISM = "SCRAM-SHA-512"
    SASL_PLAIN_USERNAME = "9433_reader"
    SASL_PLAIN_PASSWORD = "eUIpgWu0PWTJaTrjhjQD3.hoyhntiK"
    BOOTSTRAP_SERVERS = "rc1a-2ar1hqnl386tvq7k.mdb.yandexcloud.net:9091"
    GROUP_ID = "stackoverfollowers"


class MongoConfig:
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASS = os.getenv("MONGO_PASS")
    CONNECTION_STRING = f"mongodb://{MONGO_USER}:{MONGO_PASS}@mongodb:27017"
    DB_NAME = os.getenv("MONGO_DB")
    COLLECTION_NAME = "data_col"
