from asyncio import run, sleep as async_sleep
from loguru import logger

from aiokafka import AIOKafkaConsumer

from upload_aggregate_data.kafka.consumer.consumer import consume_upload_aggregate_data
from upload_aggregate_data.config.config import config
from upload_aggregate_data.database.crud.company_data_crud import CompanyDataCRUD
from upload_aggregate_data.database.connecting import db_connector


async def core():
    try:
        consumer = AIOKafkaConsumer(
            config.kafka.TOPIC,
            bootstrap_servers=f"{config.kafka.HOST}:{config.kafka.PORT}",
            enable_auto_commit=True,
            auto_offset_reset='earliest')
        async with db_connector.session_factory() as session:
            while True:
                await consumer.start()
                try:
                    message = await consume_upload_aggregate_data(consumer)
                    logger.info(await CompanyDataCRUD.upload_file_data(session, message))
                    await async_sleep(5)
                except Exception as ex:
                    logger.exception(ex)
                finally:
                    await consumer.stop()
    except Exception as ex:
        logger.exception(ex)


if __name__ == "__main__":
    run(core())
