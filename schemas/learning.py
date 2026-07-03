"""
Learning Schemas - Pydantic models for learning paths, modules, and content
"""
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime, date
from uuid import UUID


# ── Enums (string literals mirroring model enums) ──────────────────────────

class PathStatusEnum(str):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


# ── LearningPath Schemas ────────────────────────────────────────────────────

class LearningPathCreate(BaseModel):
    title: str
    description: Optional[str] = None
    estimated_duration_hours: Optional[int] = None
    target_completion_date: Optional[date] = None


class LearningPathUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    estimated_duration_hours: Optional[int] = None
    target_completion_date: Optional[date] = None


class LearningPathGenerate(BaseModel):
    """Schema for AI-generated learning path"""
    topic: str
    target_level: str = "beginner"
    weekly_hours: int = 10
    include_projects: bool = True
    focus_areas: Optional[List[str]] = None


class LearningPathResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    status: str = "active"
    progress_percentage: float = 0
    total_xp: int = 0
    earned_xp: int = 0
    estimated_duration_hours: Optional[int] = None
    target_completion_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LearningPathDetailResponse(LearningPathResponse):
    modules: List["ModuleResponse"] = []

    class Config:
        from_attributes = True


# ── Module Schemas ──────────────────────────────────────────────────────────

class ModuleCreate(BaseModel):
    title: str
    description: Optional[str] = None
    content_type: str = "theory"
    difficulty: str = "medium"
    order_index: int = 0
    xp_reward: int = 10
    estimated_minutes: int = 30
    prerequisites: Optional[List[str]] = None


class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_type: Optional[str] = None
    difficulty: Optional[str] = None
    order_index: Optional[int] = None
    xp_reward: Optional[int] = None
    estimated_minutes: Optional[int] = None
    status: Optional[str] = None


class ModuleResponse(BaseModel):
    id: UUID
    path_id: UUID
    title: str
    description: Optional[str] = None
    content_type: str
    difficulty: str
    order_index: int
    status: str
    xp_reward: int
    estimated_minutes: int
    prerequisites: Optional[List[Any]] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ModuleDetailResponse(ModuleResponse):
    contents: List["ModuleContentResponse"] = []

    class Config:
        from_attributes = True


# ── ModuleContent Schemas ───────────────────────────────────────────────────

class ModuleContentCreate(BaseModel):
    content_type: str
    title: Optional[str] = None
    content_data: dict
    order_index: int = 0


class ModuleContentUpdate(BaseModel):
    content_type: Optional[str] = None
    title: Optional[str] = None
    content_data: Optional[dict] = None
    order_index: Optional[int] = None


class ModuleContentResponse(BaseModel):
    id: UUID
    module_id: UUID
    content_type: str
    title: Optional[str] = None
    content_data: dict
    order_index: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── Recommendation Schemas ──────────────────────────────────────────────────

class RecommendationResponse(BaseModel):
    module_id: UUID
    module_title: str
    reason: str
    priority: int
    estimated_time: Optional[int] = None


# Update forward refs
LearningPathDetailResponse.model_rebuild()
ModuleDetailResponse.model_rebuild()