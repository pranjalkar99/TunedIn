from fastapi import APIRouter, Path
from typing import List
from fastapi.responses import JSONResponse
from models.schemas import ErrorResponseModel
from utils.exceptions import *
from pydantic import Field
from models.database import users_collection

router = APIRouter()
users = ["Abhishek", "Abhijit", "Abhinav", "Roseline", "Diksha"]

@router.get(
    "/autocomplete-test/{prefix}",
    tags=["Autocomplete API"],
    response_model=List[str],
    summary="Autocomplete suggestions for Question 2., uses predefined list of user",description='Current Test user list has:["Abhishek", "Abhijit", "Abhinav", "Roseline", "Diksha"]'
)
async def autocomplete(prefix: str = Path(..., title="Prefix", description="Prefix for autocomplete", min_length=1, max_length=10)) -> List[str]:
    try:
        suggestions = [user for user in users if user.lower().startswith(prefix.lower())]
        return suggestions
    except Exception as e:
        error = ErrorResponseModel(error="Internal Server Error", code=500, message="An error occurred during autocomplete.")
        return AutoCompleteException(error, e)
    

@router.get(
    "/autocomplete-userdb/{prefix}",
    tags=["Autocomplete API"],
    response_model=List[str],
    summary="Autocomplete suggestions based on first name in db, uses saved users in MongoDb",description='Current Test user db has:["Abhinab", "Abhijit"]. You may register, and add name to db to add more.'
)
async def autocomplete(prefix: str = Path(..., title="Prefix", description="Prefix for autocomplete", min_length=1, max_length=20)) -> List[str]:
    try:
        suggestions = []
        for user in users_collection.find({"first_name": {"$regex": f"^{prefix}"}}):
            suggestions.append(user["first_name"])
        # if not suggestions:
            # return ["hmm"]
        return suggestions

    except Exception as e:
        if not suggestions:
            return {"Not Found"}
        error = ErrorResponseModel(error="Internal Server Error", code=500, message="An error occurred during autocomplete.")
        return AutoCompleteException(error, e)

