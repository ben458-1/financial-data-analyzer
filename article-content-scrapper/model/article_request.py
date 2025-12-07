from typing import Optional

from pydantic import BaseModel, Field


class ArticleRequest(BaseModel):
    newspaper_id: int
    date: Optional[str]
    url: str
    article_id: int
    headline: Optional[str] = None
    preamble: Optional[str] = None
    sector: Optional[str] = None
    publish: Optional[bool] = False
    conf_id: Optional[int] = None
    s_section: Optional[int] = None

    class Config:
        allow_population_by_field_name = True
