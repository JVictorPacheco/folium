from httpx import AsyncClient

from tests.conftest import auth_headers, register


async def _make_notebook(client: AsyncClient, token: str) -> int:
    resp = await client.post("/api/v1/notebooks", json={"name": "Caderno"}, headers=auth_headers(token))
    return resp.json()["id"]


async def test_page_lifecycle(client: AsyncClient) -> None:
    token = await register(client)
    headers = auth_headers(token)
    notebook_id = await _make_notebook(client, token)

    resp = await client.post(
        f"/api/v1/notebooks/{notebook_id}/pages",
        json={"title": "Página 1"},
        headers=headers,
    )
    assert resp.status_code == 201
    page = resp.json()
    assert page["position"] == 1
    assert page["revision"] == 1

    resp = await client.get(f"/api/v1/notebooks/{notebook_id}/pages", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = await client.delete(f"/api/v1/pages/{page['id']}", headers=headers)
    assert resp.status_code == 204


async def test_content_autosave_and_revision(client: AsyncClient) -> None:
    token = await register(client)
    headers = auth_headers(token)
    notebook_id = await _make_notebook(client, token)
    page = (
        await client.post(
            f"/api/v1/notebooks/{notebook_id}/pages", json={"title": "Notas"}, headers=headers
        )
    ).json()

    content = {"type": "doc", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "oi"}]}]}

    resp = await client.put(
        f"/api/v1/pages/{page['id']}/content",
        json={"content_json": content, "revision": 1},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["revision"] == 2

    # reenvio com revisão antiga -> conflito
    resp = await client.put(
        f"/api/v1/pages/{page['id']}/content",
        json={"content_json": content, "revision": 1},
        headers=headers,
    )
    assert resp.status_code == 409

    # leitura reflete o conteúdo salvo
    resp = await client.get(f"/api/v1/pages/{page['id']}", headers=headers)
    assert resp.json()["content_json"] == content
    assert resp.json()["revision"] == 2
