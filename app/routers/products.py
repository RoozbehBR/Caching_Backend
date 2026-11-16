import json
import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_product, get_all_products
from app.database import get_db
from app.redis_client import get_redis
from app.schemas import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])

# کلیدی که دیتای لیست محصولات رو توی Redis با اون ذخیره می‌کنیم
CACHE_KEY_ALL_PRODUCTS = "all_products"


@router.post("/", response_model=ProductResponse, status_code=http_status.HTTP_201_CREATED)
async def add_new_product(
    product_data: ProductCreate, 
    db: AsyncSession = Depends(get_db),
    cache: aioredis.Redis = Depends(get_redis)
):
    # ۱. محصول رو توی دیتابیس ذخیره می‌کنیم
    new_product = await create_product(db, product_data)
    
    # ۲. مهم‌ترین بخش: کش رو پاک می‌کنیم! (چون لیست محصولات تغییر کرد و کش دیگه قدیمیه)
    await cache.delete(CACHE_KEY_ALL_PRODUCTS)
    
    return new_product


@router.get("/", response_model=list[ProductResponse])
async def list_all_products(
    db: AsyncSession = Depends(get_db),
    cache: aioredis.Redis = Depends(get_redis)
):
    # ۱. اول از همه می‌ریم سراغ Redis (کش)
    cached_products = await cache.get(CACHE_KEY_ALL_PRODUCTS)
    
    # ۲. اگر داده توی کش بود (Cache Hit)
    if cached_products:
        print("✅ داده از Redis خونده شد (فوق‌العاده سریع)")
        # چون دیتا به صورت JSON رشته‌ای ذخیره شده، باید تبدیلش کنیم به لیست پایتونی
        return json.loads(cached_products)

    # ۳. اگر توی کش نبود (Cache Miss)، میریم سراغ دیتابیس
    print("❌ داده توی کش نبود، از دیتابیس خونده میشه (کمی کندتر)")
    products_from_db = await get_all_products(db)

    # ۴. حالا باید نتیجه دیتابیس رو توی Redis ذخیره کنیم تا دفعه بعد سریع باشه
    # برای این کار باید دیتا رو به JSON تبدیل کنیم
    products_json = json.dumps([
        ProductResponse.model_validate(product).model_dump(mode="json") 
        for product in products_from_db
    ])

    # ۳۰ ثانیه (setex) زمان می‌دیم که توی کش بمونه
    await cache.setex(CACHE_KEY_ALL_PRODUCTS, 30, products_json)

    return products_from_db