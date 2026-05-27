from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import secrets
from datetime import datetime, UTC
from models import PasswordResetToken,User
from users import find_user_by_email

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

import aiosmtplib
from email.message import EmailMessage
from config import settings

async def send_reset_email(email_to: str, raw_token: str):
    message = EmailMessage()
    message["From"] = settings.mail_from
    message["To"] = email_to
    message["Subject"] = "Password Reset Request"
    
    # In a real API, this points to your frontend application's URL
    reset_link = f"http://localhost:8000/reset-password?token={raw_token}"
    message.set_content(f"Click here to reset your password: {reset_link}")

    await aiosmtplib.send(
        message,
        hostname=settings.mail_server,
        port=settings.mail_port,
        username=settings.mail_username,
        password=settings.mail_password,
        start_tls=settings.mail_use_tls,
    )

@router.post("/forgot-password")
async def forgot_password(
    email: str, 
    background_tasks: BackgroundTasks, # 1. Inject the dependency
    db: AsyncSession = Depends(get_db)
):
    user = await find_user_by_email(db, email)
    if not user:
        # Security: Always return a generic message so attackers can't verify emails
        return {"message": "If that email exists, a reset link was sent."}

    # 2. Generate a secure random token
    raw_token = secrets.token_urlsafe(32)
    token_hash = hash_password(raw_token) # Re-use your password hashing function

    # 3. Save the hash to the database
    expiration = datetime.now(UTC) + timedelta(minutes=settings.reset_token_expire_minutes)
    db_token = PasswordResetToken(
        token_hash=token_hash, 
        user_id=user.id, 
        expires_at=expiration
    )
    db.add(db_token)
    await db.commit()

    # 4. Hand the email task to FastAPI to run in the background
    background_tasks.add_task(send_reset_email, user.email, raw_token)

    return {"message": "If that email exists, a reset link was sent."}


@router.post("/reset-password")
async def reset_password(
    token: str, 
    new_password: str, 
    db: AsyncSession = Depends(get_db)
):
    # 1. Hash the incoming raw token to look it up in the DB
    incoming_hash = hash_password(token)
    
    # 2. Query the DB for a matching, unused, unexpired token
    db_token = await db.scalar(
        select(PasswordResetToken)
        .where(
            PasswordResetToken.token_hash == incoming_hash,
            PasswordResetToken.used == False,
            PasswordResetToken.expires_at > datetime.now(UTC)
        )
    )

    if not db_token:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # 3. Update the user's password
    user = await db.get(User, db_token.user_id)
    user.hashed_password = hash_password(new_password)
    
    # 4. Mark the token as used so it cannot be used again (Single-Use)
    db_token.used = True
    
    await db.commit()
    return {"message": "Password updated successfully"}