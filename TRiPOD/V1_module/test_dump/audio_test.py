import pyaudio, time
import numpy as np
import _thread

RATE    = 96000
CHUNK   = 4096

def delay(player, data, chunk):
    # time.sleep(1)   #1 sec delay
    player.write(data, chunk)

p = pyaudio.PyAudio()

player = p.open(format=pyaudio.paInt32, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)

stream = p.open(format=pyaudio.paInt32, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

# for i in range(int(20*RATE/CHUNK)): #do this for 10 seconds
while True:
    audio_data=np.fromstring(stream.read(CHUNK), dtype=np.int32)
    print(np.shape(audio_data))
    # print(np.array2string(audio_data)+",")
    # time.sleep(2)
    _thread.start_new_thread(delay, (player, audio_data, CHUNK))

# stream.stop_stream()
# stream.close()
# p.terminate()
