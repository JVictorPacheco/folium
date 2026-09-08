from typing import Any

from app.repositories.page import PageRepository

SNIPPET_RADIUS = 40


def _extract_text(node: Any, parts: list[str]) -> None:
    if isinstance(node, dict):
        text = node.get("text")
        if isinstance(text, str):
            parts.append(text)
        for child in node.get("content") or []:
            _extract_text(child, parts)
    elif isinstance(node, list):
        for child in node:
            _extract_text(child, parts)


def page_plain_text(content_json: dict) -> str:
    parts: list[str] = []
    _extract_text(content_json, parts)
    return " ".join(parts)


def _snippet(text: str, query: str) -> str:
    lower = text.lower()
    idx = lower.find(query.lower())
    if idx == -1:
        return text[: SNIPPET_RADIUS * 2].strip()
    start = max(0, idx - SNIPPET_RADIUS)
    end = min(len(text), idx + len(query) + SNIPPET_RADIUS)
    prefix = "…" if start > 0 else ""
    suffix = "…" if end < len(text) else ""
    return f"{prefix}{text[start:end].strip()}{suffix}"


class SearchService:
    def __init__(self, page_repo: PageRepository) -> None:
        self._page_repo = page_repo

    async def search(self, user_id: int, query: str, tag: str | None = None) -> list[dict]:
        query = query.strip()
        if not query:
            return []

        pages = await self._page_repo.list_for_user(user_id, tag)
        needle = query.lower()
        results: list[dict] = []
        for page in pages:
            title_match = needle in page.title.lower()
            notebook_match = needle in page.notebook.name.lower()
            text = page_plain_text(page.content_json)
            content_match = needle in text.lower()
            if not (title_match or notebook_match or content_match):
                continue
            snippet = _snippet(text, query) if content_match else page.title
            results.append(
                {
                    "notebook_id": page.notebook_id,
                    "notebook_name": page.notebook.name,
                    "page_id": page.id,
                    "page_title": page.title,
                    "snippet": snippet,
                }
            )
        return results
