from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date
import re


class EmployeeBase(BaseModel):
    name: str = Field(..., description="Employee name")

    email: EmailStr
    department: Optional[str] = None
    role: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        # 1. Remove leading/trailing spaces
        name = value.strip()

        # 2. Check empty after stripping
        if not name:
            raise ValueError("Name must not be empty or spaces only")

        # 3. Allow only letters and spaces
        if not re.fullmatch(r"[A-Za-z ]+", name):
            raise ValueError("Name must contain only alphabets and spaces")

        return name


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    role: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]):
        if value is None:
            return value

        name = value.strip()

        if not name:
            raise ValueError("Name must not be empty or spaces only")

        if not re.fullmatch(r"[A-Za-z ]+", name):
            raise ValueError("Name must contain only alphabets and spaces")

        return name


class Employee(EmployeeBase):
    id: int
    date_joined: date

    class Config:
        from_attributes = True
