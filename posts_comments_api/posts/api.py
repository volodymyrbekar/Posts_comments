from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router


from .schemas import (
    PostsEntryCreateSchema,
    PostsEntryListSchema,
    PostsEntryDetailSchema,
    PostsEntryUpdateSchema,
    PostsEntryDeleteSchema,
)
from .models import PostEntry

router = Router()


# Create a new post
# @router.post("/posts", response=PostsEntryDetailSchema)
# def create_post(request, data_in: PostsEntryCreateSchema):
#     post = PostEntry.objects.create(**data_in.dict())
#     return post


@router.get("", response=List[PostsEntryListSchema])
def list_posts_entries(request):
    qs = PostEntry.objects.all()
    return qs


@router.get("{entry_id}", response=PostsEntryDetailSchema)
def get_posts_entry(request, entry_id: int):
    obj = get_object_or_404(PostEntry, id=entry_id)
    return obj
