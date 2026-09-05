import pytest



@pytest.mark.asyncio
async def test_get_me_authenticated(client):
    json = {
        "email": "test@test.com",
        "password": "123456789"
    }
    response_signup = await client.post("/api/v1/auth/register", json=json)
    assert response_signup.status_code == 201
    response_login = await client.post("/api/v1/auth/login", json=json)
    assert response_login.status_code == 200
    token = response_login.json()["access_token"]

    response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == json["email"]
    assert data["is_active"] is True
    assert "id" in data



@pytest.mark.asyncio
async def test_get_me_without_token(client):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_me_invalid_token(client):
    response = await client.get("/api/v1/users/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
