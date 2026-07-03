"""
Task Schemas - Pydantic models for tasks, submissions, and evaluations
"""
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID


# ── Task CRUD Schemas ────────────────────────────────────────────────────────

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    task_type: str = "practice"
    difficulty: str = "medium"
    deadline: Optional[datetime] = None
    max_attempts: int = 3
    xp_reward: int = 5
    hints: Optional[List[str]] = None
    template_code: Optional[dict] = None
    test_cases: Optional[dict] = None
    module_id: Optional[UUID] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    task_type: Optional[str] = None
    difficulty: Optional[str] = None
    deadline: Optional[datetime] = None
    max_attempts: Optional[int] = None
    xp_reward: Optional[int] = None
    status: Optional[str] = None


class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    module_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    task_type: str
    difficulty: str
    status: str
    deadline: Optional[datetime] = None
    max_attempts: int
    current_attempts: int = 0
    xp_reward: int
    hints: Optional[List[Any]] = None
    hints_used: int = 0
    template_code: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskDetailResponse(TaskResponse):
    test_cases: Optional[dict] = None
    submissions: List["SubmissionResponse"] = []

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    items: List[TaskResponse]
    total: int
    page: int
    size: int
    pages: int


class DailyTasksResponse(BaseModel):
    date: str
    tasks: List[TaskResponse]
    completed: int
    total: int
    xp_available: int


# ── Submission Schemas ────────────────────────────────────────────────────────

class SubmissionCreate(BaseModel):
    content: str
    language: Optional[str] = None
    time_spent_seconds: Optional[int] = None
    typing_pattern_data: Optional[dict] = None


class SubmissionResponse(BaseModel):
    id: UUID
    task_id: UUID
    user_id: UUID
    content: str
    language: Optional[str] = None
    score: Optional[float] = None
    max_score: float = 100.0
    feedback: Optional[dict] = None
    ai_feedback: Optional[str] = None
    time_spent_seconds: Optional[int] = None
    plagiarism_score: Optional[float] = None
    verification_status: str = "pending"
    attempt_number: int = 1
    test_results: Optional[dict] = None
    tests_passed: Optional[int] = None
    tests_total: Optional[int] = None
    submitted_at: datetime
    evaluated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Evaluation / Hints ────────────────────────────────────────────────────────

class TaskEvaluationResult(BaseModel):
    submission_id: UUID
    passed: bool
    score: float
    feedback: str
    ai_feedback: Optional[str] = None
    tests_passed: Optional[int] = None
    tests_total: Optional[int] = None
    xp_earned: int = 0
    suggestions: List[str] = []


class HintResponse(BaseModel):
    hint_number: int
    hint: str
    hints_remaining: int


# Update forward refs
TaskDetailResponse.model_rebuild()
