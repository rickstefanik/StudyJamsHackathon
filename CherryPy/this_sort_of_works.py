#! /usr/bin/env python3

import os
import wave
import numpy as np
import pyaudio
from watson_developer_cloud import TextToSpeechV1
from cherrypy.lib import static
import json
import re
import cherrypy
import random
#from tools import encode


class MelodyController:
    def shiftPitch(self, newFile, shift):
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


    def __init__(self):
        self.text_to_speech = TextToSpeechV1(
            iam_apikey='nBVvz1-p4Q3F0rF_L8c0UmCfirPNfIKaVO32prppKCzR',
            url='https://stream.watsonplatform.net/text-to-speech/api'
        )
        self.localDir = os.path.dirname(__file__)
        self.absDir = os.path.join(os.getcwd(), self.localDir)
        self.pitchLookup = {
                            "F": -100,
                            "F#": -80,
                            "G": -60,
                            "G#": -39,
                            "A": -19,
                            "A#": 3,
                            "B": 23,
                            "C": 44,
                            "C#": 66,
                            "D": 90
        }
        self.fileNum = 1

    def sayWord(self, word):
        with open('temp.wav', 'wb') as audio_file:
            audio_file.write(
                self.text_to_speech.synthesize(
                    word,
                    'audio/wav',
                    'en-US_AllisonVoice'
                    #'en-US_LisaVoice'
                ).get_result().content)

    def generateCloseTag(self):
        return "</voice-transformation>"

    def generateStartTag(self, pitch):
        pitch = str(pitch)
        #timber = str(random.randint(-100,101))
        #return "".join(['<voice-transformation timbre="Sunrise" timbre_extent="', timber ,'%" breathiness="0%" type="Custom" pitch="', pitch ,'%" pitch_range="-100%" rate="-100%" glottal_tension="-100%" timbre="Sunrise">'])
        return "".join(['<voice-transformation timbre="Sunrise" timbre_extent="100%" breathiness="0%" type="Custom" pitch="', pitch ,'%" pitch_range="-100%" rate="-100%" glottal_tension="-100%" timbre="Sunrise">'])

    def generateTag(self, words, pitch):
        return "".join([self.generateStartTag(pitch), words, self.generateCloseTag()])


    def watsonSpeak(self, textFromUser, pitch, filename="output.wav"):
        #if filename == "output":
        #    filename += str(self.fileNum) + ".wav"

        print("In Watson Speak")
        words = textFromUser.split(" ")
        sayThis = ""
        #melody = ["F", "F", "D", "C", "A", "C"]
        #melody = ["F", "A", "F", "A", "A#", "F", "C", "C", "F"]
        
        melody = ["F", "F", "C", "C", "D", "D", "C", "C", "A#", "A#", "A", "A", "G", "G", "F"]
        #melody = ["A", "G", "F", "G", "A", "A", "A", "G", "G", "G", "C", "C", "C", "A", "G", "F", "G", "A", "A", "A", "G", "F", "G" ,"A", "G", "F"]
        
        
        #keyExample = ""
        i = 0
        for word in words:
            #print("before cat")
            sayThis += self.generateTag(word, self.pitchLookup[melody[i]])
            #print("after cat")
            #print(sayThis)
            i += 1
            i %= len(melody)
        self.sayWord(sayThis)
        self.shiftPitch(filename, 0)


    def bytes_from_file(self, filename, chunksize=8192):
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(chunksize)
                if chunk:
                    for b in chunk:
                        yield b
                else:
                    break
    def GET(self):
        #name = "output" + str(self.fileNum) + ".wav"
        name = "output.wav"
        path = os.path.join(self.absDir, name)
        #print("I;m about to finish get")
        #print("PATH: " + path)
        #return json.dumps({"result" : "success"})
        #f = static.serve_file(path, "audio/wav", "attachment", path)
        return static.serve_file(path, "audio/wav", "attachment", path)
        #return json.dumps({"result": "success", "file": encode(f)})

    def GET_KEY(self, key):
        try:
            #print("I'm about to get the request")
            #payload = cherrypy.request.body.read()
            #print(cherrypy.request.body)
            #print("PAYLOAD: " + str(payload))
            #payload = json.loads(payload)
            #print("PAYLOAD: " + str(payload))
            self.watsonSpeak(key, 50)
        except:
            return json.dumps({"result": "error"})
        #path = os.path.join(self.absDir, "output.wav")
        #return static.serve_file(path, "audio/wav", "attachment", path)
        fileString = ""
        for b in self.bytes_from_file("output.wav"):
            fileString += str(b)

        print(fileString)
        return json.dumps({"result": "success", "file": fileString})


        
    
    def POST(self):
        #return json.dumps({"result": "success"})
        
        try:
            print("I'm about to get the request")
            payload = cherrypy.request.body.read()
            print(cherrypy.request.body)
            print("PAYLOAD: " + str(payload))
            payload = json.loads(payload)
            print("PAYLOAD: " + str(payload))
            self.watsonSpeak(payload['text'], 50)
            #self.fileNum += 1
        except:
            return json.dumps({"result": "error"})
        #'{"text":"This is what I want to send"}'
        #name = "output" + str(self.fileNum) + ".wav"
        path = os.path.join(self.absDir, "output.wav")
        return static.serve_file(path, "audio/wav", "attachment", path)


