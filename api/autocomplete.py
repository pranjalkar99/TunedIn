from fastapi import APIRouter
from typing import List
from fastapi.responses import JSONResponse
from models.schemas import ErrorResponseModel
from utils.exceptions import *

router = APIRouter()


users = ["Abhishek", "Abhijit", "Abhinav", "Roseline", "Diksha"]

@router.get("/autocomplete/{prefix}", tags=["Autocomplete"], response_model=List[str], summary="Autocomplete suggestions for Question 2.")
async def autocomplete(prefix: str) -> List[str]:
    try:
        suggestions = [user for user in users if user.lower().startswith(prefix.lower())]
        return JSONResponse(status_code=200, content=suggestions)
    except Exception as e:
        error = ErrorResponseModel(error="Internal Server Error", code=500, message="An error occurred during autocomplete.")
        return AutoCompleteException(error, e)
