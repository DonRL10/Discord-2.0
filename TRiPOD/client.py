from lib.classes import Request, ClientVC, ScreenShare
from mlsocket import MLSocket
import pickle, pyaudio, _thread, numpy as np


sock = MLSocket()
sock.connect(("localhost", 12345))
print("Connected")

# req = Request("ss_start", "")
req = Request("vc", "")
data = pickle.dumps(req)
sock.send(data)
vc = ClientVC()
vc.ConnectVC_Client()
# ss = ScreenShare()
# _thread.start_new_thread(ss.Share, ())
# ss.connect_ss()




"""OLD TESTS"""
# Vc()
#
# def delay(player, data, chunk):
#     # time.sleep(1)   #1 sec delay
#     player.write(data, chunk)
#
# def vc_listen(listen, player):
#
#     RATE    = 96000
#     CHUNK   = 4096#32768
#
#     while True:
#
#             packets = listen.recv(4096)
#             if packets != b'':
#                 # print(type(packets))
#                 # print(packets)
#                 player.write(packets, CHUNK)
#
# def Vc():
#
#     conn = MLSocket()
#     conn.connect(("localhost", 12346))
#
#     listener = MLSocket()
#     listener.connect(('localhost', 12347))
#
#
#     RATE    = 96000
#     CHUNK   = 4096
#     print("VC CONNECTED.")
#
#     p = pyaudio.PyAudio()
#     stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
#     player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)
#
#     _thread.start_new_thread(vc_listen, (conn, listener, player))
#     while True:
#         audio_data=np.fromstring(stream.read(CHUNK), dtype=np.int16)
#         conn.send(audio_data)
#         # print(audio_data)
#
