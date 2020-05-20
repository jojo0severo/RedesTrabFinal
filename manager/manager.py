from threading import Lock
from manager.json_helper import *
from manager.client_socket import ClientSender
from manager.client_socket import ClientReceiver
from model.user import User
from model.subject import Subject
from model.group import Group
from model.quiz import Quiz


class Manager:
    def __init__(self, host='127.0.0.1', port=9000, buffer_size=4096):
        self.quiz = None
        self.user = None
        self.subjects = []
        self.groups = []

        self.lock = Lock()
        self.sender = ClientSender(host=host, port=port - 920, buffer_size=buffer_size)
        ClientReceiver(manager=self, lock=self.lock, host=host, port=port, buffer_size=buffer_size)

    @decorate_user
    def get_user(self):
        return self.user

    def connect_user(self, data):
        # resp = self._send('connect', data)
        # self.user = User(resp['data']['id'], resp['data']['name'])
        self.user = User(0, data)
        return True

    @decorate_subjects
    def get_subjects(self):
        return self.subjects

    def recover_subjects(self):
        # resp = self._send('getSubjects')

        resp = {
            "status": 200,
            "result": True,
            "response": "Subjects recovered",
            "data": [
                {
                    "id": '1',
                    "subjectName": "Assunto 1"
                },
                {
                    "id": '2',
                    "subjectName": "Assunto 2"
                },
                {
                    "id": '3',
                    "subjectName": "Assunto 3"
                }
            ]
        }

        if resp['result']:
            for subject in resp['data']:
                self.subjects.append(Subject(subject['id'], subject['subjectName']))

        else:
            self.subjects.append(Subject(0, resp['message']))

    @decorate_groups
    def get_groups(self):
        return self.groups

    def recover_groups(self, subject_id):
        for subject in self.subjects:
            if subject.id == subject_id:
                self.user.subject = subject
                break

        # resp = self._send('getGroups', data)

        resp = {
            "status": 200,
            "result": True,
            "response": "Groups recovered",
            "data": [
                {
                    "id": '1',
                    "groupName": "Nome da sala 1",
                    "playersNumber": 1
                },
                {
                    "id": '2',
                    "groupName": "Nome da sala 2",
                    "playersNumber": 1
                },
                {
                    "id": '3',
                    "groupName": "Nome da sala 3",
                    "playersNumber": 1
                },
                {
                    "id": '4',
                    "groupName": "Nome da sala 4",
                    "playersNumber": 1
                }
            ]
        }

        if resp['result']:
            for group in resp['data']:
                self.groups.append(Group(group['id'], group['groupName'], group['playersNumber']))

        else:
            self.groups.append(Group(0, resp['message'], 0))

    @decorate_group
    def get_group(self):
        return self.user.group

    def enter_group(self, group_id):
        # resp = self._send('joinGroup', [self.user.id, self.user.subject.id, group_id])

        resp = {
            "status": 201,
            "result": True,
            "response": "Group recovered",
            "data": [
                "nome 1",
                "nome 2",
                "nome 3"
            ]
        }

        if resp['result']:
            for group in self.groups:
                if group.id == group_id:
                    group.users = [*resp['data'], self.user.name]
                    self.user.group = group
                    break

        else:
            for group in self.groups:
                if group.id == group_id:
                    group.users = ['Group not found on server']
                    self.user.group = group
                    break

    def create_group(self, group_name):
        # resp = self._send('createGroup', [self.user.id, self.user.subject.id, group_name])

        resp = {
            "status": 201,
            "result": True,
            "response": "Group created",
            "data": {
                "id": '1',
                'groupName': group_name,
                'playersNumber': 1
            }
        }

        if resp['result']:
            group = Group(resp['data']['id'], resp['data']['groupName'], resp['data']['playersNumber'])
            group.users = [self.user.name]

        else:
            group = Group(0, resp['message'], 0)

        self.groups.append(group)
        self.user.group = group

    def _send(self, event, data=None):
        if event == 'connect':
            data = get_connection_request(data)

        elif event == 'getSubjects':
            data = get_subjects_request()

        elif event == 'getGroups':
            data = get_groups_request(data)

        elif event == 'joinGroup':
            data = join_group_request(*data)

        elif event == 'createGroup':
            data = create_group_request(*data)

        self.lock.acquire()
        resp = self.sender.send(data)
        self.lock.release()

        return resp

    def handle_update(self, data):
        pass
