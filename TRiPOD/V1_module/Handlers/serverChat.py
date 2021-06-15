import os, sys, random
from socket import socket, AF_INET, SOCK_STREAM
from texting import TextClass

class ServerChat(TextClass):

    NAME="Unnamed"
    UID="bruh"
    USERS = []

    def __init__(self, name):
        self.NAME = name
        self.UID = random.randint(1000, 9999)

    def Add_User(self, user):
        self.USERS.append(user)


    def BroadCast(self, msg):
        self.RequestHandler_Sendall(self.USERS, msg)

    def Server_Text_Handler(self, user, address):

        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(("localhost", 1235))
        sock.listen(5)
        user, addr = sock.accept()

        while True:
            msg = user.recv(1024).decode()
            self.BroadCast(msg)
            print("\n", msg)
            print("\nServer>> ")

            if msg == "bye":
                break

        print("\n", "Disconnected from", address, "\nServer>> ", end="")
        sock.close()


# serv = ServerChat("Bossmans")
server = TextClass()
server.set_socket(freq=2)
server.start_server("text", func=server.Text_Handler)
sock_mod.start_server("text")
