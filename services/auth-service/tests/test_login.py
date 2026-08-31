import pytest


@pytest.mark.asyncio
async def test_login_success(client):
    json = {
        "email": "test@test.com",
        "password": "123456789qw",
    }
    response_register = await client.post("/api/v1/auth/register", json=json)
    assert response_register.status_code == 201
    response_login = await client.post("/api/v1/auth/login", json=json)
    assert response_login.status_code == 200
    data = response_login.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    json = {
        "email": "test@test.com",
        "password": "123456789qw",
        }
    json_wrong_password = {
        "email": "test@test.com",
        "password": "wrongPassword",
    }
    response_register = await client.post("/api/v1/auth/register", json=json)
    assert response_register.status_code == 201
    response_login = await client.post("/api/v1/auth/login", json=json_wrong_password)
    assert response_login.status_code == 401
    assert response_login.json()["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_login_nonexistent_email(client):
    json = {
        "email": "nonexistent@test.com",
        "password": "123456789qw",
    }
    response_login = await client.post("/api/v1/auth/login", json=json)
    assert response_login.status_code == 401
    assert response_login.json()["detail"] == "Incorrect email or password"