"""
Database Models Package

All domain models organized by feature:
- User Management: User, UserProfile
- Learning System: LearningPath, Module, ModuleContent
- Task Management: Task, Submission
- Journal: JournalEntry, Tag, EntryTag
- Progress & Gamification: DailyProgress, SkillLevel, Achievement, UserAchievement
- Reminders: Reminder
- Mentor: Conversation, Message
- Challenges: IndustryChallenge, ChallengeSolution, ResumeHighlight
- Anti-Cheat: SubmissionAnalysis, VerificationChallenge, UserIntegrityProfile, SuspiciousActivityLog, SubmissionFingerprint
"""
from models.user import User, UserProfile
from models.learning import LearningPath, Module, ModuleContent
from models.task import Task, Submission
from models.journal import JournalEntry, Tag, EntryTag
from models.progress import DailyProgress, SkillLevel, Achievement, UserAchievement
from models.reminder import Reminder
from models.conversation import Conversation, Message
from models.challenge import IndustryChallenge, ChallengeSolution, ResumeHighlight
from models.anti_cheat import (
    SubmissionAnalysis,
    VerificationChallenge,
    UserIntegrityProfile,
    SuspiciousActivityLog,
    SubmissionFingerprint,
    SuspicionLevel,
    SuspicionType,
    VerificationType,
    VerificationStatus,
)

__all__ = [
    # User
    "User",
    "UserProfile",
    # Learning
    "LearningPath",
    "Module",
    "ModuleContent",
    # Tasks
    "Task",
    "Submission",
    # Journal
    "JournalEntry",
    "Tag",
    "EntryTag",
    # Progress
    "DailyProgress",
    "SkillLevel",
    "Achievement",
    "UserAchievement",
    # Reminders
    "Reminder",
    # Mentor
    "Conversation",
    "Message",
    # Challenges
    "IndustryChallenge",
    "ChallengeSolution",
    "ResumeHighlight",
    # Anti-Cheat
    "SubmissionAnalysis",
    "VerificationChallenge",
    "UserIntegrityProfile",
    "SuspiciousActivityLog",
    "SubmissionFingerprint",
    "SuspicionLevel",
    "SuspicionType",
    "VerificationType",
    "VerificationStatus",
]
