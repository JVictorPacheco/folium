from httpx import AsyncClient

from app.services import content as content_module
from tests.conftest import auth_headers, register


async def _make_page(client: AsyncClient, token: str) -> tuple[int, int]:
    headers = auth_headers(token)
    notebook = (
        await client.post("/api/v1/notebooks", json={"name": "Caderno"}, headers=headers)
    ).json()
    page = (
        await client.post(
            f"/api/v1/notebooks/{notebook['id']}/pages", json={"title": "Notas"}, headers=headers
        )
    ).json()
    return notebook["id"], page["id"]


async def _save(client: AsyncClient, headers: dict[str, str], page_id: int, revision: int, text: str) -> dict:
    content = {"type": "doc", "content": [{"type": "paragraph", "content": [{"type": "text", "text": text}]}]}
    resp = await client.put(
        f"/api/v1/pages/{page_id}/content",
        json={"content_json": content, "revision": revision},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    return resp.json()


async def test_first_edit_snapshots_previous_content_and_throttles_next(client: AsyncClient) -> None:
    token = await register(client)
    headers = auth_headers(token)
    _, page_id = await _make_page(client, token)

    await _save(client, headers, page_id, 1, "primeira edição")

    resp = await client.get(f"/api/v1/pages/{page_id}/versions", headers=headers)
    assert resp.status_code == 200
    versions = resp.json()
    assert len(versions) == 1
    assert versions[0]["revision"] == 1

    detail = await client.get(f"/api/v1/pages/{page_id}/versions/{versions[0]['id']}", headers=headers)
    assert detail.json()["content_json"] == {}

    # edição imediata seguinte não deve criar outra versão (dentro da janela de 5min)
    await _save(client, headers, page_id, 2, "segunda edição")
    resp = await client.get(f"/api/v1/pages/{page_id}/versions", headers=headers)
    assert len(resp.json()) == 1


async def test_snapshot_after_throttle_window_elapses(client: AsyncClient, monkeypatch) -> None:
    token = await register(client)
    headers = auth_headers(token)
    _, page_id = await _make_page(client, token)

    await _save(client, headers, page_id, 1, "primeira edição")

    monkeypatch.setattr(content_module, "SNAPSHOT_THROTTLE_MINUTES", 0)
    await _save(client, headers, page_id, 2, "segunda edição")

    resp = await client.get(f"/api/v1/pages/{page_id}/versions", headers=headers)
    assert len(resp.json()) == 2


async def test_restore_reverts_content_and_snapshots_current_state(client: AsyncClient) -> None:
    token = await register(client)
    headers = auth_headers(token)
    _, page_id = await _make_page(client, token)

    await _save(client, headers, page_id, 1, "primeira edição")
    versions = (await client.get(f"/api/v1/pages/{page_id}/versions", headers=headers)).json()
    original_version_id = versions[0]["id"]

    resp = await client.post(
        f"/api/v1/pages/{page_id}/versions/{original_version_id}/restore", headers=headers
    )
    assert resp.status_code == 200, resp.text
    restored = resp.json()
    assert restored["content_json"] == {}
    assert restored["revision"] == 3  # 1 (create) -> 2 (save) -> 3 (restore)

    resp = await client.get(f"/api/v1/pages/{page_id}/versions", headers=headers)
    versions_after = resp.json()
    assert len(versions_after) == 2  # snapshot original + snapshot pré-restore


async def test_versions_isolated_between_users(client: AsyncClient) -> None:
    token_a = await register(client, email="a@example.com")
    _, page_id = await _make_page(client, token_a)
    await _save(client, auth_headers(token_a), page_id, 1, "conteúdo do usuário A")
    versions = (await client.get(f"/api/v1/pages/{page_id}/versions", headers=auth_headers(token_a))).json()
    version_id = versions[0]["id"]

    token_b = await register(client, email="b@example.com")
    headers_b = auth_headers(token_b)

    assert (await client.get(f"/api/v1/pages/{page_id}/versions", headers=headers_b)).status_code == 404
    assert (
        await client.get(f"/api/v1/pages/{page_id}/versions/{version_id}", headers=headers_b)
    ).status_code == 404
    assert (
        await client.post(f"/api/v1/pages/{page_id}/versions/{version_id}/restore", headers=headers_b)
    ).status_code == 404


async def test_version_not_found_for_mismatched_page(client: AsyncClient) -> None:
    token = await register(client)
    headers = auth_headers(token)
    _, page_id_1 = await _make_page(client, token)
    _, page_id_2 = await _make_page(client, token)

    await _save(client, headers, page_id_1, 1, "página 1")
    versions = (await client.get(f"/api/v1/pages/{page_id_1}/versions", headers=headers)).json()
    version_id = versions[0]["id"]

    resp = await client.get(f"/api/v1/pages/{page_id_2}/versions/{version_id}", headers=headers)
    assert resp.status_code == 404
