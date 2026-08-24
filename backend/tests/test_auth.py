from httpx import AsyncClient

from tests.conftest import register


async def test_register_and_login(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "ana@example.com", "password": "senha1234"},
    )
    assert resp.status_code == 201
    assert resp.json()["token_type"] == "bearer"
    assert resp.json()["access_token"]

    dup = await client.post(
        "/api/v1/auth/register",
        json={"email": "ana@example.com", "password": "senha1234"},
    )
    assert dup.status_code == 409

    wrong = await client.post(
        "/api/v1/auth/login",
        json={"email": "ana@example.com", "password": "senhaerrada"},
    )
    assert wrong.status_code == 401

    ok = await client.post(
        "/api/v1/auth/login",
        json={"email": "ana@example.com", "password": "senha1234"},
    )
    assert ok.status_code == 200
    assert ok.json()["access_token"]


async def test_password_too_short(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "b@example.com", "password": "curta"},
    )
    assert resp.status_code == 422


async def test_requires_auth(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/notebooks")
    assert resp.status_code == 401


async def test_register_normalizes_email(client: AsyncClient) -> None:
    token = await register(client, email="Case@Example.com")
    assert token
