import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# -----------------------
# Helpers
# -----------------------

def get_auth_token():
    response = client.post(
        "/api/token",
        data={
            "username": "admin",
            "password": "admin123"
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def auth_headers():
    token = get_auth_token()
    return {"Authorization": f"Bearer {token}"}


# -----------------------
# Authentication tests
# -----------------------

def test_login_success():
    response = client.post(
        "/api/token",
        data={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure():
    response = client.post(
        "/api/token",
        data={"username": "admin", "password": "wrong"}
    )
    assert response.status_code == 401


# -----------------------
# Create Employee
# -----------------------

def test_create_employee_success():
    response = client.post(
        "/api/employees/",
        json={
            "name": "John Doe",
            "email": "john.doe@test.com",
            "department": "Engineering",
            "role": "Developer"
        },
        headers=auth_headers()
    )
    assert response.status_code == 201
    assert response.json()["email"] == "john.doe@test.com"


def test_create_employee_duplicate_email():
    response = client.post(
        "/api/employees/",
        json={
            "name": "Duplicate User",
            "email": "john.doe@test.com",
            "department": "HR",
            "role": "Manager"
        },
        headers=auth_headers()
    )
    assert response.status_code == 400


# -----------------------
# List Employees
# -----------------------

def test_list_employees():
    response = client.get(
        "/api/employees/",
        headers=auth_headers()
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# -----------------------
# Get Employee by ID
# -----------------------

def test_get_employee_success():
    # first list to get an ID
    response = client.get("/api/employees/", headers=auth_headers())
    employee_id = response.json()[0]["id"]

    response = client.get(
        f"/api/employees/{employee_id}",
        headers=auth_headers()
    )
    assert response.status_code == 200
    assert response.json()["id"] == employee_id


def test_get_employee_not_found():
    response = client.get(
        "/api/employees/999999",
        headers=auth_headers()
    )
    assert response.status_code == 404


# -----------------------
# Update Employee
# -----------------------

def test_update_employee_success():
    response = client.get("/api/employees/", headers=auth_headers())
    employee_id = response.json()[0]["id"]

    response = client.put(
        f"/api/employees/{employee_id}",
        json={"role": "Senior Developer"},
        headers=auth_headers()
    )
    assert response.status_code == 200
    assert response.json()["role"] == "Senior Developer"


def test_update_employee_not_found():
    response = client.put(
        "/api/employees/999999",
        json={"role": "Manager"},
        headers=auth_headers()
    )
    assert response.status_code == 404


# -----------------------
# Delete Employee
# -----------------------

def test_delete_employee_success():
    response = client.get("/api/employees/", headers=auth_headers())
    employee_id = response.json()[0]["id"]

    response = client.delete(
        f"/api/employees/{employee_id}",
        headers=auth_headers()
    )
    assert response.status_code == 204


def test_delete_employee_not_found():
    response = client.delete(
        "/api/employees/999999",
        headers=auth_headers()
    )
    assert response.status_code == 404

