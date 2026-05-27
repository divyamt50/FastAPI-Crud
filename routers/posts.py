from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import models
from db import get_db
from schemas import PostCreate, PostResponse, PostUpdate, PostPagination
from auth import get_current_user

router = APIRouter(
    prefix="/api/posts",
    tags=["posts"],
)

@router.get("", response_model=PostPagination)
async def get_posts(
        db: Annotated[AsyncSession, Depends(get_db)],
        skip:Annotated[int, Query(ge=0)] = 0,
        limit:Annotated[int, Query(ge=1,le=100)] = 10
    ):
    count_query = select(func.count()).select_from(models.Post)
    total = await db.scalar(count_query) or 0

    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .order_by(models.Post.id.desc())
        .offset(skip)
        .limit(limit)
    )
    posts = result.scalars().all()
    has_more = (skip + len(posts)) < total

    return PostPagination(
        posts = posts,
        limit = limit,
        total = total,
        skip = skip,
        has_more = has_more
    )

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.id == post_id)
    )
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, current_user:Annotated[models.User, Depends(get_current_user)],db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User).where(models.User.id == post.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    new_post = models.Post(title=post.title, content=post.content, user_id=current_user.id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post, attribute_names=["author"])
    return new_post

@router.patch("/{post_id}", response_model=PostResponse)
async def patch_post(
    post_id: int,
    post_data: PostUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    update_data = post_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)

    await db.commit()
    await db.refresh(post, attribute_names=["author"])
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, current_user:Annotated[models.User, Depends(get_current_user)],db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    


    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you can delete only your posts"
        )

    await db.delete(post)
    await db.commit()
    return None