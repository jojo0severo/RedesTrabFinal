import uuid


class Generator:
    def __call__(self, *args, **kwargs):
        return uuid.uuid4()
