"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogpost" collection
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List

# ------------------
# Example schemas
# ------------------
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: Optional[str] = Field(None, description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# ------------------
# Portfolio schemas
# ------------------
class Team(BaseModel):
    name: str = Field(..., description="Team name")
    tagline: Optional[str] = Field(None, description="Short team tagline")
    about: Optional[str] = Field(None, description="Team description")
    website: Optional[HttpUrl] = Field(None, description="Team website URL")
    github: Optional[HttpUrl] = Field(None, description="GitHub org URL")
    x: Optional[HttpUrl] = Field(None, description="X/Twitter URL")
    linkedin: Optional[HttpUrl] = Field(None, description="LinkedIn URL")

class Member(BaseModel):
    name: str = Field(..., description="Member full name")
    role: str = Field(..., description="Primary role/title")
    bio: Optional[str] = Field(None, description="Short bio")
    avatar: Optional[HttpUrl] = Field(None, description="Avatar image URL")
    github: Optional[HttpUrl] = Field(None, description="GitHub profile")
    linkedin: Optional[HttpUrl] = Field(None, description="LinkedIn profile")
    twitter: Optional[HttpUrl] = Field(None, description="Twitter profile")
    skills: List[str] = Field(default_factory=list, description="Notable skills")

class Project(BaseModel):
    title: str = Field(..., description="Project title")
    summary: str = Field(..., description="Short project summary")
    cover: Optional[HttpUrl] = Field(None, description="Cover image URL")
    repo: Optional[HttpUrl] = Field(None, description="Repository URL")
    demo: Optional[HttpUrl] = Field(None, description="Live demo URL")
    members: List[str] = Field(default_factory=list, description="Members involved (names)")
    tags: List[str] = Field(default_factory=list, description="Tech or topic tags")
