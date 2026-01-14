from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql import func
from .database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    department = Column(String(50), nullable=True)
    role = Column(String(50), nullable=True)
    date_joined = Column(Date, nullable=False, server_default=func.current_date())
