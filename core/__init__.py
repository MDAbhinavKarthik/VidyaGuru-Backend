"""
Core Package

Exports:
- Security: password hashing, JWT token generation/verification
- Exceptions: VidyaGuru-specific exception hierarchy
- Error Codes: Centralized error code registry and mappings
- Middleware: Security middleware for request/response handling
"""

from core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    create_tokens,
    decode_token,
    verify_token,
    SecurityError
)

from core.exceptions import (
    VidyaGuruException,
    # 4xx Errors
    ValidationError,
    ResourceNotFoundError,
    UnauthorizedError,
    ForbiddenError,
    ConflictError,
    RateLimitError,
    # 5xx Errors
    InternalServerError,
    DatabaseError,
    ExternalServiceError,
    # Domain-Specific
    UserAuthenticationError,
    InvalidTokenError,
    AccountDisabledError,
    CheatingSuspectedError,
    VerificationRequiredError,
    InvalidLearningPathError,
    TaskSubmissionError,
    ChallengeGenerationError,
    SubmissionAnalysisError,
    MentorResponseError,
    InvalidOperationError,
    QuotaExceededError,
    DuplicateSubmissionError,
    DataIntegrityError,
)

from core.error_codes import ErrorCode, ErrorCodeRegistry

__all__ = [
    # Security
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "create_refresh_token",
    "create_tokens",
    "decode_token",
    "verify_token",
    "SecurityError",
    # Exceptions - Base
    "VidyaGuruException",
    # Exceptions - 4xx
    "ValidationError",
    "ResourceNotFoundError",
    "UnauthorizedError",
    "ForbiddenError",
    "ConflictError",
    "RateLimitError",
    # Exceptions - 5xx
    "InternalServerError",
    "DatabaseError",
    "ExternalServiceError",
    # Exceptions - Domain-Specific
    "UserAuthenticationError",
    "InvalidTokenError",
    "AccountDisabledError",
    "CheatingSuspectedError",
    "VerificationRequiredError",
    "InvalidLearningPathError",
    "TaskSubmissionError",
    "ChallengeGenerationError",
    "SubmissionAnalysisError",
    "MentorResponseError",
    "InvalidOperationError",
    "QuotaExceededError",
    "DuplicateSubmissionError",
    "DataIntegrityError",
    # Error Codes
    "ErrorCode",
    "ErrorCodeRegistry",
]
