import uuid


class Generator:
    def __new__(cls, *args, **kwargs):
        return str(uuid.uuid4())
