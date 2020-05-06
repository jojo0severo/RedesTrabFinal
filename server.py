from gevent.server import DatagramServer


class MultiThreadServer(DatagramServer):
    def handle(self, data, address):
        pass