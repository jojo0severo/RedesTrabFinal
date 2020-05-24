

class Subject:
    """
    Essa classe armazena as informações referentes ao assunto como o id, nome, quiz dele e ids dos grupos.
    """

    def __init__(self, _id, name, quiz):
        self.id = _id
        self.name = name
        self.quiz = quiz
        self.group_ids = []

    def add_group(self, group_id):
        self.group_ids.append(group_id)

    def remove_group(self, group_id):
        try:
            self.group_ids.remove(group_id)
            return True

        except ValueError:
            return False
