

class User:
    """
    Classe que armazena as informações referentes ao usuário.
    Como o id, o nome, a pontuação atual, o grupo que ele pertence, o assunto escolhido e se já começou a partida.
    """

    def __init__(self, _id, name):
        self.id = _id
        self.name = name

        self.points = 0
        self.group = None
        self.subject = None
        self.started = False
