from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from zlib import compress

from mss import mss


WIDTH = 1280
HEIGHT = 720

def handle_clients(conn):
    with mss() as sct:

        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

        while True:

            img = sct.grab(rect)

            pixels = compress(img.rgb, 6)


            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))

            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)
            conn.sendall(pixels)

def main(host, port):
    sock = socket()
    sock.bind((host, port))
    try:
        sock.listen(5)
        print('Server started.')

        while True:
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            thread = Thread(target=handle_clients, args=(conn,)).start()
    finally:
        sock.close()


main('localhost', 5000)
