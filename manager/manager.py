from threading import Lock
from manager.json_helper import *
from manager.client_socket import ClientSender
from manager.client_socket import ClientReceiver
from model.user import User
from model.subject import Subject
from model.group import Group
from model.quiz import Quiz
from model.question import Question


class Manager:
    def __init__(self, host, port, server_host, server_port, buffer_size):
        self.quiz = None
        self.user = None
        self.winner = None
        self.ready = False
        self.losers = []
        self.subjects = []
        self.groups = []

        self.lock = Lock()
        self.sender = ClientSender(host=host,
                                   port=port,
                                   server_host=server_host,
                                   server_port=server_port,
                                   buffer_size=buffer_size)

        ClientReceiver(manager=self, lock=self.lock, host=host, port=port + 1, buffer_size=buffer_size)

    @decorate_user
    def get_user(self):
        return self.user

    def connect_user(self, user_name):
        resp = self._send('connect', user_name)

        self.user = User(resp['data']['id'], resp['data']['name'])

    @decorate_subjects
    def get_subjects(self):
        return self.subjects

    def recover_subjects(self):
        resp = self._send('getSubjects')

        self.subjects.clear()
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

        resp = self._send('getGroups', subject_id)

        self.groups.clear()
        if resp['result']:
            for group in resp['data']:
                self.groups.append(Group(group['id'], group['groupName']))

        else:
            self.groups.append(Group(0, resp['message']))

    @decorate_group
    def get_group(self):
        return self.user.group

    def enter_group(self, group_id):
        resp = self._send('joinGroup', [self.user.id, self.user.subject.id, group_id])

        if resp['result']:
            for group in self.groups:
                if group.id == group_id:
                    group.users = resp['data']
                    self.user.group = group
                    break

        else:
            for group in self.groups:
                if group.id == group_id:
                    group.users = ['Group not found on server']
                    self.user.group = group
                    break

    def create_group(self, group_name):
        resp = self._send('createGroup', [self.user.id, self.user.subject.id, group_name])

        if resp['result']:
            group = Group(resp['data']['id'], resp['data']['groupName'])
            group.users = [self.user.name]

        else:
            group = Group(0, resp['message'])

        self.groups.append(group)
        self.user.group = group

    def leave_group(self):
        resp = self._send('leaveGroup', self.user.id)

        self.groups.clear()
        if resp['result']:
            self.user.group = None
            for group in resp['data']:
                self.groups.append(Group(group['id'], group['groupName']))

        else:
            self.groups.append(Group(0, resp['message']))

    def start_match(self):
        if self.user.started:
            if self.ready:
                return True
            return False

        self.user.started = True

        resp = self._send('startMatch', self.user.id)
        if resp['result']:
            self.ready = True

            questions = []
            for question in resp['data']:
                questions.append(
                    Question(question['questionTitle'], question['alternatives'], question['correctAlternative']))

            self.quiz = Quiz(self.user.subject.name, questions)

            return True

        return False

    @decorate_question
    def get_question(self):
        next_question = self.quiz.next_question()

        if next_question is False:
            return None

        return next_question

    def get_results(self):
        return self.winner is not None

    def end_match(self):
        resp = self._send('endMatch', [self.user.id, self.quiz.points()])
        if resp['result']:
            self.update_end_game(resp['data'])
            self.quiz = None
            self.ready = False
            self.user.started = False
            return True

        return False

    def add_previous_answer(self, answer):
        self.quiz.add_answer(answer)

    @transform
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

        elif event == 'leaveGroup':
            data = leave_group_request(data)

        elif event == 'startMatch':
            data = start_match_request(data)

        elif event == 'endMatch':
            data = end_match_request(*data)

        data = data.encode('utf-8')

        self.lock.acquire()
        resp = self.sender.send(data)
        self.lock.release()

        return resp

    def handle_update(self, data):
        data = json.loads(data)
        if data['message'] == 'updateGroups':
            self.update_groups(data['data'])

        elif data['message'] == 'updateUsers':
            self.update_users(data['data'])

        elif data['message'] == 'startMatch':
            self.ready = True
            self.update_quiz(data['data'])

        elif data['message'] == 'endMatch':
            self.update_end_game(data['data'])

    def update_groups(self, groups):
        for group in groups:
            self.groups.append(Group(group['id'], group['groupName']))

    def update_users(self, users):
        self.user.group.users.clear()
        for user in users:
            self.user.group.users.append(user['name'])

    def update_quiz(self, questions):
        obj_questions = []
        for q in questions:
            obj_questions.append(Question(q['questionTitle'], q['alternatives'], q['correctAlternative']))

        self.quiz = Quiz(self.user.subject.name, obj_questions)

    def update_end_game(self, data):
        self.winner = data['winner']
        self.losers = data['losers']

        if self.user.id == data['winner'][0]:
            self.user.points = data['winner'][2]
        else:
            for loser in self.losers:
                if loser[0] == self.user.id:
                    self.user.points = loser[2]
                    break

    def get_message(self):
        if self.winner[0] == self.user.id:
            message = f'Parabens, {self.user.name}, voce ganhou com {self.user.points} pontos!'

        else:
            difference = self.winner[2] - self.user.points
            if difference == 0:
                message = f'Voce empatou com o jogador {self.winner[1]} com {self.user.points} pontos.'
            else:
                message = f'Sinto muito, {self.user.name}, voce perdeu para {self.winner[1]} por {difference} ' \
                    f'ponto{"s" if difference > 1 else ""}.'

        self.user.points = 0

        return message
