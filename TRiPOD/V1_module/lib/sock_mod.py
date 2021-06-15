from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
from mlsocket import MLSocket
import _thread, pickle
import pyaudio, time
import numpy as np

class socket_mod:

    HOST = "localhost"
    PORT = 12345
    addr = (HOST, PORT)
    server_socket = None

    clients = []
    clients_addr = []

    def set_socket(self, host="localhost", port=12345, freq=2 ):

        # global HOST
        # global PORT
        # global server_socket

        self.HOST = host
        self.PORT = port

        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind(self.addr)
        self.server_socket.listen(freq)



            #
            # if cmd == "":
            #
            #     print("No Task Assigned, Closing socket")
            #     self.server_socket.close()
            #     break
            # elif cmd ==

    # def User_Handler(self, user, address, cmd):
    #
    #     while True:
    #         msg = user.recv(1024).decode()
    #         print("\n",address, "-", msg)
    #         print("\nServer>> ")
    #
    #         if msg == "bye":
    #             break
    #         elif msg == cmd:
    #             _thread.start_new_thread(self.setup_vc, (user, ))
    #
    #     print("\n", "Disconnected from", address, "\nServer>> ", end="")
    #     del self.clients[user]
    #     del self.clients_addr[address]

    def RequestHandler_Listener(self, func_socket, address, cmd, func):

        while True:
            cmd_from_user = func_socket.recv(1024).decode()
            print(cmd_from_user)

            if cmd_from_user == cmd:
                _thread.start_new_thread(func, (func_socket, address))

    def RequestHandler_Send(self, socket, command):

        socket.sendall(command)

    def RequestHandler_Sendall(self, list, command):

        if list == None:
            for i in self.clients:
                i.sendall(command)

        else:
            for i in list:
                i.sendall(command)




    def delay(self, player, data, chunk):
        # time.sleep(1)   #1 sec delay
        player.write(data, chunk)

    def setup_vc(self, user):

        while True:

            global HOST
            RATE    = 96000
            CHUNK   = 32768

            s = MLSocket()
            s.bind((HOST, 1234))
            s.listen()
            conn, adr = s.accept()

            p = pyaudio.PyAudio()
            player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)
            while True:

                audio = conn.recv(32768)
                _thread.start_new_thread(self.delay, (player, audio, CHUNK))
                # print(audio)

            conn.close()

    def start_socket(self, cmd, func=None):


        while True:
            user, address = self.server_socket.accept()
            self.clients.append(user)
            self.clients_addr.append(address)

            print("Connected To ", address)
            print("\nServer>> ", end="")

            # _thread.start_new_thread(func, (user, address))
            _thread.start_new_thread(self.RequestHandler_Listener, (user, address, cmd, func))



    def start_server(self, cmd, func=None):
        _thread.start_new_thread(self.start_socket, (cmd, func))

        print(cmd+" Server Started")
        while True:

            cmd = input("Server >> ")

            for i in self.clients:
                i.send(cmd.encode())


#
# sock = socket_mod()
# sock.set_socket(freq=5)
# sock.start_server(func=sock.User_Handler)
