
##INCOMPLETE!!!

import tkinter
import tkinter as tk
import tkinter.messagebox
import pyaudio
import wave
import os
from sys import byteorder
from array import array
from struct import pack

sample_format = pyaudio.paInt16 #16 bit/sample
noofchannels = 2
samplespersecond = 48000
sampleChunk = 1024 
seconds = 5
soundDataFilename = "rawSound.wav"
c=0
THRESHOLD = 500

class interfaceSound:

    def __init__(self, chunk=sampleChunk, frmat=sample_format, channels=noofchannels, rate=samplespersecond, py=pyaudio.PyAudio(),new=c, sdf=soundDataFilename):
        self.main = tkinter.Tk()
        self.collections = []
        self.main.geometry('500x300')
        self.main.title('interfaceSound')
        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.newname=new
        self.frames = []
        self.st = 1
        self.fn=sdf
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        self.buttons = tkinter.Frame(self.main, padx=120, pady=120)
 
        self.buttons.pack(fill=tk.BOTH)

        self.strt_rec = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Start Recording', command=lambda: self.start_record())
        self.strt_rec.grid(row=0, column=0, padx=80, pady=5)
        self.stop_rec = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Stop Recording', command=lambda: self.stop())
        self.stop_rec.grid(row=1, column=0, columnspan=1, padx=80, pady=5)

        tkinter.mainloop()

    def is_silent(snd_data):
       return max(snd_data) < THRESHOLD

    def normalize(snd_data):
       MAXIMUM = 16384  #increasing this might increase noise
       times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    def trim1(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r


    snd_data = trim1(snd_data) 
    snd_data.reverse()
    snd_data = trim1(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    r = array('h', [0 for i in range(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*RATE))])
    return r

def record():

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=2, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')

    while 1:
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > 200:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r
    def start_record(self):
        self.st = 1
        self.frames = []
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        while self.st == 1:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            print("..recording..")
            self.main.update()


        stream.close()

        wf = wave.open(self.fn, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def stop(self):
        self.st = 0
        self.newname += 1
        self.fn="rawSound"+str(self.newname)+".wav"

guiAUD = interfaceSound()