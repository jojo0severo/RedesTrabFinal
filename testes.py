from server import SocketServer


if __name__ == '__main__':
    s = SocketServer()

    s.handle('{"event": "connect", "json": {"name": "joao"}}'.encode('utf-8'), ('127.0.0.1', 8000))

    s.handle('{"event": "getSubjects", "json": {}}'.encode('utf-8'), ('127.0.0.1', 8000))

    subject_id = list(s.transformer.manager.subjects.keys())[0]
    s.handle(('{"event": "getGroups", "json": {"subject_id": "%s"}}' % subject_id).encode('utf-8'), ('127.0.0.1', 8000))

    user_id = s.transformer.connect_user({'name': 'joaozinho', 'address': ('127.0.0.1', 8000)})['data']['id']
    subject_id = list(s.transformer.manager.subjects.keys())[0]
    s.handle(('{"event": "createGroup", "json": '
              '{"user_id": "%s", "subject_id": "%s", "group_name": "batata"}}' % (user_id, subject_id)
              ).encode('utf-8'), ('127.0.0.1', 8000))

    s.handle(('{"event": "leaveGroup", "json": {"user_id": "%s"}}' % user_id).encode('utf-8'), ('127.0.0.1', 8000))

    user_id = s.transformer.connect_user({'name': 'carlinho', 'address': ('127.0.0.1', 8000)})['data']['id']
    group_id = list(s.transformer.manager.groups.keys())[0]
    s.handle(('{"event": "joinGroup", "json": '
             '{"user_id": "%s", "subject_id": "%s", "group_id": "%s"}}' % (user_id, subject_id, group_id)).encode('utf-8'), ('127.0.0.1', 8000))

    s.handle(('{"event": "getUsers", "json": {"group_id": "%s"}}' % group_id).encode('utf-8'), ('127.0.0.1', 8000))

    s.handle('error'.encode('utf-8'), ('127.0.0.1', 8000))