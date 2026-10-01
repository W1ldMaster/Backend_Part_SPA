import traceback

from app.exceptions import (CannotFollowSelfError, GroupNotFoundError,
                            PermissionDeniedError, PostNotFoundError,
                            UserNotFoundError)
from fastapi import HTTPException


def handle_domain_exception(e: Exception):
    if isinstance(e, (PostNotFoundError, GroupNotFoundError, UserNotFoundError)):
        raise HTTPException(status_code=404, detail=str(e))
    if isinstance(e, PermissionDeniedError):
        raise HTTPException(status_code=403, detail=str(e))
    if isinstance(e, CannotFollowSelfError):
        raise HTTPException(status_code=400, detail=str(e))

    traceback.print_exc()
    raise HTTPException(status_code=500, detail="Internal Server Error")
