#! /usr/bin/env python3

import math        #import needed modules
import pyaudio     #sudo apt-get install python-pyaudio


def playNote(FREQUENCY, LENGTH):

    PyAudio = pyaudio.PyAudio     #initialize pyaudio

    #See https://en.wikipedia.org/wiki/Bit_rate#Audio
    BITRATE = 44100     #number of frames per second/frameset.

    #FREQUENCY = 1500     #Hz, waves per second, 261.63=C4-note.
    #LENGTH = 1     #seconds to play sound    

    if FREQUENCY > BITRATE:
        BITRATE = FREQUENCY+100

    NUMBEROFFRAMES = int(BITRATE * LENGTH)
    RESTFRAMES = NUMBEROFFRAMES % BITRATE
    WAVEDATA = ''

    #generating wawes
    for x in range(NUMBEROFFRAMES):
     WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))

    for x in range(RESTFRAMES):
     WAVEDATA = WAVEDATA+chr(128)

    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(1),
                    channels = 1,
                    rate = BITRATE,
                    output = True)
    
    stream.write(WAVEDATA)
    stream.stop_stream()
    stream.close()
    p.terminate()

notes = [523, 587, 659, 698, 785, 880, 988, 1047]
for f in notes:
    playNote(f, .25)
