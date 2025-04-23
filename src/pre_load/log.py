import logging

from toolkit.repo.db.exceptions import AlreadyExists
from toolkit.types_app import _F

logging.basicConfig(level=logging.INFO)


def logger(prefix: str = "==="):
    def decor(f: _F):
        async def wrapper(*args, **kwargs):
            logging.info(f"{prefix} Loading {f.__name__} data")
            try:
                created = await f(*args, **kwargs)
            except AlreadyExists:
                logging.info(f"{f.__name__} data already exists... exiting.")
                return None
            logging.info(f"{prefix} {created}")
            return created

        return wrapper

    return decor
