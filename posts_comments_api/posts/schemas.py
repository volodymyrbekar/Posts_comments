from datetime import datetime

from ninja import Schema


class PostsEntryCreateSchema(Schema):
    # Post data
    title: str
    content: str


class PostsEntryListSchema(Schema):
    # Get list of posts
    id: int
    title: str
    content: str


class PostsEntryDetailSchema(Schema):
    # Get data
    id: int
    title: str
    content: str
    updated_at: datetime
    created_at: datetime


class PostsEntryUpdateSchema(Schema):
    id: int
    title: str
    content: str


class PostsEntryDeleteSchema(Schema):
    # Delete data
    id: int

