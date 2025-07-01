from contextlib import asynccontextmanager
import redis.asyncio as redis
from pydantic_settings import BaseSettings
from fastapi import FastAPI, WebSocket


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    ttl: int = 60 * 60  # 1 hour


def build_app(settings: Settings):
    redis_client = redis.from_url(settings.redis_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        # Shutdown - close Redis connection
        await redis_client.aclose()

    app = FastAPI(lifespan=lifespan)

    @app.websocket("/ws")
    async def ws(
        websocket: WebSocket,
    ):
        await websocket.accept()
        await websocket.send_text("Hello world")
        await websocket.close()

    return app


settings = Settings()
app = build_app(settings)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
