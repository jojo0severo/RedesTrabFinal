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

    def add_user(self, name):
        _id = Generator()
        self.users[_id] = User(_id, name)

    def add_group(self, user_id, subject_id, group_name):
        if user_id not in self.users:
            return False

        if subject_id not in self.subjects:
            return False

        _id = Generator()

        if not self.users[user_id].add_group(group_id=_id, subject_id=subject_id, is_host=True):
            return False

        group = Group(_id, group_name)
        group.add_user(user_id)

        self.groups[_id] = group
        self.subjects[subject_id].add_group(_id)

        return True

    def enter_group(self, user_id, subject_id, group_id):
        if user_id not in self.users:
            return False

        if subject_id not in self.subjects:
            return False

        if group_id not in self.groups:
            return False

        if not self.users[user_id].add_group(group_id=group_id, subject_id=subject_id, is_host=False):
            return False

        self.groups[group_id].add_user(user_id)

        return True

    def cancel_group(self, user_id):
        if user_id not in self.users:
            return False

        user = self.users[user_id]
        if user.is_host:
            if not self.subjects[user.subject_id].remove_group(user.group_id):
                return False

            user.group = None
            user.subject = None
            self.groups.pop(user.group_id)

            return True

        return False

    def user_finished(self, user_id):
        if user_id not in self.users:
            return False

        user = self.users[user_id]
        if not user.playing:
            return False

        user.playing = False
        return True

    def all_finished(self, user_id):
        user = self.users[user_id]
        for us_id in self.groups[user.group_id].user_ids:
            if self.users[us_id].playing:
                return False

        return True
