import os
from fastapi import FastAPI
from app.config.database import get_database, close_database
from dotenv import load_dotenv
from app.routes.notes import router as note_router
from app.routes.auth import router as auth_router
from contextlib import asynccontextmanager

load_dotenv()
host_url = os.getenv("host", "127.0.0.1")

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_database()
    print("[OK] MongoDB connected.")
    
    yield
    
    close_database()

app = FastAPI(title="NoteApp API - Group 6", lifespan=lifespan)

# Auth routers (no upload for this branch)
app.include_router(note_router, prefix="/api")
app.include_router(auth_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Server FastAPI hoat dong on dinh"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=host_url, port=8000, reload=True)