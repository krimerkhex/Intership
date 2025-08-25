import json
from loguru import logger


async def consume_upload_aggregate_data(consumer):
    try:
        logger.info("Waiting for message from kafka")
        async for msg in consumer:
            try:
                message = json.loads(msg.value.decode('utf-8'))
                message = message["file"]
                if message:
                    logger.info("Message processed successfully")
                    return message
                return None
            except Exception as e:
                logger.exception(f"Error processing message: {e}")
    finally:
        await consumer.stop()
