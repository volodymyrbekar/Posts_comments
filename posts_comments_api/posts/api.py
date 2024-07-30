from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from .schemas import (
    PostsEntryCreateSchema,
    PostsEntryListSchema,
    PostsEntryDetailSchema,
    PostsEntryUpdateSchema,
    PostsEntryDeleteSchema,
)
from .models import PostEntry

router = Router()


# /api/posts/create
@router.post("/create", response=PostsEntryDetailSchema, auth=JWTAuth())
def create_post(request, post: PostsEntryCreateSchema):
    new_post = PostEntry.objects.create(**post.dict())
    return {"id": new_post.id,
            "title": new_post.title,
            "content": new_post.content,
            "created_at": new_post.created_at,
            "updated_at": new_post.updated_at,
            "user_id": new_post.user_id,
            }


# /api/posts/list/
@router.get("/list", response=List[PostsEntryListSchema])
def list_posts_entries(request):
    qs = PostEntry.objects.all()
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