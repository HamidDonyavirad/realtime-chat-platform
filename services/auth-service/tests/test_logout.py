import pytest

@pytest.mark.asyncio
async def test_logout_revoke_refresh_token(client:AsyncClient):
    json = {"email":"test@test.com","password":"123456789"}

    response_register = await client.post("/api/v1/auth/register", json=json)
    assert response_register.status_code == 201
    response_login = await client.post("/api/v1/auth/login", json=json)
    assert response_login.status_code == 200
    data = response_login.json()
    refresh_token = data["refresh_token"]

    response_logout = await client.post("/api/v1/auth/logout", json={"refresh_token": refresh_token})
    assert response_logout.status_code == 200
    assert response_logout.json()["message"] == "Successfully logged out"

    response_refresh = await client.post("/api/v1/auth/refresh",json={"refresh_token": refresh_token})
    assert response_refresh.status_code == 401


    
