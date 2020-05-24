from controller.database_loader import Loader


class JSONTransformer:
    def __init__(self):
        self.manager = Loader().manager

    def connect_user(self, json):
        name = json['name']
        address = json['address']

        result, message = self.manager.add_user(name, address)
        return {'result': True, 'status': 201, 'message': 'User connected', 'data': {'id': message, 'name': name}}

    def get_subjects(self):
        result, message = self.manager.get_subjects()

        json_subjects = []
        for subject in message:
            json_subjects.append({'id': subject.id, 'subjectName': subject.name})

        return {'result': True, 'status': 200, 'message': 'Subjects recovered', 'data': json_subjects}

    def get_groups(self, json):
        subject_id = json['subject_id']

        result, message = self.manager.get_groups(subject_id)
        if result:
            json_groups = []
            for group in message:
                json_groups.append({'id': group.id, 'groupName': group.name})

            return {'result': True, 'status': 200, 'message': 'Groups recovered', 'data': json_groups}

        else:
            return {'result': False, 'status': 400, 'message': message, 'data': []}

    def get_users(self, json):
        group_id = json['group_id']

        result, message = self.manager.get_users(group_id)
        if result:
            json_users = []
            for user in message:
                json_users.append({'id': user.id, 'name': user.name})

            return {'result': True, 'status': 200, 'message': 'Users recovered', 'data': json_users}

        else:
            return {'result': False, 'status': 400, 'message': message, 'data': []}

    def create_group(self, json):
        user_id = json['user_id']
        subject_id = json['subject_id']
        group_name = json['group_name']

        result, message = self.manager.add_group(user_id, subject_id, group_name)
        if result:
            return {
                'result': True, 'status': 200, 'message': 'Group created',
                'data': {
                    'id': message[0],
                    'groupName': group_name
                }
            }
        else:
            return {'result': False, 'status': 400, 'message': message, 'data': {}}

    def join_group(self, json):
        user_id = json['user_id']
        subject_id = json['subject_id']
        group_id = json['group_id']

        result, message = self.manager.enter_group(user_id, subject_id, group_id)
        if result:
            return {'result': result, 'status': 200, 'message': 'User joined the group', 'data': message}, {
                'group_id': group_id}
        else:
            return {'result': result, 'status': 400, 'message': message, 'data': {}}, None

    def leave_group(self, json):
        user_id = json['user_id']

        result, message = self.manager.leave_group(user_id)
        if result:
            if message[1] is None:
                json_groups = []
            else:
                _, groups = self.manager.get_groups(message[0].subject_id)

                json_groups = []
                for group in groups:
                    json_groups.append({'id': group.id, 'groupName': group.name})

            return {'result': True, 'status': 200, 'message': 'User left the group', 'data': json_groups}, {
                'group_id': message[1]}

        else:
            return {'result': False, 'status': 400, 'message': message, 'data': []}, None

    def start_match(self, json):
        user_id = json['user_id']

        result, message = self.manager.start_match(user_id)
        if result:
            if isinstance(message, str):
                return {'result': False, 'status': 200, 'message': message, 'data': []}, None

            group_id = self.manager.users[user_id].group_id
            json_questions = []
            for question in message:
                json_questions.append({
                    'questionTitle': question.title,
                    'alternatives': question.alternatives,
                    'correctAlternative': question.correct_alternative})

            return {'result': True, 'status': 200, 'message': 'Match recovered', 'data': json_questions}, {
                'group_id': group_id}

        return {'result': False, 'status': 500, 'message': message, 'data': []}, None

    def end_match(self, json):
        user_id = json['user_id']
        points = json['user_points']

        result, message = self.manager.end_match(user_id, points)
        if result:
            group_id = message['group_id']
            message = {'winner': message['winner'], 'losers': message['losers']}
            return {'result': True, 'status': 200, 'message': 'User finished', 'data': message}, {'group_id': group_id}

        else:
            return {'result': False, 'status': 400, 'message': message, 'data': {}}, None

    def unrecognized(self, event):
        return {'result': False, 'status': 400, 'message': 'Unrecognized event', 'data': {'received': str(event)}}

    def json_decode_error(self, data, error):
        return {
            'result': False, 'status': 400, 'message': 'JSON Decode error',
            'data': {'received': str(data), 'error_message': error}
        }

    def get_update_response(self, event_name, excluded_address, json_data):
        if event_name == 'create_group':
            data = self.get_groups(json_data)['data']
            resp = {'result': True, 'status': 205, 'message': 'updateGroups', 'data': data}

            addresses = [user.receive_address for user in self.manager.users.values() if user.group_id is None]

        elif event_name == 'join_group':
            data = self.get_users(json_data)['data']
            resp = {'result': True, 'status': 205, 'message': 'updateUsers', 'data': data}

            users_ids = [obj['id'] for obj in data]
            addresses = [self.manager.users[user_id].receive_address for user_id in users_ids]

        elif event_name == 'leave_group':
            data = self.get_users(json_data)['data']
            resp = {'result': True, 'status': 205, 'message': 'updateUsers', 'data': data}

            users_ids = [obj['id'] for obj in data]
            addresses = [self.manager.users[user_id].receive_address for user_id in users_ids]

        elif event_name == 'start_match':
            data = [{
                'questionTitle': question.title,
                'alternatives': question.alternatives,
                'correctAlternative': question.correct_alternative} for question in
                self.manager.get_questions(json_data)]

            resp = {'result': True, 'status': 205, 'message': 'startMatch', 'data': data}

            users_ids = [obj['id'] for obj in self.get_users(json_data)['data']]
            addresses = [self.manager.users[user_id].receive_address for user_id in users_ids]

        elif event_name == 'end_match':
            group = self.manager.groups[json_data['group_id']]
            winner = self.manager.users[group.winner[0]].name

            resp = {
                'result': True,
                'status': 205,
                'message': 'endMatch',
                'data': {
                    'winner': [group.winner[0], winner, group.winner[1]],
                    'losers': [[loser[0], self.manager.users[loser[0]].name, loser[1]] for loser in group.losers]
                }
            }

            users_ids = [obj['id'] for obj in self.get_users(json_data)['data']]
            addresses = [self.manager.users[user_id].receive_address for user_id in users_ids]

        else:
            addresses = None
            resp = None

        try:
            addresses.remove(excluded_address)
        except ValueError:
            pass

        return resp, addresses
