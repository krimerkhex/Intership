from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)

from typing import AsyncGenerator

from upload_aggregate_data.config.config import config


class DatabaseConnector:
    def __init__(
            self,
            url: str,
    ):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_connector = DatabaseConnector(
    url=str(config.db.URL),
)
