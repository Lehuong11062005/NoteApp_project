from fastapi import FastAPI
# from app.config.database import get_database,close_database
import os
from dotenv import load_dotenv

load_dotenv()
host_url=os.getenv("host")

app=FastAPI(title="The Project of Group 6")

@app.get("/")
def root():
    return {"messsage" : "Server hoat dong on dinh"}

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("main:app",host=host_url,port=8000,reload=True)