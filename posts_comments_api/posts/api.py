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
    return {"id": new_post.id}


# /api/posts/list/
@router.get("/list", response=List[PostsEntryListSchema])
def list_posts_entries(request):
    qs = PostEntry.objects.all()
    return qs


# /api/posts/{entry_id}
@router.put("/{entry_id}", response=PostsEntryDetailSchema)
def get_posts_entry(request, entry_id: int, data: PostsEntryUpdateSchema):
    obj = get_object_or_404(PostEntry, id=entry_id)
    return obj


# /api/posts/{entry_id}
@router.delete("/{entry_id}", response=PostsEntryDeleteSchema)
def delete_posts_entry(request, entry_id: int):
    obj = get_object_or_404(PostEntry, id=entry_id)
    obj.delete()
    return {'id': entry_id}