
from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from enum import Enum
from pathlib import Path
from typing import List, Optional
from models.schemas import UserSchema, ResponseModel, ErrorResponseModel
from utils.exceptions import handle_exception
from models.database import users_collection
from utils.authenticate_func import authenticate_user,generate_token,hash_password, check_hash_password
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from models.schemas import District, Hostel
from pydantic import BaseModel, EmailStr
# # from models.database import MongoDB
from pymongo import MongoClient
router = APIRouter()
import re
security = HTTPBasic()
from passlib.context import CryptContext

# security = HTTPBasic()
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_hashed_password(password):
#     return pwd_context.hash(password)

# def authenticate_user(credentials: HTTPBasicCredentials):
#     user = users_collection.find_one({"username": credentials.username})
#     if not user or not verify_password(credentials.password, user["password"]):
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid username or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return user




@router.post("/register",tags=["User"], summary="Signup new user into the App")
async def register(username: str, password: str):
    regex = ("^(?=.*[a-z])(?=." +
             "*[A-Z])(?=.*\\d)" +
             "(?=.*[-+_!@#$%^&*., ?]).+$")
    p = re.compile(regex)
    
    if (password == None):
        raise HTTPException(status_code=400, detail="Please enter characters in your password string.")
    elif not (re.search(p, password)):
       raise HTTPException(status_code=400, detail="Use atleast 1 uppercase, one lower case, one special character, and a number in your password.") 
    elif users_collection.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Oops, Username already exists... Login Again to use")
    elif len(list(password))<8:
        raise HTTPException(status_code=400, detail="Please enter the password with atleast 8  characters.")
    else:
        user = {"username": username, "password": hash_password(password)}
        users_collection.insert_one(user)
    return {"message": "User registered successfully.Added to db."}


@router.post("/login",tags=["User"], summary=" JWT Token based Secure Login for existing users")
async def login(username:str, password:str):#,credentials: HTTPBasicCredentials = Depends(security) ):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    # Generate the JWT token
    token = generate_token(username)
    
    # Return the token as the response
    
    result= {"token": token, "message" : "Login Successful"}
    return ResponseModel(data=result, message="Logged in check successful.")

@router.put("/update-details",tags=["User"], summary=" Update details for existing users")
async def update_profile(
    username: str,
    password: str,
    first_name: Optional[str] = "",
    last_name: Optional[str] = "",
    date_of_birth: Optional[str] = "",
    education_details: Optional[List[str]] = [],
    email: Optional[EmailStr] = "",
    contact_no: Optional[str] = "",
    skills: Optional[List[str]] = [],
    internships: Optional[List[str]] = [],
    year_of_joining_tu: Optional[int] = None,
    district: Optional[District] = None,
    hostel: Optional[Hostel] = None,
    expected_year_of_completion: Optional[int] = None,
    department: Optional[str] = "",
    course: Optional[str] = "",
    current_semester: Optional[str] = "",
    bio: Optional[str] = "",
    residence: Optional[str] = "",
    #credentials: HTTPBasicCredentials = Depends(security)
):# ,token:str):
    user = users_collection.find_one({"username": username})
    if user is None:
        return JSONResponse(
        status_code=500,
        content = {
            "message": "user doesn't exist"
        }
    )
    auth_user = authenticate_user(user.get("username"), password)
    if not auth_user:
        return JSONResponse(
            status_code=401, 
            content = {
                "message" : "Incorrect Password..."
            }
        )
    user = users_collection.find_one({"username": username})
    if user is None:
        return JSONResponse(
            status_code=404,
            content={
                "message": "User doesn't exist"
            }
        )

    try:
        user["first_name"] = first_name or user.get("first_name")
        user["last_name"] = last_name or user.get("last_name")
        user["date_of_birth"] = date_of_birth or user.get("date_of_birth")
        user["education_details"] = education_details or user.get("education_details")
        user["email"] = email or user.get("email")
        user["contact_no"] = contact_no or user.get("contact_no")
        user["skills"] = skills or user.get("skills")
        user["internships"] = internships or user.get("internships")
        user["year_of_joining_tu"] = year_of_joining_tu or user.get("year_of_joining_tu")
        user["district"] = district or user.get("district")
        user["hostel"] = hostel or user.get("hostel")
        user["expected_year_of_completion"] = expected_year_of_completion or user.get("expected_year_of_completion")
        user["department"] = department or user.get("department")
        user["course"] = course or user.get("course")
        user["current_semester"] = current_semester or user.get("current_semester")
        user["bio"] = bio or user.get("bio")
        user["residence"] = residence or user.get("residence")
        user["hostel"] = hostel or user.get("hostel")

        users_collection.replace_one({"username": user.get("username")}, user)

        return JSONResponse(
            status_code=200,
            content={
                "message": "success"
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error",
                "error": str(e)
            }
        )
@router.delete("/delete_user", tags=["User"], summary=" Delete existing user")
def delete_user(username:str, password:str):#,credentials: HTTPBasicCredentials = Depends(security)):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password., or maybe user does not exist")
    result = users_collection.delete_one({"username": username, "password": password})
    # info_data = {'username':credentials.username}
    # result = users_collection.delete_many(info_data)
    # if result.deleted_count == 0:
    #     raise HTTPException(status_code=404, detail="User not found.")
    if result:
        return JSONResponse(
                status_code=201,
                content={
                    "message": "Deleted Requested User Successfullky.",
                }
            )
    else:
        return JSONResponse(
                status_code=404,
                content={
                    "message": "User does not exist.",
                }
            )


@router.get("/get-details",tags=["User"], summary=" Get details for existing users")
async def get_profile(username:str, password:str):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    users_cursor = users_collection.find_one({"username": username})
    # return user
    # users = []
    if users_cursor:
        users_cursor["_id"] = str(users_cursor["_id"])  # Convert ObjectId to string
        return {"users": [users_cursor]}
    else:
        return {"message": "User not found"}


@router.post("/upload-resume", tags=["User"], summary="Upload a resume file")
async def upload_resume(username:str, password:str,resume_file: UploadFile = File(...)):
    user = authenticate_user(username, password)
    # Create a unique filename for the resume
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    resume_path = Path("resumes") / resume_file.filename

    # Save the resume file to the specified path
    with open(resume_path, "wb") as file:
        contents = await resume_file.read()
        file.write(contents)
    # Update the user's resume field in the database
    users_collection.update_one(
        {"username": username},
        {"$set": {"resume": str(resume_path)}}
    )

    return {"message": "Resume uploaded successfully."}



@router.post("/send-connection-request/{from_user}/{to_user}", tags=["Connections"], summary="Send connection request to another user")
async def send_connection_request(from_user: str, to_user: str):
    # Check if both users exist in the database
    from_user_data = users_collection.find_one({"username": from_user})
    to_user_data = users_collection.find_one({"username": to_user})
    if not from_user_data or not to_user_data:
        raise HTTPException(status_code=404, detail="One or both users not found.")

    # Add the connection request to the from_user's connections list
    users_collection.update_one(
        {"username": from_user},
        {"$addToSet": {"connections": to_user}}
    )

    return {"message": "Connection request sent successfully."}


@router.put("/accept-connection-request/{from_user}/{to_user}", tags=["Connections"], summary="Accept connection request from another user")
async def accept_connection_request(from_user: str, to_user: str):
    # Check if both users exist in the database
    from_user_data = users_collection.find_one({"username": from_user})
    to_user_data = users_collection.find_one({"username": to_user})
    if not from_user_data or not to_user_data:
        raise HTTPException(status_code=404, detail="One or both users not found.")

    # Check if the connection request exists in the from_user's connections list
    if to_user not in from_user_data.get("connections", []):
        raise HTTPException(status_code=400, detail="Connection request not found.")

    # Add both users to each other's connections list
    users_collection.update_one(
        {"username": from_user},
        {"$addToSet": {"connections": to_user}}
    )
    users_collection.update_one(
        {"username": to_user},
        {"$addToSet": {"connections": from_user}}
    )

    return {"message": "Connection request accepted successfully."}




@router.get("/users/search", tags=["User"], summary="Search other users by criteria")
async def search_users(name: str = None, semester: str = None, department: str = None, program: str = None,
                       hostel: str = None, residence: str = None, skills: str = None):
    query = {}
    if name:
        query["name"] = {"$regex": f".*{name}.*", "$options": "i"}
    if semester:
        query["current_semester"] = semester
    if department:
        query["department"] = department
    if program:
        query["program"] = program
    if hostel:
        query["hostel"] = hostel
    if residence:
        query["residence"] = residence
    if skills:
        query["skills"] = {"$in": [skill.strip() for skill in skills.split(",")]}

    users_cursor = users_collection.find(query)
    # return {"users": users}
    users = []

    for user in users_cursor:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        users.append(user)

    return {"users": users} 



  # ## Assuming user has been authenticated...
    # try:
    #     user["first_name"] = request.first_name or user.get("first_name")
    #     user["last_name"] = request.last_name or user.get("last_name")
    #     user["date_of_birth"] = request.date_of_birth or user.get("date_of_birth")
    #     user["education_details"] = request.education_details or user.get("education_details")
    #     user["email"] = request.email or user.get("email")
    #     user["contact_no"] = request.contact_no or user.get("contact_no")
    #     user["skills"] = request.skills or user.get("skills")
    #     user["internships"] = request.internships or user.get("internships")
    #     user["year_of_joining_tu"] = request.year_of_joining_tu or user.get("year_of_joining_tu")
    #     user["expected_year_of_completion"] = request.expected_year_of_completion or user.get("expected_year_of_completion")
    #     user["department"] = request.department or user.get("department")
    #     user["course"] = request.course or user.get("course")
    #     user["current_semester"] = request.current_semester or user.get("current_semester")
    #     user["bio"] = request.bio or user.get("bio")
    #     user["residence"] = request.residence or user.get("residence")
    #     user["district"] = request.district or user.get("district")
    #     user["hostel"] = request.hostel or user.get("hostel")

    #     # Save the updated user details
    #     users_collection.replace_one({"username": user["username"]}, user)
    #     # await user.save()

    #     return JSONResponse(
    #         status_code=200, 
    #         content = {
    #             "message" : "success"
    #         }
    #     )

    # except Exception as e:
    #     return JSONResponse(
    #             status_code=500, 
    #             content = {
    #                 "message" : "error",
    #                 "error" : str(e)})

        


