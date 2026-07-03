"""
Reminder Schemas - Pydantic models for study reminders and smart suggestions
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# ── Reminder CRUD Schemas ────────────────────────────────────────────────────

class ReminderCreate(BaseModel):
    title: str
    description: Optional[str] = None
    reminder_type: str = "custom"
    scheduled_at: datetime
    repeat_pattern: str = "none"
    repeat_config: Optional[dict] = None
    channels: Optional[List[str]] = None
    related_task_id: Optional[UUID] = None
    related_module_id: Optional[UUID] = None


class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    reminder_type: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    repeat_pattern: Optional[str] = None
    repeat_config: Optional[dict] = None
    channels: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ReminderResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    reminder_type: str
    scheduled_at: datetime
    repeat_pattern: str
    repeat_config: Optional[dict] = None
    channels: Optional[List] = None
    is_active: bool = True
    is_completed: bool = False
    last_sent: Optional[datetime] = None
    send_count: int = 0
    related_task_id: Optional[UUID] = None
    related_module_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReminderListResponse(BaseModel):
    items: List[ReminderResponse]
    total: int
    page: int
    size: int


# ── Smart Reminders ──────────────────────────────────────────────────────────

class SmartReminderSuggestion(BaseModel):
    title: str
    description: str
    suggested_time: datetime
    reminder_type: str
    reason: str
    priority: int = 1


class UpcomingRemindersResponse(BaseModel):
    reminders: List[ReminderResponse]
    total_upcoming: int
    next_reminder: Optional[ReminderResponse] = None
