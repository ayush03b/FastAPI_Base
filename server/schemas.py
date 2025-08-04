import email
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional
from pydantic import EmailStr
from pydantic.types import conint


# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Book Schemas
class BookBase(BaseModel):
    title: str
    author: str
    price: float


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None


class BookResponse(BookBase):
    id: int
    created_at: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class BookWithVotes(BookResponse):
    votes: int
    owner: UserResponse

    model_config = ConfigDict(from_attributes=True)


class VoteInfo(BaseModel):
    user_id: int
    username: str
    email: EmailStr


class BookWithOwner(BookResponse):
    owner: UserResponse

    model_config = ConfigDict(from_attributes=True)


# User with books relationship
class UserWithBooks(UserResponse):
    books: List[BookResponse] = []

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    book_id: int
    direction: conint(ge=-1, le=1) = Field(
        ...,
        description="Vote direction: 1 for upvote, -1 for downvote, 0 to remove vote",
    )
