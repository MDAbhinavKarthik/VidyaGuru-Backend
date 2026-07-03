"""
VidyaGuru AI Mentor Package
A comprehensive AI-powered learning mentor system

"विद्या ददाति विनयम्" - Knowledge gives humility
"""

from mentor.prompts import (
    LearningPhase,
    MentorPersonality,
    LearnerContext,
    build_system_prompt,
    build_phase_prompt,
    get_wisdom_quote,
    get_motivation_message,
    WISDOM_QUOTES,
    PHASE_PROMPTS,
    ANTI_CHEATING_PROMPTS,
)

from mentor.engine import (
    MentorEngine,
    LLMProvider,
    MessageRole,
    Message,
    LearningSession,
    MentorResponse,
    CheatingIndicator,
)

from mentor.session_manager import (
    SessionManager,
    PhaseStateMachine,
)

from mentor.cheating_detection import (
    CheatingDetector,
    CheatingAnalysis,
    SuspicionLevel,
    VerificationStrategy,
    cheating_detector,
)

__all__ = [
    # Prompts
    "LearningPhase",
    "MentorPersonality", 
    "LearnerContext",
    "build_system_prompt",
    "build_phase_prompt",
    "get_wisdom_quote",
    "get_motivation_message",
    "WISDOM_QUOTES",
    "PHASE_PROMPTS",
    "ANTI_CHEATING_PROMPTS",
    
    # Engine
    "MentorEngine",
    "LLMProvider",
    "MessageRole",
    "Message",
    "LearningSession",
    "MentorResponse",
    "CheatingIndicator",
    
    # Session Management
    "SessionManager",
    "PhaseStateMachine",
    
    # Cheating Detection
    "CheatingDetector",
    "CheatingAnalysis",
    "SuspicionLevel",
    "VerificationStrategy",
    "cheating_detector",
]

__version__ = "1.0.0"
