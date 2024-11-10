import datetime
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import func


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)


class Message(Base):
    __tablename__ = "messages"
    uid: Mapped[str] = mapped_column(primary_key=True, default= lambda: str(uuid4()))
    sender_id: Mapped[int]
    text: Mapped[str]
    time: Mapped[datetime.datetime] = mapped_column(server_default=func.now())