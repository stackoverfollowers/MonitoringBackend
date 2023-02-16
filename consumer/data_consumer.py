from aiokafka import AIOKafkaConsumer
from aiokafka.helpers import create_ssl_context

from config import KafkaConfig


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
    print("Cool, weare connected!")
    try:
        # Consume messages
        print(1)
        async for msg in consumer:
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )
    finally:
        await consumer.stop()
