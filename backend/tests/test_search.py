from httpx import AsyncClient

from tests.conftest import auth_headers, register


async def _make_page_with_text(
    client: AsyncClient, headers: dict[str, str], notebook_name: str, page_title: str, text: str
) -> dict:
    notebook = (
        await client.post("/api/v1/notebooks", json={"name": notebook_name}, headers=headers)
    ).json()
    page = (
        await client.post(
            f"/api/v1/notebooks/{notebook['id']}/pages", json={"title": page_title}, headers=headers
        )
    ).json()
    content = {
        "type": "doc",
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": text}]}],
    }
    await client.put(
        f"/api/v1/pages/{page['id']}/content",
        json={"content_json": content, "revision": 1},
        headers=headers,
    )
    return {"notebook": notebook, "page": page}


async def test_search_matches_content_and_returns_snippet(client: AsyncClient) -> None:
    token = await register(client)
    headers = auth_headers(token)
    await _make_page_with_text(
        client, headers, "Receitas", "Bolo", "uma receita de bolo de cenoura com cobertura de chocolate"
    )
    await _make_page_with_text(client, headers, "Trabalho", "Reunião", "pauta da reunião de segunda")

    resp = await client.get("/api/v1/search", params={"q": "cenoura"}, headers=headers)
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert results[0]["page_title"] == "Bolo"
    assert "cenoura" in results[0]["snippet"]


async def test_search_matches_page_title_and_notebook_name(client: AsyncClient) -> None:
    token = await register(client)
    headers = auth_headers(token)
    await _make_page_with_text(client, headers, "Caderno Especial", "Notas soltas", "conteúdo qualquer")

    resp = await client.get("/api/v1/search", params={"q": "especial"}, headers=headers)
    assert len(resp.json()) == 1

    resp = await client.get("/api/v1/search", params={"q": "soltas"}, headers=headers)
    assert len(resp.json()) == 1

    resp = await client.get("/api/v1/search", params={"q": "inexistente"}, headers=headers)
    assert resp.json() == []


async def test_search_filtered_by_tag(client: AsyncClient) -> None:
    token = await register(client)
    headers = auth_headers(token)
    made = await _make_page_with_text(client, headers, "Caderno A", "Página A", "texto compartilhado")
    await _make_page_with_text(client, headers, "Caderno B", "Página B", "texto compartilhado também")

    await client.patch(
        f"/api/v1/notebooks/{made['notebook']['id']}", json={"tags": ["trabalho"]}, headers=headers
    )

    resp = await client.get(
        "/api/v1/search", params={"q": "compartilhado", "tag": "trabalho"}, headers=headers
    )
    results = resp.json()
    assert len(results) == 1
    assert results[0]["notebook_id"] == made["notebook"]["id"]


async def test_search_isolated_between_users(client: AsyncClient) -> None:
    token_a = await register(client, email="a@example.com")
    await _make_page_with_text(
        client, auth_headers(token_a), "Caderno A", "Página A", "informação confidencial do usuário A"
    )

    token_b = await register(client, email="b@example.com")
    resp = await client.get(
        "/api/v1/search", params={"q": "confidencial"}, headers=auth_headers(token_b)
    )
    assert resp.json() == []
