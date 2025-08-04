from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship with books (one-to-many)
    books = relationship("Book", back_populates="owner", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="user", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Foreign key to user
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship with user (many-to-one)
    owner = relationship("User", back_populates="books")

    votes = relationship("Vote", back_populates="book", cascade="all, delete-orphan")

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="votes")
    book = relationship("Book", back_populates="votes")

    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="uix_vote"),
    )