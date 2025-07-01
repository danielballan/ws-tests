from contextlib import asynccontextmanager
import redis.asyncio as redis
from pydantic_settings import BaseSettings
from fastapi import FastAPI, WebSocket
import random

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

    
    @app.post("/upload")
    async def create():
        "Declare a new dataset."

        # Allocate a counter for this node_id.
        node_id = 999
        await redis_client.setnx(f"seq_num:{node_id}", 0)
        return {"node_id": node_id}

    @app.delete("/upload/{node_id}", status_code=204)
    async def close(node_id):
        "Declare that a dataset is done streaming."

        await redis_client.delete(f"seq_num:{node_id}")
        # TODO: Shorten TTL on all extant data for this node.
        return None

    return app


settings = Settings()
app = build_app(settings)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
