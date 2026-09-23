class DomainException(Exception):
    pass


class PostNotFoundError(DomainException):
    pass


class UserNotFoundError(DomainException):
    pass


class GroupNotFoundError(DomainException):
    pass


class PermissionDeniedError(DomainException):
    pass


class CannotFollowSelfError(DomainException):
    pass
