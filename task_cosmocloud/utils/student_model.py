from pydantic import BaseModel
from typing import Optional,List

class AddressModel(BaseModel):
    city: str
    country: str

class StudentCreateModel(BaseModel):
    name: str
    age: int
    address: AddressModel

class StudentResponseModel(BaseModel):
    name: str
    age: int

class StudentListResponse(BaseModel):
    data: List[StudentResponseModel]