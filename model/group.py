

class Group:
    """
    Classe que armazena as informações referentes ao grupo como os nomes dos usuarios que estao no grupo.
    """
    def __init__(self, _id, name):
        self.id = _id
        self.name = name
        self.users = []
