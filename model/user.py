

class User:
    def __init__(self, _id, name):
        self.id = _id
        self.name = name

        self.group = None
        self.subject = None
        self.started = False
