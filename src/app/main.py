from fastapi import FastAPI

from .api import routes
from .database import engine, database, metadata


metadata.create_all(engine)
app = FastAPI()

app.include_router(routes.router, prefix="/api/v1", tags=["MindMap"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def get_health() -> dict:
    return {"Health": "Healthy!!"}
