import pytest
from sqlalchemy import select

from app.models.user import User

@pytest.mark.asyncio
async def test_register_success(client):
    json = {
        "email": "test@test.com",
        "password": "123456789qw",
    }

    response = await client.post("/api/v1/auth/register", json=json)
    assert response.status_code == 201
    data = response.json()

    assert data["email"] == "test@test.com"
    assert data["is_active"] is True
    assert data["is_verified"] is False

    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
        json = {
            "email":"test1@test.com",
            "password":"123456789po",
        }
        response = await client.post("/api/v1/auth/register", json=json)
        assert response.status_code == 201
        response = await client.post("/api/v1/auth/register", json=json)
        assert response.status_code == 409
        assert response.json() == {"detail": "Email already registered"}


@pytest.mark.asyncio
async def test_register_invalid_email(client):
    json = {
        "email":"not-an-email",
        "password":"strong123",
    }
    response = await client.post("/api/v1/auth/register", json=json)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_short_password(client):
    json = {
        "email":"test@test.com",
        "password":"123",
    }
    response = await client.post("/api/v1/auth/register", json=json)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_password_is_hashed(client,db):
    json = {
        "email":"test@test.com",
        "password":"123456789",
    }
    response = await client.post("/api/v1/auth/register", json=json)
    assert response.status_code == 201

    result = await db.execute(
        select(User).where(User.email == json["email"])
    )
    user = result.scalar_one()
    assert user.hashed_password != json["password"]