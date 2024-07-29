from datetime import datetime
from typing import Optional

from ninja import Schema


class PostsEntryCreateSchema(Schema):
    # Post data
    title: str
    content: str
    user_id: int


class PostsEntryListSchema(Schema):
    # Get list of posts
    id: int
    title: str
    content: str
    user_id: int


class PostsEntryDetailSchema(Schema):
    # Get data
    id: int
    title: str
    content: str
    updated_at: datetime
    created_at: datetime
    user_id: int


class PostsEntryUpdateSchema(Schema):
    title: Optional[str] = None
    content: Optional[str] = None


class PostsEntryDeleteSchema(Schema):
    # Delete data
    id: int

