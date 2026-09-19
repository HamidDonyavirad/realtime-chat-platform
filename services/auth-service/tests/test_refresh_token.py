import pytest
from sqlalchemy import select
from datetime import datetime, timedelta,timezone

from app.models.refresh_token import RefreshToken
from app.security.refresh_token import hash_refresh_token


@pytest.mark.asyncio
async def test_valid_refresh_token(client):
    json = {"email": "test@test.com", "password": "123456789"}

    response_register = await client.post("/api/v1/auth/register", json=json)
    assert response_register.status_code == 201
    response_login = await client.post("/api/v1/auth/login", json=json)
    assert response_login.status_code == 200
    data = response_login.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    response_refresh = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert response_refresh.status_code == 200
    data = response_refresh.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["access_token"] != access_token
    assert data["refresh_token"] == refresh_token



@pytest.mark.asyncio
async def test_invalid_refresh_token(client):
    refresh_token = "invalid"
    response_refresh = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert response_refresh.status_code == 401
    assert response_refresh.json()["detail"] == "Invalid refresh token"

@pytest.mark.asyncio
async def test_revoke_refresh(client,db):

    json = {"email": "test@test.com", "password": "123456789"}

    response_register = await client.post("/api/v1/auth/register", json=json)
    assert response_register.status_code == 201
    response_login = await client.post("/api/v1/auth/login", json=json)
    assert response_login.status_code == 200
    data = response_login.json()
    refresh_token = data["refresh_token"]
    result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash== hash_refresh_token(refresh_token)))
    refresh_token_db = result.scalar_one()
    refresh_token_db.is_revoked = True
    await db.commit()
    response_refresh = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert response_refresh.status_code == 401
    assert response_refresh.json()["detail"] == "Refresh token has been revoked"


@pytest.mark.asyncio
async def test_expired_refresh(client,db):

    json = {"email": "test@test.com", "password": "123456789"}

    response_register = await client.post("/api/v1/auth/register", json=json)
    assert response_register.status_code == 201
    response_login = await client.post("/api/v1/auth/login", json=json)
    assert response_login.status_code == 200
    data = response_login.json()
    refresh_token = data["refresh_token"]
    result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == hash_refresh_token(refresh_token)))
    refresh_token_db = result.scalar_one()
    refresh_token_db.expires_at = datetime.now(timezone.utc) - timedelta(days=1)
    await db.commit()
    response_refresh = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert response_refresh.status_code == 401
    assert response_refresh.json()["detail"] == "Refresh token expired"