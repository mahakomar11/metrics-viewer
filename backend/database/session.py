from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import Config


async def get_session(config: Config) -> AsyncSession:
    engine = create_async_engine(
        config.async_postgres_url,
        pool_size=30,
        max_overflow=0,
        pool_pre_ping=True,  # liveness upon each checkout
    )

    session_maker = async_sessionmaker(engine)
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        finally:
            await session.rollback()
