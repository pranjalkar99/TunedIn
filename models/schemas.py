from typing import List, Optional, Tuple, Any, Dict
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class EducationDetails(BaseModel):
    school_name: str
    board: str
    year_of_completion: int

class InternshipDetails(BaseModel):
    company_name: str
    role: str
    start_date: str
    end_date: str
class Hostel(str, Enum):
    CMH = 'cmh'
    PMH = 'pmh'
    NMH = 'nmh'
    KMH = 'kmh'
    NWH = 'nwh'
    JWH = 'jwh'
    BWH = 'bwh'
    PWH = 'pwh'
    KWH = 'kwh'
    SWH = 'swh'
    TMH = 'tmh'
    MWH = 'mwh'
class District(str, Enum):
    JORHAT = 'Jorhat'
    SONITPUR = 'Sonitpur'
    TINSUKIA = 'Tinsukia'
    WEST_KARBI_ANGLONG = 'West Karbi Anglong'
    BARPETA = 'Barpeta'
    CACHAR = 'Cachar'
    CHIRANG = 'Chirang'
    SOUTH_SALMARA_MANKACHAR = 'South Salmara-Mankachar'
    UDALGURI = 'Udalguri'
    BAKSA = 'Baksa'
    BONGAIGAON = 'Bongaigaon'
    CHARAIDEO = 'Charaideo'
    DARRANG = 'Darrang'
    DHUBRI = 'Dhubri'
    DIMA_HASAO = 'Dima Hasao'
    GOLAGHAT = 'Golaghat'
    KAMRUP = 'Kamrup'
    DHEMAJI = 'Dhemaji'
    DIBRUGARH = 'Dibrugarh'
    GOALPARA = 'Goalpara'
    HAILAKANDI = 'Hailakandi'
    KAMRUP_METROPOLITAN = 'Kamrup Metropolitan'
    KARBI_ANGLONG = 'Karbi Anglong'
    KOKRAJHAR = 'Kokrajhar'
    MAJULI = 'Majuli'
    NAGAON = 'Nagaon'
    SIVASAGAR = 'Sivasagar'
    KARIMGANJ = 'Karimganj'
    LAKHIMPUR = 'Lakhimpur'
    MORIGAON = 'Morigaon'
    NALBARI = 'Nalbari'
    

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
    district: Optional[District] = None
    hostel: Optional[Hostel] = None
    resume: Optional[str] = ""
    connections: List[str] = []
    # hostel: Optional[str] = ""

class GraphInput(BaseModel):
    graph_edges_list: List[Tuple]
    check_friends: Tuple[str, str]


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