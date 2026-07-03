"""
Progress Schemas - Pydantic models for progress tracking, achievements, and analytics
"""
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from datetime import datetime, date
from uuid import UUID


# ── Overview & Daily ────────────────────────────────────────────────────────

class ProgressOverviewResponse(BaseModel):
    user_id: UUID
    total_xp: int = 0
    current_level: int = 1
    current_streak: int = 0
    longest_streak: int = 0
    total_modules_completed: int = 0
    total_tasks_completed: int = 0
    total_time_spent_minutes: int = 0
    paths_completed: int = 0
    paths_active: int = 0


class DailyProgressResponse(BaseModel):
    date: date
    xp_earned: int = 0
    time_spent_minutes: int = 0
    modules_completed: int = 0
    tasks_completed: int = 0
    challenges_attempted: int = 0
    streak_maintained: bool = False
    current_streak: int = 0
    journal_entries_created: int = 0
    mentor_messages_sent: int = 0

    class Config:
        from_attributes = True


# ── Streak ──────────────────────────────────────────────────────────────────

class StreakResponse(BaseModel):
    current_streak: int = 0
    longest_streak: int = 0
    last_active_date: Optional[date] = None
    streak_history: List[date] = []


# ── Achievements ─────────────────────────────────────────────────────────────

class AchievementResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None
    category: str
    rarity: str
    xp_reward: int = 0
    is_hidden: bool = False

    class Config:
        from_attributes = True


class UserAchievementResponse(BaseModel):
    achievement: AchievementResponse
    earned_at: datetime
    progress_snapshot: Optional[dict] = None

    class Config:
        from_attributes = True


class AchievementListResponse(BaseModel):
    earned: List[UserAchievementResponse] = []
    available: List[AchievementResponse] = []
    total_earned: int = 0


# ── Skills ───────────────────────────────────────────────────────────────────

class SkillLevelResponse(BaseModel):
    id: UUID
    skill_name: str
    skill_category: Optional[str] = None
    current_level: int = 0
    confidence_score: float = 50.0
    assessments_count: int = 0
    last_assessed: Optional[datetime] = None

    class Config:
        from_attributes = True


class SkillRadarResponse(BaseModel):
    skills: List[SkillLevelResponse]
    categories: List[str]
    radar_data: List[dict]


# ── Analytics & Timeline ─────────────────────────────────────────────────────

class ActivityItem(BaseModel):
    date: date
    activity_type: str
    description: str
    xp_earned: int = 0
    metadata: Optional[dict] = None


class TimelineResponse(BaseModel):
    items: List[ActivityItem]
    total: int
    page: int
    size: int


class ProgressAnalyticsResponse(BaseModel):
    weekly_xp: List[dict]
    monthly_xp: List[dict]
    activity_heatmap: List[dict]
    learning_velocity: float = 0.0
    consistency_score: float = 0.0
    top_skills: List[SkillLevelResponse] = []
    improvement_areas: List[str] = []


# ── Leaderboard ──────────────────────────────────────────────────────────────

class LeaderboardEntry(BaseModel):
    rank: int
    user_id: UUID
    username: str
    display_name: Optional[str] = None
    total_xp: int = 0
    current_streak: int = 0
    avatar_url: Optional[str] = None
    is_current_user: bool = False


class LeaderboardResponse(BaseModel):
    entries: List[LeaderboardEntry]
    current_user_rank: Optional[int] = None
    total_users: int = 0
    period: str = "all_time"
