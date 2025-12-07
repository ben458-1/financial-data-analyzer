from pydantic import BaseModel
from typing import List, Optional


class Element(BaseModel):
    name: str
    type: str
    attribute: Optional[str] = None


class Selector(BaseModel):
    name: str
    type: str


class Doc(BaseModel):
    date: List[Selector]
    name: str
    next: Optional[dict]  # we'll define nested model below
    type: str
    popup: Optional[dict]
    maxDays: int
    newsUrl: List[Element]
    headline: List[Selector]
    isActive: int
    language: str
    maxLoops: int
    metadata: List[Selector]
    preamble: List[Selector]
    dateRegex: str
    searchUri: str
    timeRegex: str
    loopSection: List[Selector]
    newspaperId: int
    sectionRank: int
    dateRegexDesc: str
    timeRegexDesc: str
    articleSection: str
    searcSectorType: List[Selector]


class ConfigModel(BaseModel):
    id: int
    doc: Doc
    newspaper_id: int
    priority: int


# Redefine `next` and `popup` to use a nested model:
class ActionElement(BaseModel):
    method: str
    element: Element


# Update the main model with nested models for `next` and `popup`
class ConfigModelFinal(ConfigModel):
    next: Optional[ActionElement]
    popup: Optional[ActionElement]
