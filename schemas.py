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

from pydantic import BaseModel, Field
from typing import Optional, List

# Core ecommerce schemas

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    images: List[str] = Field(default_factory=list, description="List of image URLs")
    featured: bool = Field(False, description="Whether product is featured on homepage")
    rating: float = Field(4.5, ge=0, le=5, description="Average rating")
    reviews_count: int = Field(0, ge=0, description="Number of reviews")
    sizes: List[str] = Field(default_factory=lambda: ["6","7","8","9","10","11","12"], description="Available sizes")
    in_stock: bool = Field(True, description="Whether product is in stock")

class Review(BaseModel):
    """Reviews collection schema (collection: "review")"""
    product_id: str = Field(..., description="Related product ObjectId as string")
    name: str = Field(..., description="Reviewer name")
    rating: int = Field(..., ge=1, le=5, description="Star rating 1-5")
    comment: Optional[str] = Field(None, description="Review text")

class Collection(BaseModel):
    """Collections like Men, Women, Kids (collection: "collection")"""
    name: str
    slug: str
    image: str = Field(..., description="Hero / lifestyle image URL")
    description: Optional[str] = None

class Athlete(BaseModel):
    """Ambassadors / community athletes (collection: "athlete")"""
    name: str
    sport: str
    image: str
    bio: Optional[str] = None
    instagram: Optional[str] = None

class Newsletter(BaseModel):
    """Newsletter subscribers (collection: "newsletter")"""
    email: str

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
