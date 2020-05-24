from controller.id_generator import Generator
from model.user import User
from model.subject import Subject
from model.group import Group


class Manager:
    def __init__(self):
        self.users = {}
        self.subjects = {}
        self.groups = {}
        self.quizzes = {}

    def add_user(self, name, address):
        _id = Generator()
        self.users[_id] = User(_id, address, name)

        return True, _id

    def get_subjects(self):
        return True, list(self.subjects.values())

    def get_groups(self, subject_id):
        if subject_id not in self.subjects:
            return False, 'Subject not registered'

        group_ids = self.subjects[subject_id].group_ids

        groups = []
        for group_id in group_ids:
            if group_id not in self.groups:
                return False, 'Internal Error'

            groups.append(self.groups[group_id])

        return True, groups

    def get_users(self, group_id):
        if group_id not in self.groups:
            return False, 'Group not registered'

        user_ids = self.groups[group_id].user_ids

        users = []
        for user_id in user_ids:
            if user_id not in self.users:
                return False

            users.append(self.users[user_id])

        return True, users

    def add_group(self, user_id, subject_id, group_name):
        if user_id not in self.users:
            return False, 'User not registered'

        if subject_id not in self.subjects:
            return False, 'Subject not registered'

        _id = Generator()

        if not self.users[user_id].add_group(group_id=_id, subject_id=subject_id, is_host=True):
            return False, 'User already in group'

        group = Group(_id, group_name)
        group.add_user(user_id)

        self.groups[_id] = group
        self.subjects[subject_id].add_group(_id)

        return True, _id

    def enter_group(self, user_id, subject_id, group_id):
        if user_id not in self.users:
            return False, 'User not registered'

        if subject_id not in self.subjects:
            return False, 'Subject not registered'

        if group_id not in self.groups:
            return False, 'Group not registered'

        if not self.users[user_id].add_group(group_id=group_id, subject_id=subject_id, is_host=False):
            return False, 'User already in group'

        self.groups[group_id].add_user(user_id)

        users = [self.users[user_id].name for user_id in self.groups[group_id].user_ids]

        return True, users

    def leave_group(self, user_id):
        if user_id not in self.users:
            return False, 'User not registered'

        if not self.users[user_id].group_id or not self.users[user_id].subject_id:
            return False, 'User not in any group'

        group_id = self.users[user_id].group_id

        if not self.groups[group_id].remove_user(user_id):
            return False, 'User not in the specified group'

        self.users[user_id].leave_group()

        if self.groups[group_id].empty():
            self.groups.pop(group_id)
            self.subjects[self.users[user_id].subject_id].remove_group(group_id)
            return True, (self.users[user_id], None)

        return True, (self.users[user_id], group_id)

    def start_match(self, user_id):
        if user_id not in self.users:
            return False, 'User not registered'

        user = self.users[user_id]
        if not user.playing:
            user.playing = True
            if self.all_started(user.group_id):
                return True, self.subjects[user.subject_id].quiz.questions

            return True, 'Some players still dont started'

        return False, 'User was already playing'

    def end_match(self, user_id, points):
        if user_id not in self.users:
            return False, 'User not registered'

        user = self.users[user_id]
        if not user.playing:
            return False, 'User is not playing'

        user.playing = False
        group = self.groups[user.group_id]
        group.add_points(user_id, points)
        if self.all_finished(user.group_id):
            winner = group.winner
            winner = winner[0], self.users[winner[0]].name, winner[1]

            losers = [[loser[0], self.users[loser[0]].name, loser[1]] for loser in group.losers]

            return True, {'winner': winner, 'losers': losers, 'group_id': user.group_id}

        return False, 'Still waiting for players'

    def get_questions(self, group_id):
        group_id = group_id['group_id']
        user_id = self.groups[group_id].user_ids[0]
        subject_id = self.users[user_id].subject_id

        return self.subjects[subject_id].quiz.questions

    def all_started(self, group_id):
        for us_id in self.groups[group_id].user_ids:
            if not self.users[us_id].playing:
                return False

        return True

    def all_finished(self, group_id):
        for us_id in self.groups[group_id].user_ids:
            if self.users[us_id].playing:
                return False

        return True
