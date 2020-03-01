print("Loading libraries. Please wait..", end=' ')
import parselmouth
import numpy as np
import seaborn as sep
import pyaudio
import wave
import matplotlib.pyplot as plt
import mplcursors
import datetime
import os

from sys import byteorder
from array import array
from struct import pack
import statistics
import time
import msvcrt
from msvcrt import getch


THRESHOLD = 2500
CHUNK_SIZE = 1024
CHANNELS=1
FORMAT = pyaudio.paInt16 # 16 bit res
RATE = 48000


def countdown(t):
    aborted=False
    while t>-1 and aborted==False:
        mins, secs = divmod(t, 60)
        timefmt = '{:02d}:{:02d}'.format(mins, secs)
        print(timefmt+" secs. Press 'esc' to exit and show only data plots. Press 'Enter' to open now.", end='\r')
        time.sleep(1)
        if msvcrt.kbhit():
            keypress=msvcrt.getch()
            if keypress == chr(27).encode():
              aborted=True
              return True
            elif keypress == chr(13).encode():
              aborted=True
              return False
        t -= 1

p = pyaudio.PyAudio()

print("Done.\n")

path = os.path.dirname(os.path.abspath(__file__))+"\\output\\"

if not os.path.exists(path):
    os.makedirs(path)

badOp=True
while badOp==True:
       try:
          op=int(input("Type of recording?\nPress 1 for CG and 2 for PD.\n"))
       except:
           print("Bad Option\n")
           continue
       if op==1: 
          #path to output/CG/foldername
          foldernameCG=input("Enter folder name..\"PD\" is reserved!\n")
          if foldernameCG.lower()=="pd":
              print("Unauthorised")
              getch()
              exit()
          path=path+"CG\\"+foldernameCG+"\\"
          xb=input("Save as?\n")
          if not os.path.exists(path):
             os.makedirs(path)
          badOp=False
       elif op==2:
          foldername=input("Enter folder name..\"CG\" is reserved!\n")
          if foldername.lower()=="cg":
              print("Unauthorised")
              getch()
              exit()
          path=path+"PD\\"+foldername+"\\"
          xb=input("Save as?\n")
          if not os.path.exists(path):
             os.makedirs(path)
          #path to output/foldername/
          badOp=False
       else:
           print("Bad Option\n")

fcurmil="autoCapture"+"_name_"+str(datetime.datetime.now().strftime("%f"))+xb
fn=fcurmil+".wav"

mfccfn="MFCC_features_for_"+fcurmil+".DATA"
mfccdata=os.path.join(path, mfccfn)

formantfn="Formant_features_for_"+fcurmil+".DATA"
formantmatrixSave=os.path.join(path,formantfn)

if not os.path.exists(path):
    os.makedirs(path)




c=1
for i in range(p.get_device_count()):
  if p.get_device_info_by_index(i).get('maxInputChannels')>0 and '@' not in p.get_device_info_by_index(i).get('name') and int(p.get_device_info_by_index(i).get('hostApi'))==0 and p.get_device_info_by_index(i).get('name')!="Microsoft Sound Mapper - Input":
    print(str(c)+") "+str(p.get_device_info_by_index(i)))
    c+=1
    print("\n\n")


try:
     INPUT_DEVICE_IN=int(input("Input Device Index?\n"))
except:
     print("Invalid Index...Press any key to exit.\n")
     getch()
     exit



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


    snd_data = trim1(snd_data) #samne
    snd_data.reverse()
    snd_data = trim1(snd_data) #piche
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    r = array('h', [0 for i in range(int(seconds*RATE))]) #samne
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*RATE))]) #piche
    return r

def record():
    try:
       stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE, input_device_index=INPUT_DEVICE_IN)
    except Exception as e:
       print(str(e)+"\nPress any key to exit")
       getch()
       exit()
    
    num_silent = 0
    snd_started = False

    r = array('h')

    while 1:
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)
        print(max(snd_data))
        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > 350: #increase this to increase timeout
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r

def record_to_file(path):
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

if __name__ == '__main__':
    print("Listening..")    
    record_to_file(os.path.join(path, fn))
    print("Done...Written to "+fn+"\n")


sep.set()
snd = parselmouth.Sound((os.path.join(path, fn)))
pointProcess = parselmouth.praat.call(snd, "To PointProcess (periodic, cc)", 75, 600)

def draw_spectrogram(spectrogram, dynamic_range=70):
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='afmhot')
    plt.ylim([spectrogram.ymin, spectrogram.ymax])
    plt.xlabel("time [s]")
    plt.ylabel("frequency [Hz]")

def draw_pitch(pitch):
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
    plt.grid(False)
    plt.ylim(0, pitch.ceiling)
    plt.ylabel("F0 [Hz]")

def getJitter(pointProcess):
   localJitter = parselmouth.praat.call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
   localabsoluteJitter = parselmouth.praat.call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
   rapJitter = parselmouth.praat.call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
   ppq5Jitter = parselmouth.praat.call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
   ddpJitter = parselmouth.praat.call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)

   return localJitter,localabsoluteJitter,rapJitter,ppq5Jitter,ddpJitter

def getShimmer(pointProcess):
   localShimmer =  parselmouth.praat.call([snd, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
   localdbShimmer = parselmouth.praat.call([snd, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
   apq3Shimmer = parselmouth.praat.call([snd, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
   aqpq5Shimmer = parselmouth.praat.call([snd, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
   apq11Shimmer =  parselmouth.praat.call([snd, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
   ddaShimmer = parselmouth.praat.call([snd, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

   return localShimmer,localdbShimmer,apq3Shimmer,aqpq5Shimmer,apq11Shimmer,ddaShimmer

def getHarmonicFeatures(sound):
    harmonicitycc=parselmouth.praat.call(snd,"To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    harmonicityac=parselmouth.praat.call(snd,"To Harmonicity (ac)",0.01, 75, 0.1, 4.5)

    return harmonicitycc,harmonicityac

def measureGlottalFeaturesUsingFormants(sound,pointProcess):
    formants = parselmouth.praat.call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
    numPoints = parselmouth.praat.call(pointProcess, "Get number of points")

    f1_list = []
    f2_list = []
    f3_list = []
    f4_list = []
    
     # at glottal pulses
    for point in range(0, numPoints):
        point += 1
        t = parselmouth.praat.call(pointProcess, "Get time from index", point)
        f1 = parselmouth.praat.call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = parselmouth.praat.call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        f3 = parselmouth.praat.call(formants, "Get value at time", 3, t, 'Hertz', 'Linear')
        f4 = parselmouth.praat.call(formants, "Get value at time", 4, t, 'Hertz', 'Linear')
        f1_list.append(f1)
        f2_list.append(f2)
        f3_list.append(f3)
        f4_list.append(f4)
    
    f1_list = [f1 for f1 in f1_list if str(f1) != 'nan']
    f2_list = [f2 for f2 in f2_list if str(f2) != 'nan']
    f3_list = [f3 for f3 in f3_list if str(f3) != 'nan']
    f4_list = [f4 for f4 in f4_list if str(f4) != 'nan']

    return f1_list,f2_list,f3_list,f4_list

def getFormants(sound):
    formants = parselmouth.praat.call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
    formantsmatrix=parselmouth.praat.call(formants,"To Matrix",1)
    formantsQB=parselmouth.praat.call(formants,"Get quantile of bandwidth",1, 0, 0, "Hertz", 0.5)	
    formantsmean=parselmouth.praat.call(formants,"Get mean",1, 0, 0, "Hertz")	
    formantsSD=parselmouth.praat.call(formants,"Get standard deviation", 1, 0, 0, "Hertz")
    parselmouth.praat.call(parselmouth.praat.call(formants,"To Matrix",1),"Save as text file",formantmatrixSave)

    return formants,formantsmatrix,formantsQB,formantsmean,formantsSD


def getHnr(snd):
    harmonicity = parselmouth.praat.call(snd, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = parselmouth.praat.call(harmonicity, "Get mean", 0, 0)

    return hnr

def getMFCC(sound):
    mfcc=parselmouth.praat.call(sound,"To MFCC",12, 0.015, 0.005, 100, 100, 0)
    parselmouth.praat.call(parselmouth.praat.call(mfcc,"To TableOfReal",'no'),"Save as text file",mfccdata)

    return mfcc
pitch = snd.to_pitch()
pre_emphasized_snd = snd.copy()
pre_emphasized_snd.pre_emphasize()
spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)

(localJitter,localabsoluteJitter,rapJitter,ppq5Jitter,ddpJitter)=getJitter(pointProcess)
(localShimmer,localdbShimmer,apq3Shimmer,aqpq5Shimmer,apq11Shimmer,ddaShimmer)=getShimmer(pointProcess)

Hnr=getHnr(snd)

(harmonicitycc,harmonicityac)=getHarmonicFeatures(snd)
(f1,f2,f3,f4)=measureGlottalFeaturesUsingFormants(snd,pointProcess)
f1_mean = statistics.mean(f1)
f2_mean = statistics.mean(f2)
f3_mean = statistics.mean(f3)
f4_mean = statistics.mean(f4)

(formants,formantsmatrix,formantsQB,formantsmean,formantsSD)=getFormants(snd)

mfcc=getMFCC(snd)

sfn="soundData"+"_for_"+fcurmil+".log"
ops=os.path.join(path, sfn)
with open(ops, 'w') as f:
    f.write('-----------------------------------------------------------------------------------------\n')
    print('Pitch:', pitch, file=f)
    f.write('-----------------------------------------------------------------------------------------\n')
    f.write('Jitter:\n\n')
    f.write("localJitter: "+str(localJitter)+"\nlocalabsoluteJitter: "+str(localabsoluteJitter)+"\nrapJitter: "+str(rapJitter)+"\nppq5Jitter: "+str(ppq5Jitter)+"\nddpJitter: "+str(ddpJitter)+"\n")
    f.write("-----------------------------------------------------------------------------------------\n")
    f.write("Shimmer:\n\n")
    f.write("localShimmer: "+str(localShimmer)+"\nlocaldbShimmer: "+str(localdbShimmer)+"\napq3Shimmer: "+str(apq3Shimmer)+"\naqpq5Shimmer: "+str(aqpq5Shimmer)+"\napq11Shimmer: "+str(apq11Shimmer) +"\nddaShimmer: "+str(ddaShimmer)+"\n")
    f.write("-----------------------------------------------------------------------------------------\n")
    print('Harmonicity (auto-correlation): ', harmonicityac, file=f)
    f.write("-----------------------------------------------------------------------------------------\n")
    print('Harmonicity (cross-correlation): ', harmonicitycc, file=f)
    f.write("-----------------------------------------------------------------------------------------\n")
    f.write("HNR: "+str(Hnr)+"\n")
    f.write("-----------------------------------------------------------------------------------------\n")
    f.write("Glottal features and glottal based spectral features [formants]:\n ")
    f.write("F1 : \n---------\n"+str(f1))
    f.write("\n\n")
    f.write("F2 : \n---------\n"+str(f2))
    f.write("\n\n")
    f.write("F3 : \n---------\n"+str(f3))
    f.write("\n\n")
    f.write("F4 : \n---------\n"+str(f4))
    f.write("\n\n")
    f.write("Mean of Formants:\n")
    f.write("-----------------------\n")
    f.write("F1: "+str(f1_mean)+"\nF2: "+str(f2_mean)+"\nF3: "+str(f3_mean)+"\nF4: "+str(f4_mean)+"\n")
    f.write("-----------------------------------------------------------------------------------------\n")
    print("MFCC: \n-------\n ",mfcc,file=f)
    f.write("-----------------------------------------------------------------------------------------\n")
    f.write("Formants: \n")
    f.write("-----------------------------------------------------------------------------------------\n")
    print("Object: ",formants, file=f)
    f.write("\n")
    print("Matrix: ",formantsmatrix, file=f)
    f.write("\n")
    f.write("Quantile of Bandwidth : "+ str(formantsQB)+"\n"+ "Mean : "+str(formantsmean)+"\n"+"Standard Deviation: "+str(formantsSD)+"\n")
    f.write("-----------------------------------------------------------------------------------------\n")


print("Launching 2 .DATA and 1 .log files, along with generated data plots in : \n")
if countdown(20)!=True:
   os.startfile(formantmatrixSave)
   os.startfile(mfccdata)
   os.startfile(ops)
else:
    print("Exiting...")

plt.subplot(1,2,1)
plt.title('Speech Signal Representation')
plt.plot(snd.xs(), snd.values.T)
plt.xlim([snd.xmin, snd.xmax])
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
mplcursors.cursor(hover=True)

plt.subplot(1,2,2)
plt.title('Fundamental Frequency F0')
draw_spectrogram(spectrogram)
plt.twinx()
draw_pitch(pitch)
plt.xlim([snd.xmin, snd.xmax])
mplcursors.cursor(hover=True)


mng=plt.get_current_fig_manager()
mng.window.state("zoomed")
plt.show()
f.close()


