import time
from socket import AF_INET, socket, SOCK_DGRAM


class Client:
    def __init__(self, host='127.0.0.1', port=8080, buffer_size=4096):
        self.responses = []
        self.keep_listening = True
        self.buffer_size = buffer_size
        self.server_address = (host, port)
        self.client_socket = socket(AF_INET, SOCK_DGRAM)

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
        self.client_socket.sendto('Ok'.encode('utf-8'), self.server_address)
        now = time.time()
        while time.time() - now < 5:
            msg = self.client_socket.recv(self.buffer_size).decode('utf-8')
            if msg == 'ok':
                return
            else:
                break

        self.check_ok()
