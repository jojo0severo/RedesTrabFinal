from threading import Thread
from socket import AF_INET, socket, SOCK_DGRAM, timeout


class ClientSender:
    def __init__(self, host, port, server_host, server_port, buffer_size):
        self.buffer_size = buffer_size
        self.server_address = (server_host, server_port)
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.client_socket.bind((host, port))
        self.client_socket.settimeout(5)

    def send(self, message):
        try:
            self.client_socket.sendto(message, self.server_address)
            msg = self.client_socket.recv(self.buffer_size).decode('utf-8')
            if msg:
                self.check_ok()
                return msg

        except timeout:
            pass

        self.send(message)

    def check_ok(self):
        self.client_socket.sendto('ok'.encode('utf-8'), self.server_address)

        try:
            msg = self.client_socket.recv(self.buffer_size).decode('utf-8')
        except timeout:
            return

        if msg.lower() == 'ok':
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
        self.client_socket.settimeout(5)

        Thread(target=self.listen).start()

    def listen(self):
        while self.keep_listening:
            try:
                msg, address = self.client_socket.recvfrom(self.buffer_size)

                self.lock.acquire()

                self.manager.handle_update(msg)
                self.check_ok(address)

                self.lock.release()

            except timeout:
                pass

    def check_ok(self, address):
        self.client_socket.sendto('ok'.encode('utf-8'), address)

        try:
            msg, addr = self.client_socket.recvfrom(4096)
        except timeout:
            return

        msg = msg.decode('utf-8')
        if addr == address and msg.lower() == 'ok':
            return

        self.check_ok(address)
