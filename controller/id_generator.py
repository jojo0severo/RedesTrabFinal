import uuid


class Generator:
    """
    Classe para gerar ID's unicos
    """

    def __new__(cls, *args, **kwargs):
        return str(uuid.uuid4())
