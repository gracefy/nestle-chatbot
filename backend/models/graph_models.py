from pydantic import BaseModel
from typing import Optional, List


class BrandNode(BaseModel):
    name: str
    url: Optional[str] = None
    image: Optional[str] = None


class ProductNode(BaseModel):
    name: str
    brand: str
    url: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    product_size: Optional[str] = None
    product_line: Optional[str] = None
    label: Optional[str] = None


class HasProductEdge(BaseModel):
    from_brand: str  # Brand.name
    to_product: str  # Product.name
    type: str = "HAS_PRODUCT"
