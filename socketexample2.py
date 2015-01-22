import sys
import socket
import logging

HOST = ''
PORT = 8888

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        logger.warning('Failed to create socket!')
        logger.warning("Error code: %s\nMessage: %s" % (str(e[0]), str(e[1])))
        sys.exit()

    logger.info('Socket created successfully.')

    try:
        s.bind((HOST, PORT))
    except socket.error as e:
        logger.warning("Error code: %s\nMessage: %s" % (str(e[0]), str(e[1])))

    logging.info('Socket bind complete.')
    s.listen(10)
    logging.info('Socket is now listening.')
    conn, addr = s.accept()
    logging.info('Socket is connected with %s:%s' % (str(addr[0]), str(addr[1])))

    data = conn.recv(1024)
    reply = str(data)
    print reply
    conn.sendall(reply.encode('UTF8'))
    s.close()


if __name__ == '__main__':
    main()
