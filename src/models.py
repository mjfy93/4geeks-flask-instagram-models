from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Dict, Any, Optional
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), 
        unique=True, 
        nullable=False)
    password: Mapped[str] = mapped_column(
        nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), 
        nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        back_populates="author", 
        cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="author", 
        cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship(
        back_populates="author", 
        cascade="all, delete-orphan")
    
    
    following: Mapped[List["Follower"]] = relationship(
        foreign_keys="Follower.follower_id",
        back_populates="follower_user",
        cascade="all, delete-orphan"
    )
    followers: Mapped[List["Follower"]] = relationship(
        foreign_keys="Follower.followed_id",
        back_populates="followed_user",
        cascade="all, delete-orphan"
    )

    def serialize(self)-> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active
        }
    
class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(
        primary_key=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False)
    image_url: Mapped[str] = mapped_column(
        String(300), 
        nullable=False)
    caption: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False)  

    author: Mapped["User"] = relationship(
        back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="post", 
        cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship(
        back_populates="post", 
        cascade="all, delete-orphan")

    def serialize(self)-> Dict[str, Any]:
        return {
            "id": self.id,
            "author_id": self.author_id,
            "image_url": self.image_url,
            "caption": self.caption
        }

class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"), 
        nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()) 

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self)-> Dict[str, Any]:
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }

class Like(db.Model):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"), 
        nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()) 

    user: Mapped["User"] = relationship(back_populates="likes")
    post: Mapped["Post"] = relationship(back_populates="likes")

    def serialize(self)-> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id
        }
    
class Follower(db.Model):
    __tablename__ = "followers"
    __table_args__ = (
        UniqueConstraint('follower_id', 'followed_id', name='unique_follow'),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False)
    followed_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()) 
    
    follower_user: Mapped["User"] = relationship(
        foreign_keys=[follower_id],
        back_populates="following"
    )
    followed_user: Mapped["User"] = relationship(
        foreign_keys=[followed_id],
        back_populates="followers"
    )
    
    def serialize(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id
        }