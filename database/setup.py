from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from database.models import Base


engine = create_async_engine("sqlite+aiosqlite:///database/data.db", echo=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def get_session() -> async_sessionmaker:
    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,    
        expire_on_commit=False
        )
    
    return AsyncSessionLocal
