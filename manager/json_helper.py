import json


def transform(function):
    def transform(*args, **kwargs):
        resp = function(*args, **kwargs)

        return json.loads(resp.replace('\'', '"'))

    return transform


def get_connection_request(name):
    return json.dumps({"event": "connect", "json": {"name": name}})


def get_subjects_request():
    return json.dumps({"event": "getSubjects", "json": {}})


def get_groups_request(subject_id):
    return json.dumps({"event": "getGroups", "json": {"subject_id": subject_id}})


def join_group_request(user_id, subject_id, group_id):
    return json.dumps({"event": "joinGroup", "json": {"user_id": user_id, "subject_id": subject_id, "group_id": group_id}})


def create_group_request(user_id, subject_id, group_name):
    return json.dumps({"event": "createGroup", "json": {"user_id": user_id, "subject_id": subject_id, "group_name": group_name}})


def leave_group_request(user_id):
    return json.dumps({"event": "leaveGroup", "json": {"user_id": user_id}})


def decorate_user(function):
    def format_user(*args, **kwargs):
        resp = function(*args, **kwargs)

        subject = resp.subject
        json_subject = {}
        if subject is not None:
            json_subject = {'id': subject.id, 'name': subject.name}

        group = resp.group
        json_group = {}
        if group is not None:
            json_group = {'id': group.id, 'name': group.name}

        return {
            'id': resp.id, 'name': resp.name,
            'subject': json_subject,
            'group': json_group
        }

    return format_user


def decorate_subjects(function):
    def format_subjects(*args, **kwargs):
        resp = function(*args, **kwargs)

        subjects = []
        for subject in resp:
            subjects.append((subject.id, subject.name))

        return subjects

    return format_subjects


def decorate_groups(function):
    def format_groups(*args, **kwargs):
        resp = function(*args, **kwargs)

        groups = []
        for group in resp:
            groups.append((group.id, group.name))

        return groups

    return format_groups


def decorate_group(function):
    def format_group(*args, **kwargs):
        resp = function(*args, **kwargs)

        return {'id': resp.id, 'name': resp.name, 'users': resp.users}

    return format_group
