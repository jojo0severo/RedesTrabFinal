from threading import Thread
from socket import AF_INET, socket, SOCK_DGRAM


class ClientSender:
    def __init__(self, host, port, buffer_size):
        self.buffer_size = buffer_size
        self.server_address = (host, port)
        self.client_socket = socket(AF_INET, SOCK_DGRAM)

    def send(self, message):
        self.client_socket.sendto(message, self.server_address)
        msg = self.client_socket.recv(self.buffer_size).decode('utf-8')
        if msg:
            self.check_ok()
            return msg

        self.send(message)

    def check_ok(self):
        self.client_socket.sendto('ok'.encode('utf-8'), self.server_address)
        msg = self.client_socket.recv(self.buffer_size).decode('utf-8')
        if msg.lower() == 'ok':
            self.client_socket.sendto('ok'.encode('utf-8'), self.server_address)
            return

        self.check_ok()


class ClientReceiver:
    def __init__(self, manager, lock, host, port, buffer_size):
        self.keep_listening = True
        self.manager = manager
        self.lock = lock
        self.buffer_size = buffer_size
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.client_socket.bind((host, port))

        Thread(target=self.listen).start()

    def listen(self):
        while self.keep_listening:
            msg = self.client_socket.recv(self.buffer_size)

            self.lock.acquire()
            self.manager.handle_update(msg)
            self.lock.release()
