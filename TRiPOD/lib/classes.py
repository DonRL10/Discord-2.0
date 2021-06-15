from mlsocket import MLSocket
from zlib import compress, decompress
from mss import mss
import _thread, pyaudio, pickle, pygame, mysql.connector as mysql,  numpy as np

#Creates a Request object containing command and data
class Request:

    cmd = None
    data = None

    def __init__(self, command, _data):

        self.cmd = command
        self.data = _data

#Broadcaster class for sending data to all adjacent users
class Broadcaster:

    def broadcast_all(self, user_list, data):

        # print(user_list)
        for x in user_list:
            x.send(data)

    def broadcast_except(self, user_list, data, excpns):

        for x in excpns:
            del user_list[x]

        for x in user_list:
            x.send(data)

#Base VC CLass
class VoiceChat:

    CHUNK = 4096
    RATE = 96000

    def delay(self, player, data, chunk):
        # time.sleep(1)   #1 sec delay
        player.write(data, chunk)

#VC child Class for Server
class ServerVC(VoiceChat):

    l_users = []
    s_users = []
    broadcaster = Broadcaster()

    def Listen_Server(self, client, l_client, player):

        list = self.s_users.copy()
        list.remove(l_client)
        while True:
            packets = client.recv(4096)

            if packets != b'':
                # print(packets)
                self.broadcaster.broadcast_all(list, packets)
                # player.write(packets, self.CHUNK)
                # l_client.send(packets)


    def ConnectVC_Server(self):

        p = pyaudio.PyAudio()
        player = p.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, output=True, frames_per_buffer=self.CHUNK)

        vc_conn = MLSocket()
        vc_conn.bind(("localhost", 10001))
        vc_conn.listen(1)
        listener = MLSocket()
        listener.bind(("localhost", 10002))
        listener.listen(1)

        print("Vc Started.")

        while True:
            user, addr = vc_conn.accept()
            s_user, s_add = listener.accept()
            # print(addr, "Connected.")
            self.l_users.append(user)
            self.s_users.append(s_user)
            _thread.start_new_thread(self.Listen_Server, (user, s_user, player))

#VC child class for Client
class ClientVC(VoiceChat):

    def Listen_Client(self, listener, player):

        while True:
            packets = listener.recv(4096)

            if packets != b'':
                print(packets)
                player.write(packets, self.CHUNK)


    def ConnectVC_Client(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        player = p.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, output=True, frames_per_buffer=self.CHUNK)

        conn = MLSocket()
        conn.connect(('localhost', 10001))
        listener = MLSocket()
        listener.connect(('localhost', 10002))
        print("Connected to CHANNEls")

        _thread.start_new_thread(self.Listen_Client, (listener, player))

        while True:

            audio_data=np.fromstring(stream.read(self.CHUNK), dtype=np.int16)
            conn.send(audio_data)
            # print(audio_data)

#Screenshare Class
class ScreenShare:

    broadcaster = Broadcaster()
    ss_users = []
    ssl_users = []
    WIDTH = 1280
    HEIGHT = 720


    def Share(self):

        server = MLSocket()
        server.connect(('localhost', 10003))
        print("SS Connected")
        with mss() as sct:

            rect = {'top': 0, 'left': 0, 'width': self.WIDTH, 'height': self.HEIGHT}
            while True:

                img = sct.grab(rect)
                pixels = compress(img.rgb, 6)
                data = pickle.dumps(pixels)
                server.send(data)

    def SS_Broadcaster(self, user):

        while True:

            packets = user.recv(4096)

            if packets != b'':

                try:
                    self.broadcaster.broadcast_all(self.ssl_users, packets)
                except Exception as e:
                    print("skip'd")
                    print(e)


    def View_Listener(self):

        listener = MLSocket()
        listener.bind(('localhost', 10004))
        listener.listen(1)

        while True:
            l_user, addr = listener.accept()
            self.ssl_users.append(l_user)
            print(l_user)


    def start_ss_server(self):

        server = MLSocket()
        server.bind(('localhost', 10003))
        server.listen(2)

        _thread.start_new_thread(self.View_Listener, ())
        while True:
            user, add = server.accept()
            self.ss_users.append(user)
            _thread.start_new_thread(self.SS_Broadcaster, (user,))

    def connect_ss(self):

        server = MLSocket()
        server.connect(('localhost', 10004))

        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        clock = pygame.time.Clock()
        watching = True

        try:
            while watching:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        watching = False
                        break

                packets = server.recv(4096)
                data = pickle.loads(packets)
                pixels = decompress(data)

                img = pygame.image.fromstring(pixels, (self.WIDTH, self.HEIGHT), 'RGB')

                screen.blit(img, (0, 0))
                pygame.display.flip()
                clock.tick(60)
        except Exception as e:
            print("problem")
            print(e)

            # sock.close()

class Handler:

    def __init__(self):

        self.serv_db = mysql.connect(host='localhost', user="root", password="root123")
        self.cursor = serv_db.cursor()

    def Join_Server(self, server_id, user):
        """
        To add a user to a server. Maintain a Database for all this.
        """
        cursor.execute("INSERT INTO SERVERS WHERE ID")

class Data:

    server_file = None
    friends_file = None

class User:

    def __init__(self):

        self.name = None
        self.email = None
        self.pasd = None
        self.uid = None

    def setDets(self, name, email, psd, id=None):
        self.name = name
        self.email = email
        self.pasd = psd
        self.uid = id

    def setID(self, id):
        self.uid = id

    def toString(self):

        string = "["+str(self.uid)+','+self.name+','+self.email+"]"
        return string

    def fromstring(self, string):

        string = string[1:-1]
        lis = string.split(",")
        # print(lis)
        self.uid = lis[0]
        self.name = lis[1]
        self.email = lis[2]
