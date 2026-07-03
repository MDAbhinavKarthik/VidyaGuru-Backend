"""
Application Constants

Centralized registry of all constants used throughout VidyaGuru.
Organized by domain for easy access and maintenance.

Usage:
    from utils.constants import (
        CHALLENGE_CATEGORIES,
        DIFFICULTY_LEVELS,
        VERIFICATION_TYPES,
        SUSPICION_LEVELS
    )
"""

# ============================================================================
# Challenge Constants
# ============================================================================

CHALLENGE_CATEGORIES = {
    "system_design": "System Design",
    "scalability": "Scalability",
    "algorithm_optimization": "Algorithm Optimization",
    "software_architecture": "Software Architecture",
}

CHALLENGE_DIFFICULTIES = {
    "easy": "Easy",
    "intermediate": "Intermediate",
    "hard": "Hard",
    "expert": "Expert",
}

SOLUTION_STATUSES = {
    "draft": "Draft",
    "submitted": "Submitted",
    "evaluating": "Evaluating",
    "evaluated": "Evaluated",
    "resume_worthy": "Resume Worthy",
}

# XP and Scoring
CHALLENGE_XP_REWARDS = {
    "easy": 100,
    "intermediate": 250,
    "hard": 500,
    "expert": 1000,
}

SOLUTION_EVALUATION_WEIGHTS = {
    "innovation": 0.30,      # 30%
    "practicality": 0.25,    # 25%
    "completeness": 0.25,    # 25%
    "code_quality": 0.20,    # 20%
}

RESUME_WORTHY_THRESHOLD = 0.85  # 85% score required


# ============================================================================
# Anti-Cheat Constants
# ============================================================================

SUSPICION_LEVELS = {
    "none": "No suspicion",
    "low": "Low suspicion",
    "medium": "Medium suspicion",
    "high": "High suspicion",
    "critical": "Critical suspicion",
}

VERIFICATION_TYPES = {
    "follow_up_question": "Follow-up Question",
    "code_explanation": "Code Explanation",
    "live_coding": "Live Coding",
    "design_discussion": "Design Discussion",
    "whiteboard_session": "Whiteboard Session",
}

VERIFICATION_STATUSES = {
    "pending": "Pending",
    "in_progress": "In Progress",
    "passed": "Passed",
    "failed": "Failed",
    "expired": "Expired",
}

# Anti-Cheat Thresholds
PLAGIARISM_DETECTION_THRESHOLD = 0.75  # 75% similarity = plagiarism
RAPID_SUBMISSION_THRESHOLD = 60  # seconds (too fast = suspicious)
LARGE_PASTE_THRESHOLD = 500  # characters (very large paste = suspicious)
TYPING_PATTERN_ANOMALY_THRESHOLD = 0.70  # 70% deviation = suspicious

# Integrity Levels
INTEGRITY_LEVELS = {
    "excellent": "Excellent",
    "good": "Good",
    "fair": "Fair",
    "suspicious": "Suspicious",
    "restricted": "Restricted",
}

INTEGRITY_TRUST_SCORE_BOUNDARIES = {
    "excellent": 90,    # 90+
    "good": 70,         # 70-89
    "fair": 50,         # 50-69
    "suspicious": 30,   # 30-49
    "restricted": 0,    # 0-29
}


# ============================================================================
# Learning Path Constants
# ============================================================================

LEARNING_PATH_STATUSES = {
    "not_started": "Not Started",
    "in_progress": "In Progress",
    "completed": "Completed",
    "abandoned": "Abandoned",
}

PROFICIENCY_LEVELS = {
    "beginner": "Beginner",
    "intermediate": "Intermediate",
    "advanced": "Advanced",
    "expert": "Expert",
}

MODULE_TYPES = {
    "video": "Video",
    "reading": "Reading",
    "interactive": "Interactive",
    "project": "Project",
    "quiz": "Quiz",
}


# ============================================================================
# Mentor Constants
# ============================================================================

MENTOR_RESPONSE_STYLES = {
    "socratic": "Ask guiding questions",
    "directive": "Provide direct guidance",
    "explanatory": "Explain concepts",
    "collaborative": "Work through together",
}

CONVERSATION_CONTEXTS = {
    "task": "Task Explanation",
    "challenge": "Challenge Discussion",
    "debugging": "Debugging Help",
    "learning": "Learning Guidance",
    "career": "Career Advice",
}

MENTOR_SESSION_TIMEOUT_SECONDS = 3600  # 1 hour


# ============================================================================
# User & Account Constants
# ============================================================================

USER_ROLES = {
    "student": "Student",
    "mentor": "Mentor",
    "admin": "Admin",
}

ACCOUNT_STATUSES = {
    "active": "Active",
    "inactive": "Inactive",
    "suspended": "Suspended",
    "banned": "Banned",
}

PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_NUMBERS = True
PASSWORD_REQUIRE_SPECIAL = True


# ============================================================================
# JWT & Token Constants
# ============================================================================

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
TOKEN_TYPE = "Bearer"


# ============================================================================
# Rate Limiting Constants
# ============================================================================

RATE_LIMITS = {
    "challenge_generation_daily": 10,
    "hint_requests_daily": 20,
    "api_calls_per_minute": 100,
    "submissions_per_hour": 50,
}

QUOTA_RESET_HOURS = {
    "daily": 24,
    "weekly": 168,
}


# ============================================================================
# Time Constants
# ============================================================================

TASK_SUBMISSION_TIMEOUT_MINUTES = 120  # 2 hours
VERIFICATION_CHALLENGE_EXPIRY_MINUTES = 30
JOURNAL_ENTRY_AUTO_SAVE_INTERVAL_SECONDS = 30


# ============================================================================
# Pagination Constants
# ============================================================================

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
MIN_PAGE_SIZE = 1


# ============================================================================
# Email Templates
# ============================================================================

EMAIL_TEMPLATES = {
    "welcome": "Welcome to VidyaGuru",
    "verification": "Verify your email",
    "password_reset": "Reset your password",
    "challenge_completed": "Challenge completed!",
    "learning_path_milestone": "Milestone reached!",
}


# ============================================================================
# Feature Flags
# ============================================================================

FEATURES = {
    "live_mentor": True,        # AI mentor conversations
    "challenges": True,         # Industry challenges
    "anti_cheat": True,         # Anti-cheat system
    "social_learning": False,   # Future: study groups
    "certifications": False,    # Future: certificates
    "gamification": False,      # Future: badges, leaderboards
}
