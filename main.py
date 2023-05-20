
from fastapi import FastAPI
from api import autocomplete, friend_circle, users

app = FastAPI()

app.include_router(autocomplete.router)
app.include_router(friend_circle.router)
# app.include_router(users.router)