
import uuid

from app import create_app


def test_authentication_flow():

    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    unique_id = uuid.uuid4().hex[:8]
    username = f"testuser_{unique_id}"
    email = f"test_{unique_id}@example.com"
    password = "TestPassword123!"

    # Registration
    response = client.post(
        "/register",
        data={
            "username": username,
            "email": email,
            "password": password
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Registration successful" in response.data

    # Duplicate registration
    response = client.post(
        "/register",
        data={
            "username": username,
            "email": email,
            "password": password
        },
        follow_redirects=True
    )

    assert b"already exists" in response.data

    # Incorrect password
    response = client.post(
        "/login",
        data={
            "username": username,
            "password": "WrongPassword123!"
        },
        follow_redirects=True
    )

    assert b"Invalid username or password" in response.data

    # Correct login
    response = client.post(
        "/login",
        data={
            "username": username,
            "password": password
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Student Dashboard" in response.data

    # Logout
    response = client.get(
        "/logout",
        follow_redirects=True
    )

    assert b"Welcome Back" in response.data


def test_registration_validation_and_protected_pages():

    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    # Missing fields
    response = client.post(
        "/register",
        data={
            "username": "",
            "email": "",
            "password": ""
        },
        follow_redirects=True
    )

    assert b"All fields are required" in response.data

    # Short username
    response = client.post(
        "/register",
        data={
            "username": "ab",
            "email": "student@example.com",
            "password": "Password123!"
        },
        follow_redirects=True
    )

    assert b"Username must be between 3 and 30 characters" in response.data

    # Weak password
    response = client.post(
        "/register",
        data={
            "username": "student_test",
            "email": "student@example.com",
            "password": "123"
        },
        follow_redirects=True
    )

    assert b"Password must contain at least 8 characters" in response.data

    # Dashboard protection
    response = client.get(
        "/dashboard",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Welcome Back" in response.data

def test_additional_registration_validation():

    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    # Invalid username characters
    response = client.post(
        "/register",
        data={
            "username": "student@123",
            "email": "student@example.com",
            "password": "Password123!"
        },
        follow_redirects=True
    )

    assert b"Username can contain only letters, numbers and underscores" in response.data

    # Password exceeding maximum length
    response = client.post(
        "/register",
        data={
            "username": "student_test",
            "email": "student@example.com",
            "password": "A" * 129
        },
        follow_redirects=True
    )

    assert b"Password cannot exceed 128 characters" in response.data
