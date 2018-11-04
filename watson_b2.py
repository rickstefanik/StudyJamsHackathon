#! /usr/bin/env python3

import wave
import numpy as np
import pyaudio
from watson_developer_cloud import TextToSpeechV1

'''
def getWavFrequency(fileName):
    chunk = 2048

    # open up a wave
    wf = wave.open(fileName, 'rb')
    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    # use a Blackman window
    window = np.blackman(chunk)
    # open stream
    p = pyaudio.PyAudio()
    stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                output = True)

    # read some data
    data = wf.readframes(chunk)
    # play stream and find the frequency of each chunk
    while len(data) == chunk*swidth:
        # write data out to the audio stream
        stream.write(data)
        # unpack the data and times by the hamming window
        indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth), data))*window
        # Take the fft and square each value
        fftData=abs(np.fft.rfft(indata))**2
        # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        if which != len(fftData)-1:
            y0,y1,y2 = np.log(fftData[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which+x1)*RATE/chunk
            print("The freq is %f Hz." % (thefreq))
        else:
            thefreq = which*RATE/chunk
            print("The freq is %f Hz." % (thefreq))
        # read some more data
        data = wf.readframes(chunk)
    if data:
        stream.write(data)
    stream.close()
    p.terminate()'''


def shiftPitch(newFile, shift):
    wr = wave.open('temp.wav', 'r')
    # Set the parameters for the output file.
    par = list(wr.getparams())
    par[3] = 0  # The number of samples will be set by writeframes.
    par = tuple(par)
    ww = wave.open(newFile, 'w')
    ww.setparams(par)
    fr = 20
    sz = wr.getframerate()//fr  # Read and process 1/fr second at a time.
    # A larger number for fr means less reverb.
    c = int(wr.getnframes()/sz)  # count of the whole file
    #shift = 500//fr  # shifting 100 Hz
    for num in range(c):
        try:
            da = np.fromstring(wr.readframes(sz), dtype=np.int16)
            left, right = da[0::2], da[1::2]  # left and right channel
            #print(len(left), len(right))
            lf, rf = np.fft.rfft(left), np.fft.rfft(right)
            lf, rf = np.roll(lf, shift), np.roll(rf, shift)
            lf[0:shift], rf[0:shift] = 0, 0
            nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
            ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
            ww.writeframes(ns.tostring())
        except:
            break
    ww.close()
    wr.close()


text_to_speech = TextToSpeechV1(
    iam_apikey='nBVvz1-p4Q3F0rF_L8c0UmCfirPNfIKaVO32prppKCzR',
    url='https://stream.watsonplatform.net/text-to-speech/api'
)

def sayWord(word):
    with open('temp.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                word,
                'audio/wav',
                'en-US_AllisonVoice'
            ).get_result().content)



sayWord('<voice-transformation type="Custom" pitch="-100%" pitch_range="-100%" rate="-100%" glottal_tension="-80%" timbre="Sunrise"> And you can combine all this with modifications of my speech rate and my tone. </voice-transformation>')
shiftPitch("pitch0.wav", 0)
sayWord('<voice-transformation type="Custom" pitch="100%" pitch_range="-100%" rate="-100%" glottal_tension="-80%" timbre="Sunrise"> And you can combine all this with modifications of my speech rate and my tone. </voice-transformation>')
shiftPitch("pitch1.wav", 0)
'''sayWord("My")
shiftPitch("pitch1.wav", 10)
sayWord("Name")
shiftPitch("pitch2.wav", 25)
sayWord("Is")
shiftPitch("pitch3.wav", 20)
sayWord("Rick")
shiftPitch("pitch4.wav", 0)'''


infiles = ["pitch0.wav", "pitch1.wav"]

'''infiles = ["pitch0.wav", 
            "pitch1.wav",
            "pitch2.wav",
            "pitch3.wav",
            "pitch4.wav"]'''
outfile = "sounds.wav"

data= []
for infile in infiles:
    w = wave.open(infile, 'rb')
    data.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()

output = wave.open(outfile, 'wb')
output.setparams(data[0][0])
for i in range(len(infiles)):
    output.writeframes(data[i][1])
    #output.writeframes(data[1][1])
    #output.writeframes(data[2][1])
    #output.writeframes(data[3][1])
    #output.writeframes(data[4][1])
output.close()
