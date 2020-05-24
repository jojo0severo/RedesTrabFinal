

class Group:
    def __init__(self, _id, name):
        self.id = _id
        self.name = name
        self.user_ids = []
        self.winner = None
        self.losers = []

    def add_user(self, user_id):
        self.user_ids.append(user_id)

    def add_points(self, user_id, points):
        if self.winner is None:
            self.winner = (user_id, points)

        else:
            winner_id, winner_points = self.winner
            if winner_points < points:
                self.losers.append((winner_id, winner_points))
                self.winner = (user_id, points)
            else:
                self.losers.append((user_id, points))

    def remove_user(self, user_id):
        try:
            self.user_ids.remove(user_id)

        except ValueError:
            pass

        try:
            self.losers.remove(user_id)
        except ValueError:
            self.winner = None

        return True

    def empty(self):
        return len(self.user_ids) == 0
