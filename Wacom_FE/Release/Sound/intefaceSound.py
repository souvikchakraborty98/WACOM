import tkinter
import tkinter as tk
import tkinter.messagebox
import pyaudio
import wave
import os

sample_format = pyaudio.paInt16 #16 bit/sample
noofchannels = 2
samplespersecond = 48000
sampleChunk = 1024 
seconds = 5
soundDataFilename = "rawSound.wav"
c=0

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