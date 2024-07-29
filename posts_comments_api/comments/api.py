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
    return {"id": new_comment.id}


# api/comments/list/

@router.get("/list", response=List[CommentEntryListSchema])
def list_comments(request):
    qs = Comments.objects.all()
    return qs


# api/comments/{comment_id}
@router.get("/{comment_id}", response=CommentEntryDetailSchema)
def get_comment(request, comment_id: int):
    obj = get_object_or_404(Comments, id=comment_id)
    return obj


# api/comments/{comment_id}
@router.put("/{comment_id}", response=CommentEntryDetailSchema)
def update_comment(request, comment_id: int, data: CommentEntryUpdateSchema):
    obj = get_object_or_404(Comments, id=comment_id)
    obj.update(**data.dict())
    return obj


# api/comments/{comment_id}
@router.delete("/{comment_id}", response=CommentEntryDeleteSchema)
def delete_comment(request, comment_id: int):
    obj = get_object_or_404(Comments, id=comment_id)
    obj.delete()
    return {'id': comment_id}