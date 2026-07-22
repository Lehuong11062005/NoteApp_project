from fastapi import FastAPI
# from app.config.database import get_database,close_database
import os
from dotenv import load_dotenv

<<<<<<< HEAD
# 1. Import file auth.py từ thư mục routes
from app.routes import auth 

=======
>>>>>>> 2db6bcaa98c79f9581031568735fa75e7ee61a90
load_dotenv()
host_url=os.getenv("host")

app=FastAPI(title="The Project of Group 6")

<<<<<<< HEAD
# 2. Đăng ký router auth vào app
app.include_router(auth.router)

=======
>>>>>>> 2db6bcaa98c79f9581031568735fa75e7ee61a90
@app.get("/")
def root():
    return {"messsage" : "Server hoat dong on dinh"}

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("main:app",host=host_url,port=8000,reload=True)