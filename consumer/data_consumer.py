import json

from aiokafka import AIOKafkaConsumer
from aiokafka.helpers import create_ssl_context

from config import KafkaConfig
from db.db import write_in_base


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

    await consumer.start()
    print("Cool, we\'are connected!")
    try:
        async for msg in consumer:
            msg_dict = msg.__dict__
            msg_dict["value"] = json.loads(msg_dict["value"].decode("utf-8"))
            result_id = await write_in_base(data=msg_dict)
            print(f"{result_id=}")
    finally:
        await consumer.stop()
