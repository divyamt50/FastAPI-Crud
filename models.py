from __future__ import annotations
from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base

class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username:Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email:Mapped[str] = mapped_column(String(120), unique = True, nullable = False)
    password_hash:Mapped[str] = mapped_column(String(255), nullable=False)
    image_file: Mapped[None|str] = mapped_column(String(200), nullable=True, default=None)

    posts: Mapped[list[Post]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    title:Mapped[str] = mapped_column(String(100), nullable=False)
    description:Mapped[str] = mapped_column(Text, nullable=False)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index = True)
    date_posted:Mapped[datetime] = mapped_column(DateTime(timezone=True), default = lambda:datetime.now(UTC))

    author:Mapped[User] = relationship(back_populates="posts")

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id:Mapped[int] = mapped_column(primary_key=True)
    token_hash:Mapped[str] = mapped_column(String, unique=True, index=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    expires_at:Mapped[datetime] = mapped_column(DateTime)
    used:Mapped[bool] = mapped_column(Boolean, default=False)