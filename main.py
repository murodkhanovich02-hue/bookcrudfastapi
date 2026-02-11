from fastapi import FastAPI
from router.auth import auth_router
from router.book import book_router
from database.database import Base
from database.session import engine
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

Base.metadata.create_all(bind=engine)
app = FastAPI()



# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(book_router)


@app.get("/")
async def main_page():
    return {"message": "Welcome Book CRUD FastAPI"}
