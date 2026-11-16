from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import String, Text, Numeric, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # قیمت محصول
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    # موجودی انبار
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # زمان ایجاد محصول
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )