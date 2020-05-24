import json
import socket
from controller.json_transformer import JSONTransformer


class SocketServer:
    def __init__(self, host='127.0.0.1', port=65000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1)
        self.socket.bind((host, port))

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
        print(f'Listening into: "{host}:{port}"')
        self.listen()

    def listen(self):
        while True:
            try:
                message, address = self.socket.recvfrom(4096)
                self.handle(message.decode('utf-8').replace('\'', '"'), address)
            except socket.timeout:
                pass

    def handle(self, data, address):
        try:
            if data.lower() == 'ok':
                self.socket.sendto('ok'.encode('utf-8'), address)
                return
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
        try:
            self.socket.sendto(message, address)

            msg, addr = self.socket.recvfrom(4096)
            msg = msg.decode('utf-8')

            if addr == address and msg.lower() == 'ok':
                self.socket.sendto('ok'.encode('utf-8'), address)
                return

            self.send(message, address)

        except socket.timeout:
            self.send(message, address)

    def connect_user(self, address, json_data):
        response = self.transformer.connect_user(json_data)

        str_resp = json.dumps(response).encode('utf-8')
        try:
            self.send(str_resp, address)
        except:
            pass

    def get_subjects(self, address, json_data):
        response = self.transformer.get_subjects()

        str_resp = json.dumps(response).encode('utf-8')
        try:
            self.send(str_resp, address)
        except:
            pass

    def get_groups(self, address, json_data):
        response = self.transformer.get_groups(json_data)

        str_resp = json.dumps(response).encode('utf-8')
        try:
            self.send(str_resp, address)
        except:
            pass

    def get_users(self, address, json_data):
        response = self.transformer.get_users(json_data)

        str_resp = json.dumps(response).encode('utf-8')
        try:
            self.send(str_resp, address)
        except:
            pass

    def create_group(self, address, json_data):
        response = self.transformer.create_group(json_data)

        str_resp = json.dumps(response).encode('utf-8')
        try:
            self.send(str_resp, address)
        except:
            pass

        if response['result']:
            update_response, addresses = self.transformer.get_update_response('create_group', address, json_data)
            str_update_resp = json.dumps(update_response).encode('utf-8')
            last_addr = None
            try:
                for addr in addresses:
                    last_addr = addr
                    self.send(str_update_resp, addr)
            except:
                for user in self.transformer.manager.users.values():
                    if user.address == last_addr:
                        self.leave_group(last_addr, {'user_id': user.id})
                        break

    def join_group(self, address, json_data):
        response, group_id = self.transformer.join_group(json_data)

        str_resp = json.dumps(response).encode('utf-8')
        try:
            self.send(str_resp, address)
        except:
            pass

        if response['result'] and group_id is not None:
            update_response, addresses = self.transformer.get_update_response('join_group', address, group_id)
            str_update_resp = json.dumps(update_response).encode('utf-8')
            last_addr = None
            try:
                for addr in addresses:
                    last_addr = addr
                    self.send(str_update_resp, addr)
            except:
                for user in self.transformer.manager.users.values():
                    if user.address == last_addr:
                        self.leave_group(last_addr, {'user_id': user.id})
                        break

    def leave_group(self, address, json_data):
        response, group_id = self.transformer.leave_group(json_data)
        str_resp = json.dumps(response).encode('utf-8')
        try:
            self.send(str_resp, address)
        except:
            pass

        if response['result'] and group_id is not None:
            update_response, addresses = self.transformer.get_update_response('leave_group', address, group_id)
            str_update_resp = json.dumps(update_response).encode('utf-8')
            last_addr = None
            try:
                for addr in addresses:
                    last_addr = addr
                    self.send(str_update_resp, addr)
            except:
                for user in self.transformer.manager.users.values():
                    if user.address == last_addr:
                        self.leave_group(last_addr, {'user_id': user.id})
                        break

    def start_match(self, address, json_data):
        response, group_id = self.transformer.start_match(json_data)
        str_resp = json.dumps(response).encode('utf-8')
        try:
            self.send(str_resp, address)
        except:
            pass

        if response['result']:
            update_response, addresses = self.transformer.get_update_response('start_match', address, group_id)
            str_update_resp = json.dumps(update_response).encode('utf-8')
            last_addr = None
            try:
                for addr in addresses:
                    last_addr = addr
                    self.send(str_update_resp, addr)
            except:
                for user in self.transformer.manager.users.values():
                    if user.address == last_addr:
                        self.leave_group(last_addr, {'user_id': user.id})
                        break

    def end_match(self, address, json_data):
        response, group_id = self.transformer.end_match(json_data)
        str_resp = json.dumps(response).encode('utf-8')
        try:
            self.send(str_resp, address)
        except:
            pass

        if response['result']:
            update_response, addresses = self.transformer.get_update_response('end_match', address, group_id)
            str_update_resp = json.dumps(update_response).encode('utf-8')
            last_addr = None
            try:
                for addr in addresses:
                    last_addr = addr
                    self.send(str_update_resp, addr)
            except:
                for user in self.transformer.manager.users.values():
                    if user.address == last_addr:
                        self.leave_group(last_addr, {'user_id': user.id})
                        break

    def unrecognized(self, address, event):
        resp = self.transformer.unrecognized(event)
        str_resp = json.dumps(resp).encode('utf-8')
        try:
            self.send(str_resp, address)
        except:
            pass

    def json_decode_error(self, address, json_data, error):
        resp = self.transformer.json_decode_error(json_data, error)
        str_resp = json.dumps(resp).encode('utf-8')
        try:
            self.send(str_resp, address)
        except:
            pass


if __name__ == '__main__':
    SocketServer()
