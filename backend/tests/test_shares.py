from httpx import AsyncClient

from tests.conftest import auth_headers, register


async def _make_notebook(client: AsyncClient, headers: dict[str, str], name: str = "Caderno") -> dict:
    resp = await client.post("/api/v1/notebooks", json={"name": name}, headers=headers)
    return resp.json()


async def _make_page(client: AsyncClient, headers: dict[str, str], notebook_id: int) -> dict:
    resp = await client.post(f"/api/v1/notebooks/{notebook_id}/pages", json={"title": "Notas"}, headers=headers)
    return resp.json()


async def test_owner_shares_notebook_as_viewer(client: AsyncClient) -> None:
    owner_token = await register(client, email="owner@example.com")
    owner_headers = auth_headers(owner_token)
    notebook = await _make_notebook(client, owner_headers)

    viewer_token = await register(client, email="viewer@example.com")

    resp = await client.post(
        f"/api/v1/notebooks/{notebook['id']}/shares",
        json={"email": "viewer@example.com", "permission": "viewer"},
        headers=owner_headers,
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["email"] == "viewer@example.com"
    assert resp.json()["permission"] == "viewer"

    resp = await client.get(f"/api/v1/notebooks/{notebook['id']}", headers=auth_headers(viewer_token))
    assert resp.status_code == 200
    assert resp.json()["role"] == "viewer"

    resp = await client.get("/api/v1/notebooks", headers=auth_headers(viewer_token))
    ids = [nb["id"] for nb in resp.json()]
    assert notebook["id"] in ids


async def test_viewer_cannot_edit_content_or_manage_notebook(client: AsyncClient) -> None:
    owner_token = await register(client, email="owner2@example.com")
    owner_headers = auth_headers(owner_token)
    notebook = await _make_notebook(client, owner_headers)
    page = await _make_page(client, owner_headers, notebook["id"])

    await register(client, email="viewer2@example.com")
    await client.post(
        f"/api/v1/notebooks/{notebook['id']}/shares",
        json={"email": "viewer2@example.com", "permission": "viewer"},
        headers=owner_headers,
    )
    viewer_headers = auth_headers(
        (await client.post("/api/v1/auth/login", json={"email": "viewer2@example.com", "password": "senha1234"})).json()[
            "access_token"
        ]
    )

    # lê conteúdo normalmente
    resp = await client.get(f"/api/v1/pages/{page['id']}", headers=viewer_headers)
    assert resp.status_code == 200

    # não pode editar conteúdo
    content = {"type": "doc", "content": [{"type": "paragraph"}]}
    resp = await client.put(
        f"/api/v1/pages/{page['id']}/content",
        json={"content_json": content, "revision": 1},
        headers=viewer_headers,
    )
    assert resp.status_code == 404

    # não pode criar página
    resp = await client.post(
        f"/api/v1/notebooks/{notebook['id']}/pages", json={"title": "Nova"}, headers=viewer_headers
    )
    assert resp.status_code == 404

    # não pode renomear/gerir tags do caderno
    resp = await client.patch(
        f"/api/v1/notebooks/{notebook['id']}", json={"name": "Hackeado"}, headers=viewer_headers
    )
    assert resp.status_code == 404

    # não pode gerenciar compartilhamentos
    resp = await client.get(f"/api/v1/notebooks/{notebook['id']}/shares", headers=viewer_headers)
    assert resp.status_code == 404


async def test_editor_can_edit_content_and_restore_but_not_manage_notebook(client: AsyncClient) -> None:
    owner_token = await register(client, email="owner3@example.com")
    owner_headers = auth_headers(owner_token)
    notebook = await _make_notebook(client, owner_headers)
    page = await _make_page(client, owner_headers, notebook["id"])

    await register(client, email="editor3@example.com")
    await client.post(
        f"/api/v1/notebooks/{notebook['id']}/shares",
        json={"email": "editor3@example.com", "permission": "editor"},
        headers=owner_headers,
    )
    editor_token = (
        await client.post("/api/v1/auth/login", json={"email": "editor3@example.com", "password": "senha1234"})
    ).json()["access_token"]
    editor_headers = auth_headers(editor_token)

    content = {"type": "doc", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "editado"}]}]}
    resp = await client.put(
        f"/api/v1/pages/{page['id']}/content",
        json={"content_json": content, "revision": 1},
        headers=editor_headers,
    )
    assert resp.status_code == 200

    versions = (await client.get(f"/api/v1/pages/{page['id']}/versions", headers=editor_headers)).json()
    assert len(versions) == 1
    resp = await client.post(
        f"/api/v1/pages/{page['id']}/versions/{versions[0]['id']}/restore", headers=editor_headers
    )
    assert resp.status_code == 200

    # continua sem poder mexer no caderno em si
    resp = await client.delete(f"/api/v1/notebooks/{notebook['id']}", headers=editor_headers)
    assert resp.status_code == 404


async def test_sharing_requires_existing_account(client: AsyncClient) -> None:
    owner_token = await register(client, email="owner4@example.com")
    owner_headers = auth_headers(owner_token)
    notebook = await _make_notebook(client, owner_headers)

    resp = await client.post(
        f"/api/v1/notebooks/{notebook['id']}/shares",
        json={"email": "ninguem@example.com", "permission": "viewer"},
        headers=owner_headers,
    )
    assert resp.status_code == 404


async def test_cannot_share_with_self(client: AsyncClient) -> None:
    owner_token = await register(client, email="owner5@example.com")
    owner_headers = auth_headers(owner_token)
    notebook = await _make_notebook(client, owner_headers)

    resp = await client.post(
        f"/api/v1/notebooks/{notebook['id']}/shares",
        json={"email": "owner5@example.com", "permission": "editor"},
        headers=owner_headers,
    )
    assert resp.status_code == 400


async def test_sharing_twice_updates_permission_instead_of_duplicating(client: AsyncClient) -> None:
    owner_token = await register(client, email="owner6@example.com")
    owner_headers = auth_headers(owner_token)
    notebook = await _make_notebook(client, owner_headers)
    await register(client, email="user6@example.com")

    await client.post(
        f"/api/v1/notebooks/{notebook['id']}/shares",
        json={"email": "user6@example.com", "permission": "viewer"},
        headers=owner_headers,
    )
    await client.post(
        f"/api/v1/notebooks/{notebook['id']}/shares",
        json={"email": "user6@example.com", "permission": "editor"},
        headers=owner_headers,
    )

    resp = await client.get(f"/api/v1/notebooks/{notebook['id']}/shares", headers=owner_headers)
    shares = resp.json()
    assert len(shares) == 1
    assert shares[0]["permission"] == "editor"


async def test_owner_revokes_share(client: AsyncClient) -> None:
    owner_token = await register(client, email="owner7@example.com")
    owner_headers = auth_headers(owner_token)
    notebook = await _make_notebook(client, owner_headers)
    await register(client, email="user7@example.com")

    share = (
        await client.post(
            f"/api/v1/notebooks/{notebook['id']}/shares",
            json={"email": "user7@example.com", "permission": "viewer"},
            headers=owner_headers,
        )
    ).json()

    resp = await client.delete(f"/api/v1/notebooks/{notebook['id']}/shares/{share['id']}", headers=owner_headers)
    assert resp.status_code == 204

    user7_token = (
        await client.post("/api/v1/auth/login", json={"email": "user7@example.com", "password": "senha1234"})
    ).json()["access_token"]
    resp = await client.get(f"/api/v1/notebooks/{notebook['id']}", headers=auth_headers(user7_token))
    assert resp.status_code == 404


async def test_unrelated_user_has_no_access_and_cannot_manage_shares(client: AsyncClient) -> None:
    owner_token = await register(client, email="owner8@example.com")
    owner_headers = auth_headers(owner_token)
    notebook = await _make_notebook(client, owner_headers)

    stranger_token = await register(client, email="stranger8@example.com")
    stranger_headers = auth_headers(stranger_token)

    resp = await client.get(f"/api/v1/notebooks/{notebook['id']}", headers=stranger_headers)
    assert resp.status_code == 404

    resp = await client.post(
        f"/api/v1/notebooks/{notebook['id']}/shares",
        json={"email": "owner8@example.com", "permission": "viewer"},
        headers=stranger_headers,
    )
    assert resp.status_code == 404


async def test_search_includes_shared_notebooks(client: AsyncClient) -> None:
    owner_token = await register(client, email="owner9@example.com")
    owner_headers = auth_headers(owner_token)
    notebook = await _make_notebook(client, owner_headers, "Caderno compartilhado")
    page = await _make_page(client, owner_headers, notebook["id"])
    content = {"type": "doc", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "achavel"}]}]}
    await client.put(
        f"/api/v1/pages/{page['id']}/content",
        json={"content_json": content, "revision": 1},
        headers=owner_headers,
    )

    await register(client, email="viewer9@example.com")
    await client.post(
        f"/api/v1/notebooks/{notebook['id']}/shares",
        json={"email": "viewer9@example.com", "permission": "viewer"},
        headers=owner_headers,
    )
    viewer_token = (
        await client.post("/api/v1/auth/login", json={"email": "viewer9@example.com", "password": "senha1234"})
    ).json()["access_token"]

    resp = await client.get(
        "/api/v1/search", params={"q": "achavel"}, headers=auth_headers(viewer_token)
    )
    results = resp.json()
    assert len(results) == 1
    assert results[0]["notebook_id"] == notebook["id"]
