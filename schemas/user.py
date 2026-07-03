from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class UserProfileUpdate(BaseModel):
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    learning_goals: Optional[str] = None

class OnboardingData(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    education_level: Optional[str] = None
    interests: Optional[list[str]] = None
    learning_goals: Optional[str] = None

class UserProfileResponse(BaseModel):
    id: int
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    learning_goals: Optional[str] = None

    class Config:
        from_attributes = True
    
class CurrentUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool = True

    class Config:
        from_attributes = True