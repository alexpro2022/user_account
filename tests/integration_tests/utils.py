from uuid import uuid4


class PathParamMixin:
    """Placeholder for urls like `/{user_id}`"""

    path_params = dict(user_id=uuid4())
