# app/schemas/newspaper.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Newspaper(BaseModel):
    id: int
    active_hours: Optional[str] = None
    add_date: datetime
    alexa_global_ranking: Optional[int] = None
    alexa_local_ranking: Optional[int] = None
    alexa_local_region: Optional[str] = None
    currency: Optional[str] = None
    isactive: Optional[int] = None
    link: Optional[str] = None
    logo: Optional[str] = None
    name: str
    price_month: Optional[float] = None
    price_year: Optional[float] = None
    time_zone: Optional[str] = None
    language_id: Optional[int] = None
    region_id: Optional[int] = None
