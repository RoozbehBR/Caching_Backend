from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# ۱. فیلدهای مشترک محصول
# ==========================================
class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    price: Decimal = Field(..., gt=0, decimal_places=2) # قیمت باید بزرگتر از 0 باشد
    stock: int = Field(default=0, ge=0) # موجودی نمیتواند منفی باشد


# ==========================================
# ۲. ورودی ساخت محصول (Create)
# ==========================================
class ProductCreate(ProductBase):
    pass


# ==========================================
# ۳. خروجی محصول (Response)
# ==========================================
class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)