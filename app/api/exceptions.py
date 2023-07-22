from http import HTTPStatus

from fastapi import HTTPException


class PostNotFoundError(HTTPException):
    def __init__(self, post_id: int) -> None:
        status_code = HTTPStatus.NOT_FOUND
        detail = f"Post with id={post_id} not found"
        super().__init__(status_code, detail, None)


class UserDoesNotExists(HTTPException):
    def __init__(self, user_id: int):
        status_code = HTTPStatus.NOT_FOUND
        detail = f"User with id={user_id} does not exists"
        super().__init__(status_code, detail, None)


class UserDoesNotHaveSubscriptions(HTTPException):
    def __init__(self, user_id: int):
        status_code = HTTPStatus.BAD_REQUEST
        detail = f"User with id={user_id} does not have subscriptions"
        super().__init__(status_code, detail, None)
