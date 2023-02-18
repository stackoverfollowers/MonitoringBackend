import json
import logging
import traceback

from aiokafka import AIOKafkaConsumer
from aiokafka.helpers import create_ssl_context
from kafka import TopicPartition

from config import KafkaConfig
from consumer.mapper import ExMapper
from db.db import mongodb


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
        enable_auto_commit=False,
        auto_offset_reset="earliest",
    )
    await consumer.start()
    tp = TopicPartition(KafkaConfig.TOPIC, 0)
    print(
        consumer.partitions_for_topic(
            KafkaConfig.TOPIC,
        )
    )
    await consumer.seek_to_beginning(tp)

    while True:
        try:
            print("Cool, we'are connected!")
            async for msg in consumer:
                print(msg)
                msg_dict = msg.__dict__
                msg_dict["value"] = json.loads(msg_dict["value"].decode("utf-8"))

                mapper = ExMapper(msg_dict["value"])
                print(mapper.moment)

                result_id = await mongodb.write_in_base(data=msg_dict)
                print(f"{result_id=}")
        except Exception as e:
            print(traceback.format_exc())
            logging.error(traceback.format_exc())


if __name__ == "__main__":
    import asyncio

    asyncio.get_event_loop().run_until_complete(consume_forever())
