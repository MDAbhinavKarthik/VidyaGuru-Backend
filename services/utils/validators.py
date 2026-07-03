"""
Common Validators

Centralized validation functions for common data types and patterns.
Used across endpoints and services to ensure data consistency.

Usage:
    from utils.validators import (
        validate_email,
        validate_password,
        validate_difficulty,
        validate_category
    )
    
    if not validate_email(user_email):
        raise ValidationError("email", "Invalid email format")
"""

import re
from typing import Optional, List, Tuple
from datetime import datetime

from utils.constants import (
    CHALLENGE_CATEGORIES,
    CHALLENGE_DIFFICULTIES,
    USER_ROLES,
    PASSWORD_MIN_LENGTH,
    PASSWORD_REQUIRE_UPPERCASE,
    PASSWORD_REQUIRE_LOWERCASE,
    PASSWORD_REQUIRE_NUMBERS,
    PASSWORD_REQUIRE_SPECIAL,
)


# ============================================================================
# Email & Contact Validators
# ============================================================================

def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email)) if email else False


def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Accepts various formats: +1234567890, 123-456-7890, etc.
    pattern = r"^(\+\d{1,3})?[-.\s]?\d{1,14}$"
    return bool(re.match(pattern, phone)) if phone else False


# ============================================================================
# Password Validators
# ============================================================================

def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength according to policy.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password or len(password) < PASSWORD_MIN_LENGTH:
        return False, f"Password must be at least {PASSWORD_MIN_LENGTH} characters"
    
    if PASSWORD_REQUIRE_UPPERCASE and not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if PASSWORD_REQUIRE_LOWERCASE and not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if PASSWORD_REQUIRE_NUMBERS and not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    if PASSWORD_REQUIRE_SPECIAL and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    
    return True, None


def check_password_strength(password: str) -> dict:
    """
    Get detailed password strength analysis.
    
    Returns:
        Dict with strength_score (0-100) and feedback
    """
    score = 0
    feedback = []
    
    # Length
    if len(password) >= 8:
        score += 20
    if len(password) >= 12:
        score += 10
    if len(password) >= 16:
        score += 10
    
    # Complexity
    if re.search(r"[a-z]", password):
        score += 10
    if re.search(r"[A-Z]", password):
        score += 10
    if re.search(r"\d", password):
        score += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 20
    
    # Variety
    unique_chars = len(set(password))
    if unique_chars > 10:
        score += 10
    
    # Feedback
    if score < 40:
        feedback.append("Password is weak")
    elif score < 70:
        feedback.append("Password is fair - consider adding more complexity")
    else:
        feedback.append("Password is strong")
    
    return {
        "strength_score": min(score, 100),
        "feedback": feedback,
        "is_strong": score >= 70,
    }


# ============================================================================
# Challenge & Learning Validators
# ============================================================================

def validate_category(category: str) -> bool:
    """Validate challenge category"""
    return category in CHALLENGE_CATEGORIES


def validate_difficulty(difficulty: str) -> bool:
    """Validate difficulty level"""
    return difficulty in CHALLENGE_DIFFICULTIES


def validate_categories_list(categories: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate list of categories.
    
    Returns:
        Tuple of (all_valid, valid_categories)
    """
    valid = [c for c in categories if validate_category(c)]
    return len(valid) == len(categories), valid


def validate_role(role: str) -> bool:
    """Validate user role"""
    return role in USER_ROLES


# ============================================================================
# Content Validators
# ============================================================================

def validate_title(title: str, min_len: int = 3, max_len: int = 200) -> bool:
    """Validate title length"""
    return title and min_len <= len(title.strip()) <= max_len


def validate_description(
    description: str,
    min_len: int = 10,
    max_len: int = 5000
) -> bool:
    """Validate description length"""
    return description and min_len <= len(description.strip()) <= max_len


def validate_code(code: str, min_len: int = 10) -> bool:
    """Validate code submission"""
    return code and len(code.strip()) >= min_len


def sanitize_text(text: str, max_length: int = 10000) -> str:
    """
    Sanitize text input:
    - Remove leading/trailing whitespace
    - Truncate if too long
    - Preserve formatting
    """
    text = text.strip()
    return text[:max_length] if len(text) > max_length else text


# ============================================================================
# Numeric Validators
# ============================================================================

def validate_score(score: float) -> bool:
    """Validate score is 0-100"""
    return isinstance(score, (int, float)) and 0 <= score <= 100


def validate_percentage(value: float) -> bool:
    """Validate percentage 0-100"""
    return isinstance(value, (int, float)) and 0 <= value <= 100


def validate_xp(xp: int) -> bool:
    """Validate XP is positive"""
    return isinstance(xp, int) and xp >= 0


# ============================================================================
# Date/Time Validators
# ============================================================================

def validate_date(date: datetime) -> bool:
    """Validate date is in the past or present"""
    return isinstance(date, datetime) and date <= datetime.now()


def validate_future_date(date: datetime) -> bool:
    """Validate date is in the future"""
    return isinstance(date, datetime) and date > datetime.now()


def validate_time_range(start: datetime, end: datetime) -> bool:
    """Validate end time is after start time"""
    return isinstance(start, datetime) and isinstance(end, datetime) and end > start


# ============================================================================
# UUID & ID Validators
# ============================================================================

def validate_uuid(value: str) -> bool:
    """Validate UUID format"""
    import uuid
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


def validate_positive_int(value: int) -> bool:
    """Validate positive integer"""
    return isinstance(value, int) and value > 0


def validate_non_negative_int(value: int) -> bool:
    """Validate non-negative integer"""
    return isinstance(value, int) and value >= 0


# ============================================================================
# Composite Validators
# ============================================================================

def validate_user_input(
    email: str,
    password: str,
    name: Optional[str] = None,
) -> Tuple[bool, List[str]]:
    """
    Validate user registration input.
    
    Returns:
        Tuple of (all_valid, list_of_errors)
    """
    errors = []
    
    if not validate_email(email):
        errors.append("Invalid email format")
    
    valid_password, password_error = validate_password(password)
    if not valid_password:
        errors.append(password_error)
    
    if name and not validate_title(name, min_len=2, max_len=100):
        errors.append("Name must be between 2 and 100 characters")
    
    return len(errors) == 0, errors


def validate_challenge_input(
    title: str,
    description: str,
    category: str,
    difficulty: str,
) -> Tuple[bool, List[str]]:
    """
    Validate challenge creation input.
    
    Returns:
        Tuple of (all_valid, list_of_errors)
    """
    errors = []
    
    if not validate_title(title):
        errors.append("Title must be between 3 and 200 characters")
    
    if not validate_description(description):
        errors.append("Description must be between 10 and 5000 characters")
    
    if not validate_category(category):
        errors.append(f"Invalid category. Must be one of: {', '.join(CHALLENGE_CATEGORIES.keys())}")
    
    if not validate_difficulty(difficulty):
        errors.append(f"Invalid difficulty. Must be one of: {', '.join(CHALLENGE_DIFFICULTIES.keys())}")
    
    return len(errors) == 0, errors


# ============================================================================
# Batch Validators
# ============================================================================

def validate_list_not_empty(items: List, item_name: str = "items") -> Tuple[bool, Optional[str]]:
    """Validate list is not empty"""
    if not items or len(items) == 0:
        return False, f"At least one {item_name} is required"
    return True, None


def validate_list_length(
    items: List,
    min_len: int = None,
    max_len: int = None,
    item_name: str = "items"
) -> Tuple[bool, Optional[str]]:
    """Validate list length within bounds"""
    length = len(items) if items else 0
    
    if min_len and length < min_len:
        return False, f"Must have at least {min_len} {item_name}"
    
    if max_len and length > max_len:
        return False, f"Cannot have more than {max_len} {item_name}"
    
    return True, None
