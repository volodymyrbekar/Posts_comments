from ninja import Schema
from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel


class CommentAnalyticsSchema(BaseModel):
    date: date
    total_comments: int
    blocked_comments: int


class CommentEntryCreateSchema(Schema):
    content: str
    post_id: int
    user_id: int


class CommentEntryListSchema(Schema):
    id: int
    content: str
    user_id: int
    post_id: int


class CommentEntryDetailSchema(Schema):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int
    post_id: int


class CommentEntryUpdateSchema(Schema):
    content: Optional[str]


class CommentEntryDeleteSchema(Schema):
    id: int