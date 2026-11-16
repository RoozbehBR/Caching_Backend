import redis.asyncio as aioredis
from app.config import settings

# ساخت یک کلاینت (Client) برای اتصال به Redis
redis_client = aioredis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True # این خط خیلی مهمه! باعث میشه دیتاها به جای بایت، به صورت رشته (String) برگردند
)

# یک تابع Dependency برای استفاده در مسیرهای API (مثل کاری که با get_db می‌کردیم)
async def get_redis():
    yield redis_client