from gevent.server import DatagramServer


class MultiThreadServer(DatagramServer):
    def handle(self, data, address):
        self.socket.sendto(('Received %s bytes' % len(data)).encode('utf-8'), address)
