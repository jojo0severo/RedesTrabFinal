import time, json
from socket import AF_INET, socket, SOCK_DGRAM


class ClientSender:
    def __init__(self, host='127.0.0.1', port=8080, buffer_size=4096):
        self.buffer_size = buffer_size
        self.server_address = (host, port)
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.subjects = list()
        self.groups = list()

    def send(self, message):
        self.client_socket.sendto(message, self.server_address)
        now = time.time()
        while time.time() - now < 3:
            msg = self.client_socket.recv(self.buffer_size).decode('utf-8')
            if msg:
                self.check_ok()
                return msg

        self.send(message)

    def check_ok(self):
        self.client_socket.sendto('{"event": "ok", "json": {}}'.encode('utf-8'), self.server_address)
        now = time.time()
        while time.time() - now < 5:
            msg = json.loads(self.client_socket.recv(self.buffer_size).decode('utf-8'))
            print(msg)
            if msg["result"] and msg["message"] == 'Ok':
                return
            else:
                break
            
            time.sleep(1)

        self.check_ok()


class ClientReceiver:
    def __init__(self, host='127.0.0.1', port=9000, buffer_size=4096):
        self.keep_listening = True
        self.client_socket = socket()
        pass
