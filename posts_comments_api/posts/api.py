from collections import defaultdict
from typing import List
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ninja import Router, Query
from ninja_jwt.authentication import JWTAuth

from .schemas import (
    PostsEntryCreateSchema,
    PostsEntryListSchema,
    PostsEntryDetailSchema,
    PostsEntryUpdateSchema,
    PostsEntryDeleteSchema,
    PostsDailyAnalyticsSchema,
)
from .models import PostEntry

from toxicity_checker import is_toxic

router = Router()


# /api/posts/daily-breakdown
@router.get("/daily-breakdown", response=List[PostsDailyAnalyticsSchema])
def posts_daily_breakdown(request, date_from: str = Query(...), date_to: str = Query(...)):
    # Convert date_from and date_to to datetime objects
    date_from = datetime.strptime(date_from, '%Y-%m-%d')
    date_to = datetime.strptime(date_to, '%Y-%m-%d')

    qs = PostEntry.objects.filter(created_at__range=(date_from, date_to))

    posts_count = defaultdict(lambda: {"total_posts": 0, "blocked_posts": 0})

    for post in qs:
        date = post.created_at.date()
        posts_count[date]["total_posts"] += 1
        if post.is_blocked:
            posts_count[date]["blocked_posts"] += 1

    result = [{'date': date, **counts} for date, counts in posts_count.items()]
    return result


# /api/posts/create
@router.post("/create", response=PostsEntryDetailSchema, auth=JWTAuth())
def create_post_entries(request, post: PostsEntryCreateSchema):
    is_post_toxic = is_toxic(post.content)
    new_post = PostEntry.objects.create(**post.dict(), is_blocked=is_post_toxic)
    if is_post_toxic:
        return JsonResponse({"message": "The post contains toxic content and has been blocked."}, status=403)
    return {"id": new_post.id,
            "title": new_post.title,
            "content": new_post.content,
            "created_at": new_post.created_at,
            "updated_at": new_post.updated_at,
            "user_id": new_post.user_id,
            "is_blocked": new_post.is_blocked
            }


# /api/posts/list/
@router.get("/list", response=List[PostsEntryListSchema])
def list_posts_entries(request):
    qs = PostEntry.objects.filter(is_blocked=False)
    return qs


# /api/posts/{entry_id}
@router.get("/{entry_id}", response=PostsEntryDetailSchema)
def get_posts_entry(request, entry_id: int):
    post = get_object_or_404(PostEntry, id=entry_id)
    return post


# /api/posts/{entry_id}
@router.put("/{entry_id}", response=PostsEntryDetailSchema, auth=JWTAuth())
def update_posts_entry(request, entry_id: int, data: PostsEntryUpdateSchema):
    post = get_object_or_404(PostEntry, id=entry_id)
    for field, value in data.dict().items():
        setattr(post, field, value)
    post.save()
    return post


# /api/posts/{entry_id}
@router.delete("/{entry_id}", response=PostsEntryDeleteSchema, auth=JWTAuth())
def delete_posts_entry(request, entry_id: int):
    obj = get_object_or_404(PostEntry, id=entry_id)
    obj.delete()
    return {'id': entry_id, 'message': 'deleted successfully'}
