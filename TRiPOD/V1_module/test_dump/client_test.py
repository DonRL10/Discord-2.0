from socket import socket, AF_INET, SOCK_STREAM
from mlsocket import MLSocket

import _thread, pickle, pyaudio, time, os, sys, tqdm
import numpy as np

HOST = "localhost"
PORT = 12345
addr = (HOST, PORT)

user_sock = socket(AF_INET, SOCK_STREAM)
user_sock.connect(addr)
print("Connected")

def server_Handler(sock):
    while True:
        msg = sock.recv(1024)
        print("\nServer -", msg.decode(), "\nUser>> ", end="")

def setup_vc(sock):

    while True:

        RATE    = 96000
        CHUNK   = 32768
        s = MLSocket()
        s.connect((HOST, 1234))
        print("VC CONNECTED.")

        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

        while True:
            audio_data=np.fromstring(stream.read(CHUNK), dtype=np.int16)
            s.send(audio_data)


def sendfile(serv, filename):

    filesize = os.path.getsize(filename)
    sep = "<SEPARATOR>"
    serv.send(f"{filename}{sep}{filesize}".encode())
    print("Metadata sent.")
    prog = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    if(serv.recv(24).decode() == ACK):
        time.sleep(1)
        print("sending file.")

        with open(filename, "rb") as f:
            for _ in prog:
                bytes_read = f.read(BUFFER_SIZE)

                if not bytes_read:
                    print(f"\n{file_name} Transfer Complete.\n")
                    break

                serv.sendall(bytes_read)
                prog.update(len(bytes_read))


_thread.start_new_thread(server_Handler, (user_sock,))
while True:

    cmd = input("User>> ")
    user_sock.sendall(cmd.encode())

    if cmd=="bye":
        break
    elif cmd=="vc":
        # _thread.start_new_thread(setup_vc, (user_sock,))
        setup_vc(user_sock)
