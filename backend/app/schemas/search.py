from pydantic import BaseModel


class SearchResult(BaseModel):
    notebook_id: int
    notebook_name: str
    page_id: int
    page_title: str
    snippet: str
