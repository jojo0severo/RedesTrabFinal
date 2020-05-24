

class User:
    def __init__(self, _id, name):
        self.id = _id
        self.name = name

        self.points = 0
        self.group = None
        self.subject = None
        self.started = False
