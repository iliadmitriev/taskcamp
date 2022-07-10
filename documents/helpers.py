"""
Documents helper functions.

"""
import hashlib
import os
import time


def document_upload_path(instance: object, filename: str) -> str:
    """Generate upload path random hash string."""
    now_date_str = time.time().__str__()
    filename_md5 = hashlib.md5(filename.encode() + now_date_str.encode()).hexdigest()
    _, extension = os.path.splitext(filename)
    full_path = (
        f"documents/{filename_md5[0:2]}/{filename_md5[2:4]}/{filename_md5}{extension}"
    )
    return full_path
