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


@router.post("", response=PostsEntryDetailSchema)
def create_post_entry(request, data: PostsEntryCreateSchema):
    odj = PostEntry.objects.create(**data.dict())
    return odj


# /api/posts/
@router.get("", response=List[PostsEntryListSchema])
def list_posts_entries(request):
    qs = PostEntry.objects.all()
    return qs


# /api/posts/{entry_id}
@router.get("{entry_id}", response=PostsEntryDetailSchema)
def get_posts_entry(request, entry_id: int):
    obj = get_object_or_404(PostEntry, id=entry_id)
    return obj