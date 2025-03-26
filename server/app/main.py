import asyncio
from fastapi import FastAPI
from app.routes import router
from app.database import engine, Base, init_db
from app.models import IPO

app = FastAPI()


app.include_router(router)

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the IPO Analysis Backend!"}

# Sample API Endpoint
@app.get("/ipo/{ipo_name}")
def get_ipo_details(ipo_name: str):
    return {"ipo_name": ipo_name, "status": "Upcoming"}