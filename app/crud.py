from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.schemas import ProductCreate


async def create_product(db: AsyncSession, product_data: ProductCreate) -> Product:
    """ساخت محصول جدید در دیتابیس"""
    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock
    )
    
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


async def get_all_products(db: AsyncSession) -> list[Product]:
    """گرفتن لیست همه محصولات از دیتابیس"""
    database_query = select(Product).order_by(Product.id.desc())
    result = await db.execute(database_query)
    return list(result.scalars().all())


async def get_product_by_id(db: AsyncSession, product_id: int) -> Product | None:
    """گرفتن یک محصول خاص با آیدی"""
    database_query = select(Product).where(Product.id == product_id)
    result = await db.execute(database_query)
    return result.scalar_one_or_none()