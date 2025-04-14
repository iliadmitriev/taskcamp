"""
Celery worker package.
"""

from .app import celery_app

__all__ = ["celery_app"]
