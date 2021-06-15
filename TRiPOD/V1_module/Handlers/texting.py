import os, sys
from socket import socket, AF_INET, SOCK_STREAM

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from lib.sock_mod import socket_mod

class TextClass(socket_mod):

    def Text_Handler(self, user, address):

        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(("localhost", 1235))
        sock.listen(5)
        user, addr = sock.accept()

        while True:
            msg = user.recv(1024).decode()
            print("\n", msg)
            print("\nServer>> ")

            if msg == "bye":
                break
            # elif msg == vc:
            #     _thread.start_new_thread(self.setup_vc, (user, ))

        print("\n", "Disconnected from", address, "\nServer>> ", end="")
        sock.close()

    # def VoiceChat_Handler(self, user):




# server = TextClass()
# server.set_socket(freq=2)
# server.start_server("text", func=server.Text_Handler)
# sock_mod.start_server("text")
