from pydantic import BaseModel
from typing import Optional, List


# ************* Product Model *************
class NutritionItem(BaseModel):
    name: str
    amount: Optional[str] = None
    dv: Optional[str] = None
    sub_items: Optional[List["NutritionItem"]] = None


class Nutrition(BaseModel):
    serving_size: Optional[str] = None
    items: List[NutritionItem]


class ProductContent(BaseModel):
    features: List[str] = []
    nutrition: Optional[Nutrition] = None
    ingredients: Optional[str] = None
    recyclability: Optional[str] = None


class Product(BaseModel):
    name: str
    url: str
    brand: str
    category: str
    images: Optional[List[str]] = []
    product_size: Optional[str] = None
    product_line: Optional[str] = None
    description: Optional[str] = None
    labels: Optional[List[str]] = None
    contents: Optional[ProductContent] = []
    created_at: Optional[str] = None


# ************* Recipe Model *************
class RecipeStats(BaseModel):
    prep_time: Optional[str]
    cook_time: Optional[str]
    total_time: Optional[str]
    servings: Optional[str]
    skill: Optional[str]


class Recipe(BaseModel):
    brand: str
    title: str
    url: str
    images: List[str]
    description: Optional[str]
    stats: RecipeStats
    ingredients: List[str]
    instructions: List[str]
    tags: List[str]
    created_at: Optional[str] = None


# ************* Article Model *************
class Article(BaseModel):
    title: str
    url: str
    category: Optional[str] = None
    content: Optional[str] = None
    punlished_at: Optional[str] = None
    created_at: Optional[str] = None
