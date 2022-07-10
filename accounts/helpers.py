"""
Helper functions module.
"""
import uuid
from typing import Tuple

from django.conf import settings
from django.core.cache import cache


def generate_user_hash_and_token(user_id: int) -> Tuple[str, str]:
    """Generate user hash and token pair.

    Save token to cache.
    """
    user_hash = uuid.uuid4().hex
    token = uuid.uuid4().hex

    cache.set(
        user_hash,
        {"token": token, "user_id": user_id},
        settings.ACCOUNT_ACTIVATION_LINK_EXPIRE,
    )
    return user_hash, token
