from fastapi import FastAPI
from database import Base, engine
from routes import order_router
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
