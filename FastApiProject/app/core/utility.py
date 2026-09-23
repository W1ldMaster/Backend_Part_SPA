import traceback
from fastapi import HTTPException

from app.exceptions import (
    PostNotFoundError,
    PermissionDeniedError,
    GroupNotFoundError,
    UserNotFoundError,
    CannotFollowSelfError,
)


def handle_domain_exception(e: Exception):
    if isinstance(e, (PostNotFoundError, GroupNotFoundError, UserNotFoundError)):
        raise HTTPException(status_code=404, detail=str(e))
    if isinstance(e, PermissionDeniedError):
        raise HTTPException(status_code=403, detail=str(e))
    if isinstance(e, CannotFollowSelfError):
        raise HTTPException(status_code=400, detail=str(e))

    # всё остальное — неожиданное, логируем и отдаём 500
    traceback.print_exc()
    raise HTTPException(status_code=500, detail="Internal Server Error")