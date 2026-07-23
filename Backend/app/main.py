from fastapi import FastAPI
from app.config.database import get_database,close_database
import os
from dotenv import load_dotenv
from app.routes.notes import router as note_router
from contextlib import asynccontextmanager

load_dotenv()
host_url=os.getenv("host")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code chạy khi ứng dụng BẮT ĐẦU
    get_database()
    print("Đã kết nối MongoDB.")
    
    yield
    
    # Code chạy khi ứng dụng DỪNG (Shutdown)
    close_database()

app=FastAPI(title="The Project of Group 6",lifespan=lifespan)

app.include_router(note_router,prefix="/api")

@app.get("/")
def root():
    return {"messsage" : "Server hoat dong on dinh"}

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("main:app",host=host_url,port=8000,reload=True)