# from fastapi import APIRouter
# from models.schemas import UserSchema, UpdateUserModel, ResponseModel, ErrorResponseModel
# from utils.exceptions import handle_exception
# # from models.database import MongoDB
# from pymongo import MongoDB
# router = APIRouter()
# db = MongoDB()  # Assuming MongoDB connection is set up in the `database.py` module


# @router.post("/users", tags=["Users"], summary="Create a new user")
# async def create_user(user: UserSchema):
#     try:
#         result = db.create_user(user)
#         if result:
#             return ResponseModel(data=result, message="User created successfully.")
#         else:
#             error = ErrorResponseModel(error="User creation failed.", code=500, message="Failed to create a new user.")
#             return handle_exception(error, None)
#     except Exception as e:
#         error = ErrorResponseModel(error="Internal Server Error", code=500, message="An error occurred while creating the user.")
#         return handle_exception(error, e)


# @router.get("/users/{user_id}", tags=["Users"], summary="Get a user by ID")
# async def get_user(user_id: str):
#     try:
#         result = db.get_user(user_id)
#         if result:
#             return ResponseModel(data=result, message="User retrieved successfully.")
#         else:
#             error = ErrorResponseModel(error="User not found.", code=404, message="User with the specified ID not found.")
#             return handle_exception(error, None)
#     except Exception as e:
#         error = ErrorResponseModel(error="Internal Server Error", code=500, message="An error occurred while retrieving the user.")
#         return handle_exception(error, e)


# @router.put("/users/{user_id}", tags=["Users"], summary="Update a user by ID")
# async def update_user(user_id: str, user: UpdateUserModel):
#     try:
#         result = db.update_user(user_id, user)
#         if result:
#             return ResponseModel(data=result, message="User updated successfully.")
#         else:
#             error = ErrorResponseModel(error="User update failed.", code=500, message="Failed to update the user.")
#             return handle_exception(error, None)
#     except Exception as e:
#         error = ErrorResponseModel(error="Internal Server Error", code=500, message="An error occurred while updating the user.")
#         return handle_exception(error, e)


# @router.delete("/users/{user_id}", tags=["Users"], summary="Delete a user by ID")
# async def delete_user(user_id: str):
#     try:
#         result = db.delete_user(user_id)
#         if result:
#             return ResponseModel(data=result, message="User deleted successfully.")
#         else:
#             error = ErrorResponseModel(error="User deletion failed.", code=500, message="Failed to delete the user.")
#             return handle_exception(error, None)
#     except Exception as e:
#         error = ErrorResponseModel(error="Internal Server Error", code=500, message="An error occurred while deleting the user.")
#         return handle_exception(error, e)
