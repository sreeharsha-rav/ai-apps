from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from app.services.checkout import CheckoutSession

class Price(BaseModel):
    model_config = ConfigDict(extra='allow')
    amount: float
    currency: str

class PriceRange(BaseModel):
    model_config = ConfigDict(extra='allow')
    min: Optional[Price] = None
    max: Optional[Price] = None

class Media(BaseModel):
    model_config = ConfigDict(extra='allow')
    url: str
    altText: Optional[str] = None

class Shop(BaseModel):
    model_config = ConfigDict(extra='allow')
    id: str
    name: str
    onlineStoreUrl: Optional[str] = None

class Variant(BaseModel):
    model_config = ConfigDict(extra='allow')
    id: str
    productId: Optional[str] = None
    displayName: Optional[str] = None
    availableForSale: bool = True
    price: Optional[Price] = None
    media: List[Media] = []
    options: List[dict] = []
    shop: Optional[Shop] = None
    variantUrl: Optional[str] = None
    checkoutUrl: Optional[str] = None
    secondhand: Optional[bool] = None
    lookupUrl: Optional[str] = None

class Product(BaseModel):
    model_config = ConfigDict(extra='allow')
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    uniqueSellingPoint: Optional[str] = None
    topFeatures: List[str] = []
    techSpecs: List[str] = []
    attributes: List[dict] = []
    media: List[Media] = []
    priceRange: Optional[PriceRange] = None
    lookupUrl: Optional[str] = None
    variants: List[Variant] = []

class ShoppingContext(BaseModel):
    model_config = ConfigDict(extra='allow')
    products: List[Product] = Field(
        default=[],
        description="List of products in the shopping context"
    )
    product_details: Optional[Product] = Field(
        default=None,
        description="Details of a specific product"
    )
    checkout_session: Optional[CheckoutSession] = Field(
        default=None,
        description="Current checkout session state"
    )