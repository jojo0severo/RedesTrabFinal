from controller.manager import Manager


class JSONTransformer:
    def __init__(self):
        self.manager = Manager()

    def connect_user(self, json):
        name = json['name']
        address = json['address']

        result, message = self.manager.add_user(name, address)
        return {'result': True, 'status': 201, 'message': 'User connected', 'data': {'id': message}}

    def get_subjects(self):
        result, message = self.manager.get_subjects()

        json_subjects = []
        for subject in message:
            json_subjects.append({'id': subject.id, 'name': subject.name})

        return {'result': True, 'status': 200, 'message': 'Subjects recovered', 'data': json_subjects}

    def get_groups(self, json):
        subject_id = json['subject_id']

        result, message = self.manager.get_groups(subject_id)
        if result:
            json_groups = []
            for group in message:
                json_groups.append({'id': group.id, 'name': group.name})

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
                'result': True, 'status': 200, 'message': 'Group created', 'data': {'id': message, 'name': group_name}}
        else:
            return {'result': False, 'status': 400, 'message': message, 'data': {}}

    def join_group(self, json):
        user_id = json['user_id']
        subject_id = json['subject_id']
        group_id = json['group_id']

        result, message = self.manager.enter_group(user_id, subject_id, group_id)
        if result:
            return {'result': result, 'status': 200, 'message': message, 'data': {'group_id': group_id}}
        else:
            return {'result': result, 'status': 400, 'message': message, 'data': {}}

    def leave_group(self, json):
        user_id = json['user_id']

        result, message = self.manager.leave_group(user_id)
        if result:
            return {'result': result, 'status': 200, 'message': 'User left the group', 'data': {'group_id': message}}
        else:
            return {'result': result, 'status': 400, 'message': message, 'data': {}}

    def start_match(self, json):
        pass

    def end_match(self, json):
        user_id = json['user_id']

        result, message = self.manager.user_finished(user_id)
        if result:
            status = 200
        else:
            status = 400

        return {'result': result, 'status': status, 'message': message, 'data': {}}

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

            addresses = [user.address for user in self.manager.users.values() if user.group_id is None]

        elif event_name == 'join_group':
            data = self.get_users(json_data['data'])['data']
            resp = {'result': True, 'status': 205, 'message': 'updateUsers', 'data': data}

            users_ids = [obj['id'] for obj in data]
            addresses = [self.manager.users[user_id].address for user_id in users_ids]

        elif event_name == 'leave_group':
            data = self.get_users(json_data['data'])['data']
            resp = {'result': True, 'status': 205, 'message': 'updateUsers', 'data': data}

            users_ids = [obj['id'] for obj in data]
            addresses = [self.manager.users[user_id].address for user_id in users_ids]

        elif event_name == 'start_match':
            addresses = None
            resp = None

        elif event_name == 'end_match':
            addresses = None
            resp = None

        else:
            addresses = None
            resp = None

        try:
            addresses.remove(excluded_address)
        except ValueError:
            pass

        return resp, addresses
