"""
Error Codes and Status Codes for VidyaGuru API

Central registry of all error codes used throughout the system.
Provides mappings for HTTP status codes and human-readable messages.

Usage:
    from core.error_codes import ErrorCode, ErrorCodeRegistry
    
    # Use in exceptions
    raise ValidationError("email", ErrorCode.INVALID_EMAIL)
    
    # Get message
    message = ErrorCodeRegistry.get_message(ErrorCode.USER_NOT_FOUND)
    
    # Get status code
    status = ErrorCodeRegistry.get_status(ErrorCode.UNAUTHORIZED)
"""

from enum import Enum
from fastapi import status as http_status
from typing import Dict, Tuple


class ErrorCode(str, Enum):
    """
    Central registry of all error codes.
    Format: DOMAIN_SPECIFIC_ERROR
    """
    
    # ========================================================================
    # Authentication & Authorization (AUTH_*)
    # ========================================================================
    
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INVALID_TOKEN = "INVALID_TOKEN"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    FORBIDDEN = "FORBIDDEN"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    ACCOUNT_DISABLED = "ACCOUNT_DISABLED"
    ACCOUNT_NOT_VERIFIED = "ACCOUNT_NOT_VERIFIED"
    MFA_REQUIRED = "MFA_REQUIRED"
    
    # ========================================================================
    # User Management (USER_*)
    # ========================================================================
    
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    EMAIL_ALREADY_REGISTERED = "EMAIL_ALREADY_REGISTERED"
    INVALID_EMAIL_FORMAT = "INVALID_EMAIL_FORMAT"
    INVALID_PASSWORD_FORMAT = "INVALID_PASSWORD_FORMAT"
    PASSWORD_TOO_WEAK = "PASSWORD_TOO_WEAK"
    PROFILE_UPDATE_FAILED = "PROFILE_UPDATE_FAILED"
    USER_CREATION_FAILED = "USER_CREATION_FAILED"
    
    # ========================================================================
    # Learning Paths & Content (LEARNING_*)
    # ========================================================================
    
    LEARNING_PATH_NOT_FOUND = "LEARNING_PATH_NOT_FOUND"
    INVALID_LEARNING_PATH = "INVALID_LEARNING_PATH"
    MODULE_NOT_FOUND = "MODULE_NOT_FOUND"
    CONTENT_NOT_FOUND = "CONTENT_NOT_FOUND"
    PREREQUISITE_NOT_COMPLETED = "PREREQUISITE_NOT_COMPLETED"
    LEARNING_PATH_ALREADY_STARTED = "LEARNING_PATH_ALREADY_STARTED"
    
    # ========================================================================
    # Tasks & Submissions (TASK_*)
    # ========================================================================
    
    TASK_NOT_FOUND = "TASK_NOT_FOUND"
    TASK_SUBMISSION_FAILED = "TASK_SUBMISSION_FAILED"
    TASK_ALREADY_SUBMITTED = "TASK_ALREADY_SUBMITTED"
    DUPLICATE_SUBMISSION = "DUPLICATE_SUBMISSION"
    TASK_NOT_STARTED = "TASK_NOT_STARTED"
    TASK_DEADLINE_PASSED = "TASK_DEADLINE_PASSED"
    INVALID_TASK_STATUS = "INVALID_TASK_STATUS"
    SUBMISSION_FORMAT_INVALID = "SUBMISSION_FORMAT_INVALID"
    
    # ========================================================================
    # Anti-Cheat & Integrity (INTEGRITY_*)
    # ========================================================================
    
    CHEATING_SUSPECTED = "CHEATING_SUSPECTED"
    VERIFICATION_REQUIRED = "VERIFICATION_REQUIRED"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"
    VERIFICATION_EXPIRED = "VERIFICATION_EXPIRED"
    ACCOUNT_RESTRICTED = "ACCOUNT_RESTRICTED"
    SUSPICIOUS_ACTIVITY_DETECTED = "SUSPICIOUS_ACTIVITY_DETECTED"
    SUBMISSION_ANALYSIS_FAILED = "SUBMISSION_ANALYSIS_FAILED"
    
    # ========================================================================
    # Challenges (CHALLENGE_*)
    # ========================================================================
    
    CHALLENGE_NOT_FOUND = "CHALLENGE_NOT_FOUND"
    CHALLENGE_GENERATION_FAILED = "CHALLENGE_GENERATION_FAILED"
    INVALID_CHALLENGE_PARAMETERS = "INVALID_CHALLENGE_PARAMETERS"
    CHALLENGE_EVALUATION_FAILED = "CHALLENGE_EVALUATION_FAILED"
    SOLUTION_NOT_FOUND = "SOLUTION_NOT_FOUND"
    SOLUTION_EVALUATION_FAILED = "SOLUTION_EVALUATION_FAILED"
    RESUME_HIGHLIGHT_NOT_FOUND = "RESUME_HIGHLIGHT_NOT_FOUND"
    
    # ========================================================================
    # Mentor & AI (MENTOR_*)
    # ========================================================================
    
    MENTOR_RESPONSE_FAILED = "MENTOR_RESPONSE_FAILED"
    CONVERSATION_NOT_FOUND = "CONVERSATION_NOT_FOUND"
    INVALID_MENTOR_REQUEST = "INVALID_MENTOR_REQUEST"
    MENTOR_SESSION_EXPIRED = "MENTOR_SESSION_EXPIRED"
    HINT_GENERATION_FAILED = "HINT_GENERATION_FAILED"
    
    # ========================================================================
    # Journal & Progress (JOURNAL_*, PROGRESS_*)
    # ========================================================================
    
    JOURNAL_ENTRY_NOT_FOUND = "JOURNAL_ENTRY_NOT_FOUND"
    JOURNAL_CREATION_FAILED = "JOURNAL_CREATION_FAILED"
    PROGRESS_UPDATE_FAILED = "PROGRESS_UPDATE_FAILED"
    PROGRESS_TRACKING_FAILED = "PROGRESS_TRACKING_FAILED"
    
    # ========================================================================
    # Reminders (REMINDER_*)
    # ========================================================================
    
    REMINDER_NOT_FOUND = "REMINDER_NOT_FOUND"
    REMINDER_CREATION_FAILED = "REMINDER_CREATION_FAILED"
    INVALID_REMINDER_TIME = "INVALID_REMINDER_TIME"
    REMINDER_DELIVERY_FAILED = "REMINDER_DELIVERY_FAILED"
    
    # ========================================================================
    # Validation Errors (VALIDATION_*)
    # ========================================================================
    
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_REQUEST_BODY = "INVALID_REQUEST_BODY"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    INVALID_FIELD_VALUE = "INVALID_FIELD_VALUE"
    FIELD_TYPE_MISMATCH = "FIELD_TYPE_MISMATCH"
    
    # ========================================================================
    # Resource Conflicts (CONFLICT_*)
    # ========================================================================
    
    CONFLICT = "CONFLICT"
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"
    STATE_CONFLICT = "STATE_CONFLICT"
    OPERATION_NOT_ALLOWED = "OPERATION_NOT_ALLOWED"
    
    # ========================================================================
    # Rate Limiting & Quotas (RATE_*, QUOTA_*)
    # ========================================================================
    
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    QUOTA_EXCEEDED_CHALLENGES = "QUOTA_EXCEEDED_CHALLENGES"
    QUOTA_EXCEEDED_HINTS = "QUOTA_EXCEEDED_HINTS"
    QUOTA_EXCEEDED_SUBMISSIONS = "QUOTA_EXCEEDED_SUBMISSIONS"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"
    
    # ========================================================================
    # Database & Data (DATABASE_*, DATA_*)
    # ========================================================================
    
    DATABASE_ERROR = "DATABASE_ERROR"
    DATABASE_CONNECTION_FAILED = "DATABASE_CONNECTION_FAILED"
    DATA_INTEGRITY_ERROR = "DATA_INTEGRITY_ERROR"
    TRANSACTION_FAILED = "TRANSACTION_FAILED"
    QUERY_FAILED = "QUERY_FAILED"
    
    # ========================================================================
    # External Services (SERVICE_*)
    # ========================================================================
    
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    GEMINI_SERVICE_ERROR = "GEMINI_SERVICE_ERROR"
    EMAIL_SERVICE_ERROR = "EMAIL_SERVICE_ERROR"
    STORAGE_SERVICE_ERROR = "STORAGE_SERVICE_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    SERVICE_TIMEOUT = "SERVICE_TIMEOUT"
    
    # ========================================================================
    # Internal Errors (INTERNAL_*)
    # ========================================================================
    
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    UNHANDLED_EXCEPTION = "UNHANDLED_EXCEPTION"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    RUNTIME_ERROR = "RUNTIME_ERROR"


class ErrorCodeRegistry:
    """
    Registry mapping error codes to HTTP status codes and descriptions.
    Provides centralized error metadata for the entire API.
    """
    
    # Mapping: ErrorCode -> (HTTP Status Code, Human-Readable Message)
    _ERROR_MAPPINGS: Dict[str, Tuple[int, str]] = {
        # Authentication & Authorization
        ErrorCode.UNAUTHORIZED: (
            http_status.HTTP_401_UNAUTHORIZED,
            "Authentication required. Please log in.",
        ),
        ErrorCode.INVALID_CREDENTIALS: (
            http_status.HTTP_401_UNAUTHORIZED,
            "Invalid email or password.",
        ),
        ErrorCode.INVALID_TOKEN: (
            http_status.HTTP_401_UNAUTHORIZED,
            "The provided token is invalid or malformed.",
        ),
        ErrorCode.TOKEN_EXPIRED: (
            http_status.HTTP_401_UNAUTHORIZED,
            "Your session has expired. Please log in again.",
        ),
        ErrorCode.FORBIDDEN: (
            http_status.HTTP_403_FORBIDDEN,
            "Access to this resource is forbidden.",
        ),
        ErrorCode.INSUFFICIENT_PERMISSIONS: (
            http_status.HTTP_403_FORBIDDEN,
            "You do not have permission to perform this action.",
        ),
        ErrorCode.ACCOUNT_DISABLED: (
            http_status.HTTP_403_FORBIDDEN,
            "Your account has been disabled.",
        ),
        ErrorCode.ACCOUNT_NOT_VERIFIED: (
            http_status.HTTP_403_FORBIDDEN,
            "Please verify your email address before proceeding.",
        ),
        
        # User Management
        ErrorCode.USER_NOT_FOUND: (
            http_status.HTTP_404_NOT_FOUND,
            "User not found.",
        ),
        ErrorCode.USER_ALREADY_EXISTS: (
            http_status.HTTP_409_CONFLICT,
            "A user with this email already exists.",
        ),
        ErrorCode.EMAIL_ALREADY_REGISTERED: (
            http_status.HTTP_409_CONFLICT,
            "This email address is already registered.",
        ),
        ErrorCode.INVALID_EMAIL_FORMAT: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Invalid email format.",
        ),
        ErrorCode.INVALID_PASSWORD_FORMAT: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Password must be at least 8 characters long.",
        ),
        ErrorCode.PASSWORD_TOO_WEAK: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Password is too weak. Use a mix of uppercase, lowercase, numbers, and symbols.",
        ),
        
        # Learning Paths
        ErrorCode.LEARNING_PATH_NOT_FOUND: (
            http_status.HTTP_404_NOT_FOUND,
            "Learning path not found.",
        ),
        ErrorCode.INVALID_LEARNING_PATH: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "The learning path configuration is invalid.",
        ),
        ErrorCode.PREREQUISITE_NOT_COMPLETED: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "You must complete prerequisite modules first.",
        ),
        
        # Tasks
        ErrorCode.TASK_NOT_FOUND: (
            http_status.HTTP_404_NOT_FOUND,
            "Task not found.",
        ),
        ErrorCode.TASK_SUBMISSION_FAILED: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Failed to submit task. Please check your submission.",
        ),
        ErrorCode.TASK_ALREADY_SUBMITTED: (
            http_status.HTTP_409_CONFLICT,
            "You have already submitted this task.",
        ),
        ErrorCode.DUPLICATE_SUBMISSION: (
            http_status.HTTP_409_CONFLICT,
            "A submission with this content already exists.",
        ),
        ErrorCode.TASK_DEADLINE_PASSED: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "The deadline for this task has passed.",
        ),
        
        # Anti-Cheat & Integrity
        ErrorCode.CHEATING_SUSPECTED: (
            http_status.HTTP_403_FORBIDDEN,
            "Suspicious activity detected. Please verify your submission.",
        ),
        ErrorCode.VERIFICATION_REQUIRED: (
            http_status.HTTP_403_FORBIDDEN,
            "Verification required. Complete the challenge to proceed.",
        ),
        ErrorCode.VERIFICATION_FAILED: (
            http_status.HTTP_403_FORBIDDEN,
            "Verification failed. Please try again.",
        ),
        ErrorCode.VERIFICATION_EXPIRED: (
            http_status.HTTP_410_GONE,
            "Your verification challenge has expired.",
        ),
        ErrorCode.ACCOUNT_RESTRICTED: (
            http_status.HTTP_403_FORBIDDEN,
            "Your account has been restricted due to suspicious activity.",
        ),
        
        # Challenges
        ErrorCode.CHALLENGE_NOT_FOUND: (
            http_status.HTTP_404_NOT_FOUND,
            "Challenge not found.",
        ),
        ErrorCode.CHALLENGE_GENERATION_FAILED: (
            http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Failed to generate challenge. Please try again.",
        ),
        ErrorCode.INVALID_CHALLENGE_PARAMETERS: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Invalid challenge parameters.",
        ),
        ErrorCode.CHALLENGE_EVALUATION_FAILED: (
            http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Failed to evaluate challenge. Please try again.",
        ),
        
        # Mentor
        ErrorCode.MENTOR_RESPONSE_FAILED: (
            http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Failed to get mentor response. Please try again.",
        ),
        ErrorCode.INVALID_MENTOR_REQUEST: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Invalid mentor request.",
        ),
        ErrorCode.MENTOR_SESSION_EXPIRED: (
            http_status.HTTP_410_GONE,
            "Your mentor session has expired.",
        ),
        
        # Validation
        ErrorCode.VALIDATION_ERROR: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Validation error.",
        ),
        ErrorCode.INVALID_REQUEST_BODY: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Invalid request body.",
        ),
        ErrorCode.MISSING_REQUIRED_FIELD: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Required field is missing.",
        ),
        ErrorCode.INVALID_FIELD_VALUE: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Invalid field value.",
        ),
        
        # Conflicts
        ErrorCode.CONFLICT: (
            http_status.HTTP_409_CONFLICT,
            "The operation conflicts with existing data.",
        ),
        ErrorCode.RESOURCE_ALREADY_EXISTS: (
            http_status.HTTP_409_CONFLICT,
            "This resource already exists.",
        ),
        ErrorCode.OPERATION_NOT_ALLOWED: (
            http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "This operation is not allowed in the current state.",
        ),
        
        # Rate Limiting
        ErrorCode.RATE_LIMIT_EXCEEDED: (
            http_status.HTTP_429_TOO_MANY_REQUESTS,
            "Rate limit exceeded. Please try again later.",
        ),
        ErrorCode.QUOTA_EXCEEDED_CHALLENGES: (
            http_status.HTTP_429_TOO_MANY_REQUESTS,
            "You've reached your daily challenge generation limit.",
        ),
        ErrorCode.QUOTA_EXCEEDED_HINTS: (
            http_status.HTTP_429_TOO_MANY_REQUESTS,
            "You've reached your hint limit. Try again tomorrow.",
        ),
        ErrorCode.TOO_MANY_REQUESTS: (
            http_status.HTTP_429_TOO_MANY_REQUESTS,
            "Too many requests. Please slow down.",
        ),
        
        # Database & Data
        ErrorCode.DATABASE_ERROR: (
            http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Database error. Please try again.",
        ),
        ErrorCode.DATABASE_CONNECTION_FAILED: (
            http_status.HTTP_503_SERVICE_UNAVAILABLE,
            "Database connection failed. Please try again later.",
        ),
        ErrorCode.DATA_INTEGRITY_ERROR: (
            http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Data integrity error. Please contact support.",
        ),
        ErrorCode.TRANSACTION_FAILED: (
            http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Transaction failed. Please try again.",
        ),
        
        # External Services
        ErrorCode.EXTERNAL_SERVICE_ERROR: (
            http_status.HTTP_503_SERVICE_UNAVAILABLE,
            "External service error. Please try again later.",
        ),
        ErrorCode.GEMINI_SERVICE_ERROR: (
            http_status.HTTP_503_SERVICE_UNAVAILABLE,
            "AI service temporarily unavailable. Please try again.",
        ),
        ErrorCode.EMAIL_SERVICE_ERROR: (
            http_status.HTTP_503_SERVICE_UNAVAILABLE,
            "Email service temporarily unavailable.",
        ),
        ErrorCode.SERVICE_UNAVAILABLE: (
            http_status.HTTP_503_SERVICE_UNAVAILABLE,
            "Service temporarily unavailable. Please try again later.",
        ),
        ErrorCode.SERVICE_TIMEOUT: (
            http_status.HTTP_504_GATEWAY_TIMEOUT,
            "Request timeout. Please try again.",
        ),
        
        # Internal Errors
        ErrorCode.INTERNAL_SERVER_ERROR: (
            http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Internal server error. Please try again.",
        ),
        ErrorCode.UNHANDLED_EXCEPTION: (
            http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unexpected error occurred. Please try again.",
        ),
        ErrorCode.CONFIGURATION_ERROR: (
            http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Configuration error. Please contact support.",
        ),
    }
    
    @classmethod
    def get_status(cls, error_code: str) -> int:
        """Get HTTP status code for error code"""
        if error_code in cls._ERROR_MAPPINGS:
            return cls._ERROR_MAPPINGS[error_code][0]
        return http_status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @classmethod
    def get_message(cls, error_code: str) -> str:
        """Get human-readable message for error code"""
        if error_code in cls._ERROR_MAPPINGS:
            return cls._ERROR_MAPPINGS[error_code][1]
        return "An error occurred. Please try again."
    
    @classmethod
    def get_all(cls, error_code: str) -> Tuple[int, str]:
        """Get both status code and message for error code"""
        return cls.get_status(error_code), cls.get_message(error_code)
    
    @classmethod
    def register_error(
        cls,
        error_code: str,
        status_code: int,
        message: str,
    ) -> None:
        """Register a new error code mapping"""
        cls._ERROR_MAPPINGS[error_code] = (status_code, message)
