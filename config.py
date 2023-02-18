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
    CONNECTION_STRING = "mongodb://localhost:27017"
    DB_NAME = "main_db"
    COLLECTION_NAME = "data_col"
