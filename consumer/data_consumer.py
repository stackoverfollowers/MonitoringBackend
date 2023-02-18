import json
import logging
import time
import traceback
from typing import Optional

from aiokafka import AIOKafkaConsumer
from aiokafka.helpers import create_ssl_context

from config import KafkaConfig
from db.db import mongodb


class LastData:
    def __init__(self):
        self.timestamp: Optional[int] = None
        self.data: Optional[dict] = None


last_data = LastData()


async def consume_forever():
    consumer = AIOKafkaConsumer(
        KafkaConfig.TOPIC,
        client_id=KafkaConfig.CLIENT_ID,
        security_protocol=KafkaConfig.SECURITY_PROTOCOL,
        sasl_mechanism=KafkaConfig.SASL_MECHANISM,
        sasl_plain_username=KafkaConfig.SASL_PLAIN_USERNAME,
        sasl_plain_password=KafkaConfig.SASL_PLAIN_PASSWORD,
        ssl_context=create_ssl_context(cafile=KafkaConfig.CONTEXT_FILE),
        bootstrap_servers=KafkaConfig.BOOTSTRAP_SERVERS,
        group_id=KafkaConfig.GROUP_ID,
        request_timeout_ms=1000,
    )
    last_data.data = (await mongodb.get_last_data())["value"]
    last_data.timestamp = time.time()

    await consumer.start()
    while True:
        try:
            print("Cool, we'are connected!")
            async for msg in consumer:
                msg_dict = msg.__dict__
                msg_dict["value"] = json.loads(msg_dict["value"].decode("utf-8"))
                last_data.data = msg_dict["value"]
                last_data.timestamp = time.time()
                # todo: данные по датаам
                # todo: docker
                await mongodb.write_in_base(data=msg_dict)
        except Exception as e:
            logging.error(traceback.format_exc())
