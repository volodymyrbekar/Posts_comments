from ninja import Router, Query
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from typing import List

from datetime import datetime, timedelta
from collections import defaultdict

from .models import Comments
from toxicity_checker import is_toxic
from .tasks import schedule_auto_reply

from users.models import User
from django.core.exceptions import ObjectDoesNotExist

from .schemas import (
    CommentEntryListSchema,
    CommentEntryCreateSchema,
    CommentEntryDetailSchema,
    CommentEntryUpdateSchema,
    CommentEntryDeleteSchema,
    CommentAnalyticsSchema,
)

router = Router()


# /api/comments-daily-breakdown
@router.get("/comments-daily-breakdown", response=List[CommentAnalyticsSchema])
def comments_daily_breakdown(request, date_from: str = Query(...), date_to: str = Query(...)):
    # Convert date_from and date_to to datetime objects
    date_from = datetime.strptime(date_from, '%Y-%m-%d')
    date_to = datetime.strptime(date_to, '%Y-%m-%d')

    comments = Comments.objects.filter(created_at__range=(date_from, date_to))

    #  Create a dictionary to store the count of total and blocked comments for each day
    comments_count = defaultdict(lambda: {"total_comments": 0, "blocked_comments": 0})

    # Group and count comments
    for comment in comments:
        date = comment.created_at.date()
        comments_count[date]["total_comments"] += 1
        if comment.is_blocked:
            comments_count[date]["blocked_comments"] += 1

    result = [{'date': date, **counts} for date, counts in comments_count.items()]

    return result


# api/comments/create
@router.post("/create", response=CommentEntryDetailSchema, auth=JWTAuth())
def create_comment(request, comment: CommentEntryCreateSchema):
    is_comment_toxic = is_toxic(comment.content)
    new_comment = Comments.objects.create(**comment.dict(), is_blocked=is_comment_toxic)
    if is_comment_toxic:
        return JsonResponse({"message": "The comment contains toxic content and has been blocked."}, status=403)
    try:
        user = User.objects.get(id=comment.user_id)
        if user.auto_reply_enabled:
            # Schedule the auto-reply
            auto_replay_time = datetime.now() + timedelta(minutes=user.auto_reply_delay)
            schedule_auto_reply.apply_async(args=[new_comment.id, user.auto_reply_message], eta=auto_replay_time)
    except ObjectDoesNotExist:
        pass
    return {"id": new_comment.id,
            'user_id': new_comment.user_id,
            'post_id': new_comment.post_id,
            'content': new_comment.content,
            'created_at': new_comment.created_at,
            'updated_at': new_comment.updated_at,
            'is_blocked': new_comment.is_blocked
            }


# api/comments/list/
@router.get("/list", response=List[CommentEntryListSchema])
def list_comments(request):
    qs = Comments.objects.all()
    return qs


# api/comments/{comment_id}
@router.get("/{comment_id}", response=CommentEntryDetailSchema)
def get_comment(request, comment_id: int):
    comment = get_object_or_404(Comments, id=comment_id)
    return comment


# api/comments/{comment_id}
@router.put("/{comment_id}", response=CommentEntryDetailSchema, auth=JWTAuth())
def update_comment(request, comment_id: int, data: CommentEntryUpdateSchema):
    comment = get_object_or_404(Comments, id=comment_id)
    for field, value in data.dict().items():
        setattr(comment, field, value)
    comment.save()
    return comment


# api/comments/{comment_id}
@router.delete("/{comment_id}", response=CommentEntryDeleteSchema, auth=JWTAuth())
def delete_comment(request, comment_id: int):
    obj = get_object_or_404(Comments, id=comment_id)
    obj.delete()
    return {'id': comment_id, 'message': 'Comment deleted successfully!'}
