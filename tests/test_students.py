from app import app


def test_get_students(client):

    response = client.get("/students/")

    assert response.status_code == 200

def test_create_student(client):

    response = client.post(
        "/students/",
        json={
            "name": "Test Student",
            "age": 21,
            "city": "Hyderabad",
            "course": "IT"
        }
    )

    assert response.status_code == 201

def test_get_student(client):

    # Create a student first
    response = client.post(
        "/students/",
        json={
            "name": "Test Student",
            "age": 21,
            "city": "Hyderabad",
            "course": "IT"
        }
    )

    student_id = response.get_json()["data"]["id"]

    # Get the student
    response = client.get(f"/students/{student_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["data"]["name"] == "Test Student"


def test_get_student_not_found(client):

    response = client.get("/students/9999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["success"] is False
    assert data["message"] == "Student not found"

def test_update_student(client):

    # Create student
    response = client.post(
        "/students/",
        json={
            "name": "Old Name",
            "age": 20,
            "city": "Hyderabad",
            "course": "IT"
        }
    )

    student_id = response.get_json()["data"]["id"]

    # Update student
    response = client.put(
        f"/students/{student_id}",
        json={
            "name": "New Name",
            "age": 21,
            "city": "Warangal",
            "course": "CSE"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["data"]["name"] == "New Name"
    assert data["data"]["age"] == 21
    assert data["data"]["course"] == "CSE"

def test_delete_student(client):

    # Create student
    response = client.post(
        "/students/",
        json={
            "name": "Delete Student",
            "age": 22,
            "city": "Hyderabad",
            "course": "IT"
        }
    )

    student_id = response.get_json()["data"]["id"]

    # Delete student
    response = client.delete(
        f"/students/{student_id}"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["message"] == "Student deleted successfully"

def test_create_student_missing_fields(client):

    response = client.post(
        "/students/",
        json={
            "name": "Test Student"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["message"] == "All fields are required"

def test_create_student_invalid_age(client):

    response = client.post(
        "/students/",
        json={
            "name": "Test Student",
            "age": -5,
            "city": "Hyderabad",
            "course": "IT"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["message"] == "Age must be greater than 0"


def test_create_student_empty_name(client):

    response = client.post(
        "/students/",
        json={
            "name": "",
            "age": 21,
            "city": "Hyderabad",
            "course": "IT"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["message"] == "Name cannot be empty"

def test_search_students(client):

    client.post(
        "/students/",
        json={
            "name": "Rahul",
            "age": 21,
            "city": "Hyderabad",
            "course": "CSE"
        }
    )

    client.post(
        "/students/",
        json={
            "name": "Vamshi",
            "age": 20,
            "city": "Warangal",
            "course": "IT"
        }
    )

    response = client.get("/students/search?name=Rahul")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "Rahul"

def test_sort_students(client):

    client.post(
        "/students/",
        json={
            "name": "Rahul",
            "age": 25,
            "city": "Hyderabad",
            "course": "CSE"
        }
    )

    client.post(
        "/students/",
        json={
            "name": "Vamshi",
            "age": 20,
            "city": "Warangal",
            "course": "IT"
        }
    )

    response = client.get(
        "/students/sort?sort_by=age&order=asc"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True

    ages = [student["age"] for student in data["data"]]

    assert ages == sorted(ages)

def test_paginate_students(client):

    for i in range(5):

        client.post(
            "/students/",
            json={
                "name": f"Student {i}",
                "age": 20 + i,
                "city": "Hyderabad",
                "course": "IT"
            }
        )

    response = client.get(
        "/students/paginate?page=1&per_page=2"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert len(data["data"]["students"]) == 2
    assert data["data"]["current_page"] == 1

def test_invalid_sort_field(client):

    response = client.get(
        "/students/sort?sort_by=salary"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["message"] == "Invalid sort_by field"