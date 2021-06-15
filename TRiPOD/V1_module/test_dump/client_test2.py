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
        # if

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

def setup_text(sock):

    text_sock = socket(AF_INET, SOCK_STREAM)
    text_sock.connect(("localhost", 1235))

    while True:
        print("\nChat mode On.\n")
        uname = "bossman"
        cmd = input(uname+">> ")
        msg = uname+">> "+cmd

        text_sock.sendall(msg.encode())


_thread.start_new_thread(server_Handler, (user_sock,))
while True:

    cmd = input("User>> ")
    user_sock.send(cmd.encode())

    if cmd=="bye":
        break
    elif cmd=="vc":
        _thread.start_new_thread(setup_vc, (user_sock,))
    elif cmd=="text":
        # _thread.start_new_thread(setup_text, (user_sock,))
        setup_text(user_sock)
