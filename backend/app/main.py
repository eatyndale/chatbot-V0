from fastapi import FastAPI
from app.router import auth
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
