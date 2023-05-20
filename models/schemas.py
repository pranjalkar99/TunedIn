from typing import List, Optional, Tuple, Any, Dict
from pydantic import BaseModel, EmailStr, Field

class EducationDetails(BaseModel):
    school_name: str
    board: str
    year_of_completion: int

class InternshipDetails(BaseModel):
    company_name: str
    role: str
    start_date: str
    end_date: str

class UserSchema(BaseModel):
    username: str
    password: str
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    date_of_birth: Optional[str] = ""
    education_details: Optional[List[EducationDetails]] = []
    email: Optional[EmailStr] = ""
    contact_no: Optional[str] = ""
    skills: Optional[List[str]] = []
    internships: Optional[List[InternshipDetails]] = []
    year_of_joining_tu: Optional[int] = None
    expected_year_of_completion: Optional[int] = None
    department: Optional[str] = ""
    course: Optional[str] = ""
    current_semester: Optional[str] = ""
    bio: Optional[str] = ""
    residence: Optional[str] = ""
    hostel: Optional[str] = ""

class GraphInput(BaseModel):
    graph_edges_list: List[Tuple]
    check_friends: Tuple[str, str]


class UpdateUserModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    education_details: Optional[List[EducationDetails]] = None
    email: Optional[EmailStr] = None
    contact_no: Optional[str] = None
    skills: Optional[List[str]] = None
    internships: Optional[List[InternshipDetails]] = None
    year_of_joining_tu: Optional[int] = None
    expected_year_of_completion: Optional[int] = None
    department: Optional[str] = None
    course: Optional[str] = None
    current_semester: Optional[str] = None
    bio: Optional[str] = None
    residence: Optional[str] = None
    hostel: Optional[str] = None

class UserUpdateRequest(BaseModel):
    username: str
    updated_data: UpdateUserModel


class ErrorResponseModel(BaseModel):
    error: str = Field(..., description="Error message")
    code: int = Field(..., description="Error code")
    message: str = Field(..., description="Error description")

class ResponseModel:
    def __init__(self, data: Any, message: str):
        self.data = data
        self.message = message
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "message": self.message
        }