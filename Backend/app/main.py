from fastapi import FastAPI
from app.config.database import get_database, close_database
import os
from dotenv import load_dotenv
from app.routes.notes import router as note_router
from app.routes.auth import router as auth_router  # <--- Bổ sung import auth router
from contextlib import asynccontextmanager

load_dotenv()
host_url = os.getenv("host")

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_database()
    print("Đã kết nối MongoDB.")
    
    yield
    
    close_database()

app = FastAPI(title="The Project of Group 6", lifespan=lifespan)

app.include_router(note_router, prefix="/api")
app.include_router(auth_router, prefix="/api")  

@app.get("/")
def root():
    return {"message": "Server hoat dong on dinh"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=host_url, port=8000, reload=True)