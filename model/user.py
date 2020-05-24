

class User:
    """
    Classe que armazena as informações do usuário.
    Como: id, endereço, endereço de resposta (um é para respostas das requisições e outro para atualizações),
    informação se ele é o criador do grupo, nome, pontuação, se está jogando, id do assunto escolhido e id do grupo
    escolhido.
    """

    def __init__(self, _id, address, name):
        self.id = _id
        self.address = address
        self.receive_address = (address[0], address[1] + 1)
        self.is_host = False
        self.name = name
        self.score = 0
        self.playing = None
        self.subject_id = None
        self.group_id = None

    def add_group(self, group_id, subject_id, is_host):
        if self.group_id is None:
            self.group_id = group_id
            self.is_host = is_host

        else:
            return False

        self.subject_id = subject_id

        return True

    def add_score(self):
        self.score += 1

    def leave_group(self):
        self.group_id = None
        self.is_host = False
