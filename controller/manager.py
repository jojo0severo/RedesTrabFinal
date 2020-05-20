from controller.id_generator import Generator
from model.user import User
from model.subject import Subject
from model.group import Group


class Manager:
    def __init__(self):
        self.users = {}
        self.subjects = {}
        self.groups = {}

    def _add_subject(self, name):
        _id = Generator()
        self.subjects[_id] = Subject(_id, name)

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
            return True, (self.users[user_id], None)

        return True, (self.users[user_id], group_id)

    def user_finished(self, user_id):
        if user_id not in self.users:
            return False, 'User not registered'

        user = self.users[user_id]
        if not user.playing:
            return False, 'User is not playing'

        user.playing = False

        return True, 'User finished'

    def all_finished(self, user_id):
        user = self.users[user_id]
        for us_id in self.groups[user.group_id].user_ids:
            if self.users[us_id].playing:
                return False

        return True
