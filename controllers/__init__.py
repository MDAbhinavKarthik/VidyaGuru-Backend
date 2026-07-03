"""
Vidyaguru API Controllers
Aggregates all feature controllers/routers
"""
from fastapi import APIRouter

from controllers import (
    auth,
    users,
    learning,
    tasks,
    journal,
    progress,
    reminders,
    mentor,
    challenges,
    integrity
)

api_router = APIRouter()

# Include all controller routers (canonical source of truth)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(learning.router)
api_router.include_router(tasks.router)
api_router.include_router(journal.router)
api_router.include_router(progress.router)
api_router.include_router(reminders.router)
api_router.include_router(mentor.router)
api_router.include_router(challenges.router)
api_router.include_router(integrity.router)
