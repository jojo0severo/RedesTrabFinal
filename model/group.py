

class Group:
    def __init__(self, _id, name):
        self.id = _id
        self.name = name
        self.user_ids = []

    def add_user(self, user_id):
        self.user_ids.append(user_id)

    def remove_user(self, user_id):
        try:
            self.user_ids.remove(user_id)
            return True

        except ValueError:
            return False
