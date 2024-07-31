from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from typing import List

from .models import Comments

from .schemas import (
    CommentEntryListSchema,
    CommentEntryCreateSchema,
    CommentEntryDetailSchema,
    CommentEntryUpdateSchema,
    CommentEntryDeleteSchema
)

router = Router()


# api/comments/create
@router.post("/create", response=CommentEntryDetailSchema, auth=JWTAuth())
def create_comment(request, comment: CommentEntryCreateSchema):
    new_comment = Comments.objects.create(**comment.dict())
    return {"id": new_comment.id,
            'user_id': new_comment.user_id,
            'post_id': new_comment.post_id,
            'content': new_comment.content,
            'created_at': new_comment.created_at,
            'updated_at': new_comment.updated_at,
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
