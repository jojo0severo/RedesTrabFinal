import time
import json
import socket
from controller.json_transformer import JSONTransformer


class SocketServer:
    def __init__(self, host='127.0.0.1', port=8080):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        print(f'Listening into: "{host}:{port}"')

        self.transformer = JSONTransformer()

        self.event_handler = {
            'connect': self.connect_user,
            'getSubjects': self.get_subjects,
            'getGroups': self.get_groups,
            'getUsers': self.get_users,
            'createGroup': self.create_group,
            'joinGroup': self.join_group,
            'leaveGroup': self.leave_group,
            'startMatch': self.start_match,
            'endMatch': self.end_match
        }

    def listen(self):
        while True:
            message, address = self.socket.recvfrom(4096)
            self.handle(message.decode('utf-8').replace('\'', '"'), address)

    def handle(self, data, address):
        try:
            json_received = json.loads(data)

            event = json_received['event']
            if event == 'connect':
                json_received['json']['address'] = address

            if event not in self.event_handler:
                self.unrecognized(address, event)
            else:
                self.event_handler.get(event)(address, json_received['json'])

        except json.JSONDecodeError as err:
            self.json_decode_error(address, data, str(err))

    def send(self, message, address):
        self.socket.sendto(message, address)
        now = time.time()
        while time.time() - now < 5:
            msg, addr = self.socket.recvfrom(4096)
            msg = msg.decode('utf-8')
            if addr == address and msg.lower() == 'ok':
                self.socket.sendto('ok'.encode('utf-8'), address)
                self.check_ok(address)
                return

        self.send(message, address)

    def check_ok(self, address):
        self.socket.sendto('ok'.encode('utf-8'), address)

        now = time.time()
        while time.time() - now < 5:
            msg, addr = self.socket.recvfrom(4096)
            msg = msg.decode('utf-8')
            if addr == address and msg.lower() == 'ok':
                return
            else:
                break

        self.check_ok(address)

    def connect_user(self, address, json_data):
        response = self.transformer.connect_user(json_data)

        str_resp = json.dumps(response).encode('utf-8')
        self.send(str_resp, address)

    def get_subjects(self, address, json_data):
        response = self.transformer.get_subjects()

        str_resp = json.dumps(response).encode('utf-8')
        self.send(str_resp, address)

    def get_groups(self, address, json_data):
        response = self.transformer.get_groups(json_data)

        str_resp = json.dumps(response).encode('utf-8')
        self.send(str_resp, address)

    def get_users(self, address, json_data):
        response = self.transformer.get_users(json_data)

        str_resp = json.dumps(response).encode('utf-8')
        self.send(str_resp, address)

    def create_group(self, address, json_data):
        response = self.transformer.create_group(json_data)

        str_resp = json.dumps(response).encode('utf-8')
        self.send(str_resp, address)

        if response['result']:
            update_response, addresses = self.transformer.get_update_response('create_group', address, json_data)
            str_update_resp = json.dumps(update_response).encode('utf-8')
            for addr in addresses:
                self.send(str_update_resp, addr)

    def join_group(self, address, json_data):
        response = self.transformer.join_group(json_data)

        str_resp = json.dumps(response).encode('utf-8')
        self.send(str_resp, address)

        if response['result']:
            update_response, addresses = self.transformer.get_update_response('join_group', address, response)
            str_update_resp = json.dumps(update_response).encode('utf-8')
            for addr in addresses:
                self.send(str_update_resp, addr)

    def leave_group(self, address, json_data):
        response = self.transformer.leave_group(json_data)

        str_resp = json.dumps(response).encode('utf-8')
        self.send(str_resp, address)

        if response['result']:
            update_response, addresses = self.transformer.get_update_response('leave_group', address, response)
            str_update_resp = json.dumps(update_response).encode('utf-8')
            for addr in addresses:
                self.send(str_update_resp, addr)

    def start_match(self, address, json_data):
        # str_resp = json.dumps(response).encode('utf-8')
        # self.send(str_resp, address)
        pass

    def end_match(self, address, json_data):
        # str_resp = json.dumps(response).encode('utf-8')
        # self.send(str_resp, address)
        pass

    def unrecognized(self, address, event):
        resp = self.transformer.unrecognized(event)
        str_resp = json.dumps(resp).encode('utf-8')
        self.send(str_resp, address)

    def json_decode_error(self, address, json_data, error):
        resp = self.transformer.json_decode_error(json_data, error)
        str_resp = json.dumps(resp).encode('utf-8')
        self.send(str_resp, address)


if __name__ == '__main__':
    s = SocketServer()

