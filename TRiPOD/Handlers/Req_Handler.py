import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from lib.libs import *

class Handler:

    def Listen(socket, buffer):

        while True:
            data = socket.recv(buffer)



class User_Handler:

    def RecvData(conn):

        while True:

            data = conn.recv()

    # def SendData(self, clients, data):
    #
    #     if data.type == "text":
    #         print("chat")
    #     elif data.type == "svchat":
    #         print("Server Chat")
    #     elif data.type == "vc":
    #         print("voice chat")


class Server_Handler:

    def Broadcast_text(self, user, data):

        user.sendall(data);

    def Broadcast_Servertext(self, users, data):

        for x in users:
            x.sendall(data)

    def Broadcast_VC(self, users, data):

        for x in users:

            # if x == sender:
            #     continue

            x.send(data)
