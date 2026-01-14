from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date


class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    department: Optional[str] = None
    role: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    department: Optional[str] = None
    role: Optional[str] = None


class Employee(EmployeeBase):
    id: int
    date_joined: date

    class Config:
        from_attributes = True
