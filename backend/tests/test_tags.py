from httpx import AsyncClient

from tests.conftest import auth_headers, register


async def _make_notebook(client: AsyncClient, headers: dict[str, str], name: str = "Caderno") -> dict:
    resp = await client.post("/api/v1/notebooks", json={"name": name}, headers=headers)
    return resp.json()


async def test_set_tags_normalizes_trims_and_dedupes(client: AsyncClient) -> None:
    token = await register(client)
    headers = auth_headers(token)
    notebook = await _make_notebook(client, headers)

    resp = await client.patch(
        f"/api/v1/notebooks/{notebook['id']}",
        json={"tags": [" Trabalho ", "trabalho", "Pessoal"]},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["tags"] == ["pessoal", "trabalho"]

    resp = await client.get(f"/api/v1/notebooks/{notebook['id']}", headers=headers)
    assert resp.json()["tags"] == ["pessoal", "trabalho"]


async def test_list_tags_and_clear(client: AsyncClient) -> None:
    token = await register(client)
    headers = auth_headers(token)
    notebook = await _make_notebook(client, headers)

    await client.patch(
        f"/api/v1/notebooks/{notebook['id']}", json={"tags": ["estudo"]}, headers=headers
    )
    resp = await client.get("/api/v1/tags", headers=headers)
    assert [t["name"] for t in resp.json()] == ["estudo"]

    resp = await client.patch(
        f"/api/v1/notebooks/{notebook['id']}", json={"tags": []}, headers=headers
    )
    assert resp.json()["tags"] == []


async def test_filter_notebooks_by_tag(client: AsyncClient) -> None:
    token = await register(client)
    headers = auth_headers(token)
    tagged = await _make_notebook(client, headers, "Com tag")
    untagged = await _make_notebook(client, headers, "Sem tag")
    await client.patch(
        f"/api/v1/notebooks/{tagged['id']}", json={"tags": ["trabalho"]}, headers=headers
    )

    resp = await client.get("/api/v1/notebooks", params={"tag": "trabalho"}, headers=headers)
    ids = [nb["id"] for nb in resp.json()]
    assert ids == [tagged["id"]]
    assert untagged["id"] not in ids


async def test_tags_isolated_between_users(client: AsyncClient) -> None:
    token_a = await register(client, email="a@example.com")
    notebook_a = await _make_notebook(client, auth_headers(token_a))
    await client.patch(
        f"/api/v1/notebooks/{notebook_a['id']}", json={"tags": ["secreto"]}, headers=auth_headers(token_a)
    )

    token_b = await register(client, email="b@example.com")
    resp = await client.get("/api/v1/tags", headers=auth_headers(token_b))
    assert resp.json() == []
