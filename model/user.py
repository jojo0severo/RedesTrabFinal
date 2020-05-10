

class User:
    def __init__(self, _id, address, name):
        self.id = _id
        self.is_host = False
        self.name = name
        self.score = 0
        self.playing = None
        self.subject_id = None
        self.group_id = None

    def add_group(self, group_id, subject_id, is_host):
        if self.group_id is None and self.subject_id is None:
            self.group_id = group_id
            self.subject_id = subject_id
            self.is_host = is_host

            self.playing = True

            return True

        return False

    def add_score(self):
        self.score += 1
