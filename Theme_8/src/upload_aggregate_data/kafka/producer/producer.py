import json
from aiokafka import AIOKafkaProducer
from loguru import logger
from upload_aggregate_data.config.config import config


async def send_to_kafka(message: dict, topic: str = config.kafka.TOPIC):
    producer = AIOKafkaProducer(
        bootstrap_servers=f"{config.kafka.HOST}:{config.kafka.PORT}",
        max_request_size=20000000,
        compression_type="gzip",
    )
    await producer.start()
    try:
        await producer.send_and_wait(topic, json.dumps(message).encode("utf-8"))
        logger.info(f"Message sent to Kafka topic {topic}")
    except Exception as e:
        logger.exception(f"Failed to send message to Kafka: {e}")
        raise
    finally:
        await producer.stop()
