"""
Mentor Schemas - Pydantic models for AI mentor chat, conversations, and learning tools
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any, Dict
from datetime import datetime
from uuid import UUID


# ── Chat / Message Schemas ──────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None
    context_type: str = "general"
    related_module_id: Optional[UUID] = None
    related_task_id: Optional[UUID] = None
    code_context: Optional[str] = None
    include_wisdom: bool = False


class ChatMessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    tokens_used: Optional[int] = None
    metadata: Optional[dict] = None
    attachments: Optional[dict] = None
    user_rating: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    conversation_id: UUID
    message: ChatMessageResponse
    suggestions: List[str] = []
    related_resources: List[str] = []
    wisdom_quote: Optional[dict] = None
    follow_up_questions: List[str] = []


# ── Conversation Schemas ────────────────────────────────────────────────────

class ConversationResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=(), from_attributes=True)

    id: UUID
    user_id: UUID
    title: Optional[str] = None
    context_type: str
    related_module_id: Optional[UUID] = None
    related_task_id: Optional[UUID] = None
    total_tokens_used: int = 0
    summary: Optional[str] = None
    model_used: Optional[str] = None
    is_archived: bool = False
    created_at: datetime
    last_message_at: datetime


class ConversationDetailResponse(ConversationResponse):
    messages: List[ChatMessageResponse] = []

    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    items: List[ConversationResponse]
    total: int
    page: int
    size: int


# ── Concept Explanation Schemas ─────────────────────────────────────────────

class ConceptExplanationRequest(BaseModel):
    concept: str
    current_understanding: Optional[str] = None
    preferred_style: Optional[str] = "step-by-step"
    difficulty_level: str = "medium"


class ConceptExplanationResponse(BaseModel):
    concept: str
    explanation: str
    examples: List[str] = []
    analogies: List[str] = []
    related_concepts: List[str] = []
    quiz_questions: List[dict] = []
    wisdom_connection: Optional[str] = None


# ── Code Review Schemas ─────────────────────────────────────────────────────

class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"
    context: Optional[str] = None
    focus_areas: Optional[List[str]] = None


class CodeReviewResponse(BaseModel):
    overall_rating: float
    summary: str
    issues: List[dict] = []
    suggestions: List[dict] = []
    improved_code: Optional[str] = None
    learning_points: List[str] = []


# ── Quiz Schemas ────────────────────────────────────────────────────────────

class QuizGenerateRequest(BaseModel):
    topic: str
    num_questions: int = 5
    difficulty: str = "medium"
    question_types: List[str] = ["multiple_choice", "short_answer"]


class QuizQuestion(BaseModel):
    id: UUID
    question: str
    question_type: str
    options: Optional[List[str]] = None
    difficulty: str = "medium"
    topic: str
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None


class QuizResponse(BaseModel):
    quiz_id: UUID
    topic: str
    questions: List[QuizQuestion]
    time_limit_minutes: Optional[int] = None


# ── Mentor Suggestion Schema ────────────────────────────────────────────────

class MentorSuggestion(BaseModel):
    suggestion_type: str
    title: str
    description: str
    priority: int = 1
    action_url: Optional[str] = None
    metadata: Optional[dict] = None
