from fastapi import FastAPI
from router.auth import auth_router
from database.database import Base
from database.session import engine

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(auth_router)


@app.get("/")
async def main_page():
    return {"message": "Welcome Book CRUD FastAPI"}
