from uuid import uuid4


def random_id() -> str:
    return uuid4().hex
