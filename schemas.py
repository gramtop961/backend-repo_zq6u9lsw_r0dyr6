"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List

# Example schemas (retain as examples)
class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Portfolio-specific schemas
class Project(BaseModel):
    """
    Portfolio projects
    Collection: "project"
    """
    title: str = Field(..., description="Project title")
    description: str = Field(..., description="Short description of the project")
    tags: List[str] = Field(default_factory=list, description="Tech stack tags")
    github: Optional[HttpUrl] = Field(None, description="GitHub repository URL")
    demo: Optional[HttpUrl] = Field(None, description="Live demo URL")
    image: Optional[HttpUrl] = Field(None, description="Preview image URL")

class Contactmessage(BaseModel):
    """
    Contact messages
    Collection: "contactmessage"
    """
    name: str = Field(..., min_length=2)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=5000)
