from fastapi import FastAPI
from db import Base, engine
from routes.books_crud import router as books_crud_router
from routes.users_crud import router as users_crud_router
from routes.auth import router as auth_router
from routes.votes import router as votes_router
from fastapi.middleware.cors import CORSMiddleware 
import models  # Import models to ensure they are registered with Base

app = FastAPI(title="FastAPI Base", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.include_router(books_crud_router, tags=["books"])
app.include_router(users_crud_router, tags=["users"])
app.include_router(auth_router, tags=["auth"])
app.include_router(votes_router, tags=["votes"])


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
