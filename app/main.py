from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import products


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ساخت جدول‌ها موقع روشن شدن سرور
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Caching API",
    description="سیستم کش کردن با Redis",
    version="0.1.0",
    lifespan=lifespan,
)

# وصل کردن روتر محصولات
app.include_router(products.router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}