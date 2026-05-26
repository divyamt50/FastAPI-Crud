from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession



import models
from auth import(
    ACCESS_TOKEN_EXPIRE_MINUTE,
    create_access_token,
    hash_password,
    verify_password
)

from db import get_db
from schemas import Token, UserCreate, UserResponse

router = APIRouter(prefix="/api/auth", tags = ["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user:UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    # Check existing username
    result = await db.execute(select(models.User).where(models.User.username == user.username))
    if result.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    # Check existing email
    result = await db.execute(select(models.User).where(models.User.email == user.email))
    if result.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post('/login', response_model=Token)
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db:Annotated[AsyncSession, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.username == form_data.username)
    )

    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data = {"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    )

    return Token(access_token=access_token, token_type="bearer")