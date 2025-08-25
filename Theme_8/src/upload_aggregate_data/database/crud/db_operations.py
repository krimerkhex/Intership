from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger


def db_catcher(log_message: str = "Database operation"):
    def decorator(func):
        @wraps(func)
        async def wrapper(session, *args, **kwargs):
            logger.info(log_message)
            try:
                result = await func(session, *args, **kwargs)
                await session.commit()
                return result
            except SQLAlchemyError as e:
                logger.error(e)
                await session.rollback()
                raise

        return wrapper

    return decorator
