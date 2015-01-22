"""Simple Socket server."""
import sys
import socket
import thread
import logging


def handler(conn, addr):
    """Function to run in thread."""
    while True:
        data = conn.recv(1024)
        reply = str(data).strip('\r\n') + ' Neil Borle\r\n'
        print 'From %s got: %s' % (addr, data)
        conn.sendall(reply.encode('UTF8'))
        if data == '\x1b\r\n':
            conn.close()
            break


class SocketServer(object):

    """A Socket server."""
    logger = logging.getLogger()

    def __init__(self, host, port):
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())
        self.host = host
        self.port = port

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.logger.info('Socket created successfully.')
        except socket.error as e:
            self.logger.warning('Failed to create socket!')
            self.logger.warning("Error code: %s\nMessage: %s" % (str(e[0]), str(e[1])))
            sys.exit()

    def bind(self):
        """Bind to host and port"""
        try:
            self.sock.bind((self.host, self.port))
        except socket.error as e:
            self.logger.warning("Error code: %s\nMessage: %s" % (str(e[0]), str(e[1])))
        self.logger.info('Socket bind complete.')

        self.sock.listen(10)
        self.logger.info('Socket is now listening.')

    def serve(self):
        """Handle Connections."""
        while True:
            conn, addr = self.sock.accept()
            self.logger.info('Socket is connected with %s:%s' % (str(addr[0]), str(addr[1])))
            thread.start_new_thread(handler, (conn, addr))
        self.sock.close()


def main():
    """Run server."""
    server = SocketServer('', 8888)
    server.bind()
    server.serve()

if __name__ == '__main__':
    main()
