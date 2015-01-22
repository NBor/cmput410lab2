import sys
import socket
import logging

HOST = 'www.ualberta.ca'
PORT = 80

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
        remote_ip = socket.gethostbyname(HOST)
    except socekt.gaierror:
        logger.warning('host name could not be resolved.')
        sys.exit()

    s.connect((remote_ip, PORT))
    logger.info("Socket connected to %s on ip %s" % (HOST, str(PORT)))

    message = 'GET / HTTP/1.1\r\n\r\n'
    try:
        s.sendall(message.encode("UTF8"))
    except socket.error:
        logger.warning('Send failed!')
        sys.exit()

    reply = s.recv(4096)
    print reply
    s.close()

if __name__ == '__main__':
    main()
