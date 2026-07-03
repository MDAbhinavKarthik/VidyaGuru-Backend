"""
Journal Schemas - Pydantic models for idea journal entries and tags
"""
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID


# ── Tag Schemas ─────────────────────────────────────────────────────────────

class TagCreate(BaseModel):
    name: str
    color: Optional[str] = "#6366f1"


class TagResponse(BaseModel):
    id: UUID
    name: str
    color: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Journal Entry Schemas ───────────────────────────────────────────────────

class JournalEntryCreate(BaseModel):
    title: Optional[str] = None
    content: str
    entry_type: Optional[str] = "note"
    mood: Optional[str] = None
    rich_content: Optional[dict] = None
    linked_entry_ids: Optional[List[str]] = None
    related_module_id: Optional[UUID] = None
    related_task_id: Optional[UUID] = None
    tag_ids: Optional[List[UUID]] = None


class JournalEntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    entry_type: Optional[str] = None
    mood: Optional[str] = None
    rich_content: Optional[dict] = None
    linked_entry_ids: Optional[List[str]] = None
    tag_ids: Optional[List[UUID]] = None


class JournalSearchRequest(BaseModel):
    query: str
    entry_type: Optional[str] = None
    mood: Optional[str] = None
    tag_ids: Optional[List[UUID]] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None


class JournalEntryResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: Optional[str] = None
    content: str
    entry_type: str
    mood: Optional[str] = None
    rich_content: Optional[dict] = None
    ai_insights: Optional[dict] = None
    linked_entry_ids: Optional[List[Any]] = None
    related_module_id: Optional[UUID] = None
    related_task_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True


class JournalEntryListResponse(BaseModel):
    items: List[JournalEntryResponse]
    total: int
    page: int
    size: int
    pages: int


class JournalInsightsResponse(BaseModel):
    total_entries: int
    entries_by_type: dict
    entries_by_mood: dict
    most_used_tags: List[dict]
    recent_themes: List[str]
    streak_days: int
    insights: List[str]


class JournalReflectionResponse(BaseModel):
    entry_id: UUID
    reflection: str
    key_insights: List[str]
    connections: List[str]
    suggested_follow_up: List[str]
    wisdom_quote: Optional[dict] = None
