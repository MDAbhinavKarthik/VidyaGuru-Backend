"""
Root-level database bridge for VidyaGuru Backend.
Exports standard database session generators, engines, and Base models from core.database.
"""
from core.database import (
    Base,
    engine,
    async_session_maker,
    get_db,
    init_db,
    close_db,
)

__all__ = [
    "Base",
    "engine",
    "async_session_maker",
    "get_db",
    "init_db",
    "close_db",
]
