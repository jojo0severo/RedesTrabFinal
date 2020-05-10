from controller.manager import Manager


class JSONTransformer:
    def __init__(self):
        self.manager = Manager()

    def connect_user(self, json):
        name = json['name']
        address = json['address']
        
        result, message = self.manager.add_user(name, address)
        return {'result': True, 'status': 201, 'message': 'User connected', 'data': {'id': message}}

    def get_subjects(self, json):
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
            return {'result': True, 'status': 200, 'message': 'Group created', 'data': {'id': message, 'name': group_name}}
        else:
            return {'result': False, 'status': 400, 'message': message, 'data': {}}

    def join_group(self, json):
        user_id = json['user_id']
        subject_id = json['subject_id']
        group_id = json['group_id']

        result, message = self.manager.enter_group(user_id, subject_id, group_id)
        if result:
            status = 200
        else:
            status = 400

        return {'result': result, 'status': status, 'message': message, 'data': {}}

    def leave_group(self, json):
        user_id = json['user_id']

        result, message = self.manager.leave_group(user_id)
        if result:
            status = 200
        else:
            status = 400

        return {'result': result, 'status': status, 'message': message, 'data': {}}

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

    def unrecognized(self):
        return {'result': False, 'status': 400, 'message': 'Unrecognized event', 'data': {}}
