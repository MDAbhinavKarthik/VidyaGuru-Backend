"""
Custom Exception Classes for VidyaGuru API

Comprehensive exception hierarchy for structured error handling
across all API endpoints and services.

Usage:
    from core.exceptions import (
        VidyaGuruException, ResourceNotFoundError, ValidationError,
        UnauthorizedError, ForbiddenError
    )
    
    # Raise in endpoint or service
    if not user:
        raise ResourceNotFoundError("user", user_id)
    
    if not data.is_valid():
        raise ValidationError("email", "Invalid email format")
"""

from fastapi import status
from typing import Optional, Any, Dict


class VidyaGuruException(Exception):
    """
    Base exception for all VidyaGuru custom exceptions.
    
    All custom exceptions inherit from this to allow catching
    any VidyaGuru-specific error.
    """
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to API response dictionary"""
        return {
            "error": self.error_code or self.__class__.__name__,
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details,
        }


# ============================================================================
# 4xx Client Error Exceptions
# ============================================================================

class ValidationError(VidyaGuruException):
    """
    Raised when request data validation fails.
    
    Usage:
        raise ValidationError(
            "email",
            message="Invalid email format",
            details={"provided": "invalid@email"}
        )
    """
    
    def __init__(
        self,
        field: str,
        message: str = "Validation failed",
        details: Optional[Dict[str, Any]] = None,
    ):
        full_message = f"Validation error in field '{field}': {message}"
        super().__init__(
            full_message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            details=details or {"field": field},
        )
        self.field = field


class ResourceNotFoundError(VidyaGuruException):
    """
    Raised when a requested resource doesn't exist.
    
    Usage:
        raise ResourceNotFoundError("user", 123)
        raise ResourceNotFoundError("challenge", challenge_id)
    """
    
    def __init__(self, resource_type: str, resource_id: Any = None):
        if resource_id:
            message = f"{resource_type.title()} with ID '{resource_id}' not found"
        else:
            message = f"{resource_type.title()} not found"
        
        super().__init__(
            message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESOURCE_NOT_FOUND",
            details={"resource_type": resource_type, "resource_id": str(resource_id)},
        )


class UnauthorizedError(VidyaGuruException):
    """
    Raised when user is not authenticated or credentials are invalid.
    
    Usage:
        raise UnauthorizedError("Invalid credentials")
        raise UnauthorizedError("Token expired")
    """
    
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
        )


class ForbiddenError(VidyaGuruException):
    """
    Raised when user is authenticated but doesn't have permission.
    
    Usage:
        raise ForbiddenError("You don't have permission to access this resource")
        raise ForbiddenError("Admin access required")
    """
    
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(
            message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
        )


class ConflictError(VidyaGuruException):
    """
    Raised when operation conflicts with existing data.
    
    Usage:
        raise ConflictError("user", "email already exists")
        raise ConflictError("task", "solution already submitted")
    """
    
    def __init__(self, resource_type: str, reason: str):
        message = f"{resource_type.title()} conflict: {reason}"
        super().__init__(
            message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT",
            details={"resource_type": resource_type, "reason": reason},
        )


class RateLimitError(VidyaGuruException):
    """
    Raised when user exceeds rate limit.
    
    Usage:
        raise RateLimitError("Too many challenge generation requests")
    """
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
        )


# ============================================================================
# 5xx Server Error Exceptions
# ============================================================================

class InternalServerError(VidyaGuruException):
    """
    Raised when an unexpected server error occurs.
    
    Usage:
        raise InternalServerError("Database connection failed")
    """
    
    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_SERVER_ERROR",
        )


class DatabaseError(VidyaGuruException):
    """
    Raised when database operations fail.
    
    Usage:
        raise DatabaseError("Failed to save user", details={"original_error": str(e)})
    """
    
    def __init__(
        self,
        message: str = "Database error",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="DATABASE_ERROR",
            details=details,
        )


class ExternalServiceError(VidyaGuruException):
    """
    Raised when external service (LLM, email, etc.) fails.
    
    Usage:
        raise ExternalServiceError(
            "gemini",
            "Failed to generate challenge",
            details={"retry_after": 60}
        )
    """
    
    def __init__(
        self,
        service_name: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        full_message = f"{service_name.title()} service error: {message}"
        super().__init__(
            full_message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="EXTERNAL_SERVICE_ERROR",
            details={"service": service_name, **(details or {})},
        )


# ============================================================================
# Domain-Specific Exceptions
# ============================================================================

class UserAuthenticationError(UnauthorizedError):
    """Raised when user authentication fails"""
    
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message)
        self.error_code = "USER_AUTHENTICATION_FAILED"


class InvalidTokenError(UnauthorizedError):
    """Raised when JWT token is invalid or expired"""
    
    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message)
        self.error_code = "INVALID_TOKEN"


class AccountDisabledError(ForbiddenError):
    """Raised when user account is disabled"""
    
    def __init__(self):
        super().__init__("Your account has been disabled")
        self.error_code = "ACCOUNT_DISABLED"


class CheatingSuspectedError(ForbiddenError):
    """
    Raised when anti-cheat system suspects cheating.
    
    Usage:
        raise CheatingSuspectedError(
            "High suspicion of plagiarism detected",
            details={"suspicion_score": 0.92}
        )
    """
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = "CHEATING_SUSPECTED"
        self.details = details or {}


class VerificationRequiredError(ForbiddenError):
    """
    Raised when user must complete verification before proceeding.
    
    Usage:
        raise VerificationRequiredError(
            verification_challenge_id=uuid,
            details={"challenge_type": "follow_up_question"}
        )
    """
    
    def __init__(
        self,
        verification_challenge_id: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        message = f"Verification required. Challenge ID: {verification_challenge_id}"
        super().__init__(message)
        self.error_code = "VERIFICATION_REQUIRED"
        self.details = {
            "verification_challenge_id": verification_challenge_id,
            **(details or {})
        }


class InvalidLearningPathError(ValidationError):
    """Raised when learning path configuration is invalid"""
    
    def __init__(self, reason: str):
        super().__init__(
            "learning_path",
            f"Invalid learning path: {reason}",
        )
        self.error_code = "INVALID_LEARNING_PATH"


class TaskSubmissionError(ValidationError):
    """Raised when task submission fails validation"""
    
    def __init__(self, reason: str, field: str = "submission"):
        super().__init__(field, reason)
        self.error_code = "TASK_SUBMISSION_FAILED"


class ChallengeGenerationError(ExternalServiceError):
    """Raised when AI challenge generation fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("gemini", message, details)
        self.error_code = "CHALLENGE_GENERATION_FAILED"


class SubmissionAnalysisError(ExternalServiceError):
    """Raised when anti-cheat submission analysis fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("anti_cheat", message, details)
        self.error_code = "SUBMISSION_ANALYSIS_FAILED"


class MentorResponseError(ExternalServiceError):
    """Raised when AI mentor response generation fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("gemini", message, details)
        self.error_code = "MENTOR_RESPONSE_FAILED"


# ============================================================================
# Operation-Specific Exceptions
# ============================================================================

class InvalidOperationError(ValidationError):
    """Raised when operation is invalid in current state"""
    
    def __init__(self, operation: str, reason: str):
        message = f"Cannot {operation}: {reason}"
        super().__init__("operation", message)
        self.error_code = "INVALID_OPERATION"


class QuotaExceededError(RateLimitError):
    """
    Raised when user exceeds usage quotas.
    
    Usage:
        raise QuotaExceededError(
            "challenge_generation_daily",
            message="You've reached your daily challenge generation limit",
            details={"limit": 10, "used": 10}
        )
    """
    
    def __init__(
        self,
        quota_type: str,
        message: str = "Quota exceeded",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.error_code = f"QUOTA_EXCEEDED_{quota_type.upper()}"
        self.details = details or {}


class DuplicateSubmissionError(ConflictError):
    """Raised when duplicate submission is attempted"""
    
    def __init__(self, resource_type: str = "submission"):
        super().__init__(resource_type, "Already submitted")
        self.error_code = "DUPLICATE_SUBMISSION"


class DataIntegrityError(DatabaseError):
    """Raised when data integrity constraint is violated"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.error_code = "DATA_INTEGRITY_ERROR"
