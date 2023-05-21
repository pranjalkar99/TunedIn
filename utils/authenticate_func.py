from fastapi import FastAPI, HTTPException
import jwt
from models.database import users_collection
# from utils.authenticate_func import check_hash_password
import bcrypt
# generating the salt
salt = bcrypt.gensalt()
# Hash the password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Check if the provided password matches the hashed password
def check_hash_password(user_password, hashed_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

SECRET_KEY = "pranjalkar99"
def generate_token(username: str):
    token_data = {"username": username}
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
    return token
# Authenticate the user
def authenticate_user(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username.")
    hashed_password = user["password"]
    if not check_hash_password(password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password.")
    return True
