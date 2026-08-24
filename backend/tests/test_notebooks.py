from httpx import AsyncClient

from tests.conftest import auth_headers, register


async def test_create_and_list_notebooks(client: AsyncClient) -> None:
    token = await register(client, email="user@example.com")
    headers = auth_headers(token)

    resp = await client.post(
        "/api/v1/notebooks",
        json={"name": "Aulas", "page_mode": "fixed"},
        headers=headers,
    )
    assert resp.status_code == 201
    notebook = resp.json()
    assert notebook["name"] == "Aulas"
    assert notebook["page_mode"] == "fixed"

    resp = await client.get("/api/v1/notebooks", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1


async def test_update_and_delete_notebook(client: AsyncClient) -> None:
    token = await register(client)
    headers = auth_headers(token)
    created = (await client.post("/api/v1/notebooks", json={"name": "X"}, headers=headers)).json()

    resp = await client.patch(
        f"/api/v1/notebooks/{created['id']}",
        json={"name": "Renomeado"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Renomeado"

    resp = await client.delete(f"/api/v1/notebooks/{created['id']}", headers=headers)
    assert resp.status_code == 204

    resp = await client.get("/api/v1/notebooks", headers=headers)
    assert resp.json() == []


async def test_user_isolation(client: AsyncClient) -> None:
    token_a = await register(client, email="a@example.com")
    token_b = await register(client, email="b@example.com")

    notebook_a = (
        await client.post(
            "/api/v1/notebooks", json={"name": "Secreto"}, headers=auth_headers(token_a)
        )
    ).json()

    resp = await client.get(f"/api/v1/notebooks/{notebook_a['id']}", headers=auth_headers(token_b))
    assert resp.status_code == 404

    resp = await client.delete(f"/api/v1/notebooks/{notebook_a['id']}", headers=auth_headers(token_b))
    assert resp.status_code == 404

    resp = await client.get("/api/v1/notebooks", headers=auth_headers(token_b))
    assert resp.json() == []
