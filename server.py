import json
from gevent.server import DatagramServer
from controller.json_transformer import JSONTransformer


class MultiThreadServer(DatagramServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.transformer = JSONTransformer()

        self.event_handler = {
            'connect': self.transformer.connect_user,
            'getUsers': self.transformer.get_users,
            'getSubjects': self.transformer.get_subjects,
            'getGroups': self.transformer.get_groups,
            'createGroup': self.transformer.create_group,
            'joinGroup': self.transformer.join_group,
            'leaveGroup': self.transformer.leave_group,
            'startMatch': self.transformer.start_match,
            'endMatch': self.transformer.end_match,
            'ok': self._ok
        }

    def handle(self, data, address):
        json_received = json.loads(data.decode('utf-8'))

        event = json_received['event']
        if event == 'connect':
            json_received['address'] = address

        response = self.event_handler.get(event, default=self.transformer.unrecognized)(json_received['json'])
        self.socket.sendto(json.dumps(response).encode('utf-8'), address)

    def _ok(self, *args):
        return {'result': True, 'status': 200, 'message': 'Ok', 'data': {}}


if __name__ == '__main__':
    print('Receiving datagrams on 127.0.0.1:8080')
    MultiThreadServer('127.0.0.1:8080').serve_forever()
