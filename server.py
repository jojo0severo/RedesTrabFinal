from gevent.server import DatagramServer


class MultiThreadServer(DatagramServer):
    def handle(self, data, address):
        self.socket.sendto(('Received %s bytes' % len(data)).encode('utf-8'), address)


if __name__ == '__main__':
    print('Receiving datagrams on 127.0.0.1:8080')
    MultiThreadServer('127.0.0.1:8080').serve_forever()
