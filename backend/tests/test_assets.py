from httpx import AsyncClient

from app.core.config import settings
from tests.conftest import auth_headers, register

PNG_BYTES = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
PDF_BYTES = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"


async def test_upload_image(client: AsyncClient) -> None:
    token = await register(client)
    resp = await client.post(
        "/api/v1/assets",
        data={"kind": "image"},
        files={"file": ("foto.png", PNG_BYTES, "image/png")},
        headers=auth_headers(token),
    )
    assert resp.status_code == 201, resp.text
    asset = resp.json()
    assert asset["kind"] == "image"
    assert asset["mime"] == "image/png"
    assert asset["filename"] == "foto.png"
    assert asset["size"] == len(PNG_BYTES)
    assert asset["url"].startswith("/media/")


async def test_upload_pdf(client: AsyncClient) -> None:
    token = await register(client)
    resp = await client.post(
        "/api/v1/assets",
        data={"kind": "pdf"},
        files={"file": ("doc.pdf", PDF_BYTES, "application/pdf")},
        headers=auth_headers(token),
    )
    assert resp.status_code == 201, resp.text
    asset = resp.json()
    assert asset["kind"] == "pdf"
    assert asset["mime"] == "application/pdf"
    assert asset["size"] == len(PDF_BYTES)


async def test_image_rejects_wrong_mime(client: AsyncClient) -> None:
    token = await register(client)
    resp = await client.post(
        "/api/v1/assets",
        data={"kind": "image"},
        files={"file": ("foto.png", PDF_BYTES, "application/pdf")},
        headers=auth_headers(token),
    )
    assert resp.status_code == 400


async def test_pdf_rejects_wrong_mime(client: AsyncClient) -> None:
    token = await register(client)
    resp = await client.post(
        "/api/v1/assets",
        data={"kind": "pdf"},
        files={"file": ("doc.pdf", PNG_BYTES, "image/png")},
        headers=auth_headers(token),
    )
    assert resp.status_code == 400


async def test_image_rejects_too_large(client: AsyncClient, monkeypatch) -> None:
    monkeypatch.setattr(settings, "max_image_bytes", 8)
    token = await register(client)
    resp = await client.post(
        "/api/v1/assets",
        data={"kind": "image"},
        files={"file": ("grande.png", PNG_BYTES, "image/png")},
        headers=auth_headers(token),
    )
    assert resp.status_code == 400


async def test_pdf_rejects_too_large(client: AsyncClient, monkeypatch) -> None:
    monkeypatch.setattr(settings, "max_pdf_bytes", 8)
    token = await register(client)
    resp = await client.post(
        "/api/v1/assets",
        data={"kind": "pdf"},
        files={"file": ("grande.pdf", PDF_BYTES, "application/pdf")},
        headers=auth_headers(token),
    )
    assert resp.status_code == 400


async def test_upload_requires_auth(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/v1/assets",
        data={"kind": "image"},
        files={"file": ("foto.png", PNG_BYTES, "image/png")},
    )
    assert resp.status_code == 401
