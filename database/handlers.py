from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from database.models import User, Message
from database.setup import get_session
from typing import Optional


AsyncSessionLocal: async_sessionmaker[AsyncSession] = get_session()


async def get_user(user_id: int) -> Optional[User]:
    """Функция получения данных о пользователе из бд

    Args:
        user_id (int): id пользователя в телеграмме

    Returns:
        User: Объект пользователя | None
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).filter_by(user_id=user_id))
        return result.scalars().first()


async def add_user(user_id: int, username: str) -> None:
    """Функция для добавления пользователя в бд

    Args:
        user_id (int): id пользователя в телеграмме
        username (str): Тег пользователя
    """
    async with AsyncSessionLocal() as session:
        new_user = User(user_id=user_id, username=username)
        session.add(new_user)
        await session.commit()


async def log_message(sender_id: int, text: str) -> None:
    """Функция для логирования сообщения пользователя в бд

    Args:
        sender_id (int): id пользователя в телеграмме
        text (str): Текст сообщения
    """
    async with AsyncSessionLocal() as session:
        message = Message(sender_id=sender_id, text=text)
        session.add(message)
        await session.commit()
