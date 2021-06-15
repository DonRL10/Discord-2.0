from mlsocket import MLSocket
import _thread, pickle, pyaudio, numpy as np
from lib.classes import Request, ServerVC, ScreenShare
from lib.dataHandling import DataHandler
# from Handlers.Req_Handler import Server_Handler

VC_ACTIVE = False
SS_ACTIVE = []

def Start_VC():
    vc = ServerVC()
    vc.ConnectVC_Server()

def start_ScreenShare():
    ss = ScreenShare()
    ss.start_ss_server()

def Connect_To_ScreenShare():
    ss = ScreenShare()
    ss.connect_ss()

#Command handler for server
def cmd_handler(user):

    global VC_ACTIVE
    global SS_ACTIVE

    while True:

        packets = user.recv(2046)

        if packets != b'':
            req = pickle.loads(packets)
            print(req.cmd)
            if req.cmd == "vc" and VC_ACTIVE == False:
                _thread.start_new_thread(Start_VC, ())

            elif req.cmd == "ss_start":
                print("ss")
                _thread.start_new_thread(start_ScreenShare, ())
                # SS_ACTIVE.append(req.sender)
            elif req.cmd == "ss_connect":
                _thread.start_new_thread(Connect_To_ScreenShare, ())






server = MLSocket()
server.bind(("localhost", 12345))
server.listen(2)
print("Server Started.")

while True:

    client, addr = server.accept()
    _thread.start_new_thread(cmd_handler, (client,))



"""OLD TESTS"""
# def broadcast(user, data):
#     user.send(data)
#
# def vc_listen(client, player):
#
#     RATE    = 96000
#     CHUNK   = 4096#32768
#     sender = MLSocket()
#     sender.bind(('localhost', 12347))
#     sender.listen(2)
#
#     usersender, addr = sender.accept()
#
#     while True:
#
#         data = client.recv(4096)
#         if data != b'':
#             print(data)
#             usersender.send(data)
#             # thread = threading.Thread(target=broadcast, args=(client, data))
#             # thread.start()


# def vc():
#
#     vc_server = MLSocket()
#     vc_server.bind(("localhost", 12346))
#     vc_server.listen(2)
#
#     RATE    = 96000
#     CHUNK   = 4096#32768
#     p = pyaudio.PyAudio()
#     player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)
#
#     while True:
#         user, addr = vc_server.accept()
#         _thread.start_new_thread(vc_listen, (user, player))
#         # print(user)
#         # data = vc_data_socket.receive_array()
#         # print(data)
#         # vc_client, addr = vc_server.accept()
#
