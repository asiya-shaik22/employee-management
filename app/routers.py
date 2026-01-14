from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from datetime import timedelta
from .database import get_db
from .models import Employee as EmployeeModel
from .schemas import EmployeeCreate, EmployeeUpdate, Employee
from .auth import authenticate_user, get_current_user, create_access_token



# ================= AUTH ROUTES =================

auth_router = APIRouter()


@auth_router.post("/api/token", tags=["Authentication"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=30),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ================= EMPLOYEE ROUTES =================
router = APIRouter(
    prefix="/api/employees",
    tags=["Employees"],
    dependencies=[Depends(get_current_user)]
)

# create employee

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Employee)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    new_employee = EmployeeModel(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        role=employee.role,
    )

    try:
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        return new_employee
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this email already exists"
        )


# get all employees

@router.get("/", response_model=List[Employee])
def list_employees(
    page: int = Query(1, ge=1),
    department: Optional[str] = None,
    role: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(EmployeeModel)

    if department:
        query = query.filter(EmployeeModel.department == department)

    if role:
        query = query.filter(EmployeeModel.role == role)

    page_size = 10
    employees = query.offset((page - 1) * page_size).limit(page_size).all()

    return employees


# Get emp by ID

@router.get("/{employee_id}", response_model=Employee)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} not found"
        )

    return employee


# update employee

@router.put("/{employee_id}", response_model=Employee)
def update_employee(
    employee_id: int,
    updates: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} not found"
        )

    if updates.name is not None:
        employee.name = updates.name
    if updates.department is not None:
        employee.department = updates.department
    if updates.role is not None:
        employee.role = updates.role

    db.commit()
    db.refresh(employee)
    return employee



# Delete employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} not found"
        )

    db.delete(employee)
    db.commit()
    return None
