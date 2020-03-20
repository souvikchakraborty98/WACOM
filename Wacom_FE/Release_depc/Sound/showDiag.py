import parselmouth
import numpy as np
import seaborn as sep
import matplotlib.pyplot as plt
import mplcursors
import os
from msvcrt import getch
import datetime
import time
import msvcrt
import subprocess

print("/*Displays recorded data for selected files.*/\n")

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

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
         fullPath = os.path.join(dirName, entry)
         if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
         else:
            allFiles.append(fullPath)
                
    return allFiles  

path = os.path.dirname(os.path.abspath(__file__))+"\\output\\"

if not os.path.exists(path):
    os.makedirs(path)

basepath = path

listOfFiles = getListOfFiles(basepath)
# tnames=[]
# for i in listOfFiles:
#     temp=i.split('\\')
#     tnames.append(str(temp[len(temp)-1]))
# for i in tnames:
#     if i[len(i)-3:len(i)] == "wav":
#           print(i)

count=1
for i in listOfFiles:
    temp=i.split('\\')
    tempFn=str(temp[len(temp)-1])
    if tempFn[len(tempFn)-3:len(tempFn)] == "wav":
      print("\n------------------------------------------------------------------------------------------------------------------------------------\n")  
      print(str(count)+") Filename: "+tempFn+" :--\n")
      count+=1
      print("Copy this:- "+i+"\n")

print("\n\nEnter .wav files to display. 🛈 Copy filenames from above and paste them below.")
search=input()
filenamelist=search.split("\\")
filenamenew=filenamelist[len(filenamelist)-1]
pathnew=""
for i in range(len(filenamelist)-1):
    pathnew=pathnew+filenamelist[i]+"\\"

sfn="soundData"+"_for_"+filenamenew[0:-4]+".log"
ops=os.path.join(pathnew, sfn)

mfccfn="MFCC_features_for_"+filenamenew[0:-4]+".DATA"
mfccdata=os.path.join(pathnew, mfccfn)

formantfn="Formant_features_for_"+filenamenew[0:-4]+".DATA"
formantmatrixSave=os.path.join(pathnew,formantfn)

try:
    snd = parselmouth.Sound(search)
except:
    print("\nFile not found/Not a .wav file")
    print("Press any key to exit")
    getch()
    quit()

sep.set()

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

pitch = snd.to_pitch()
pre_emphasized_snd = snd.copy()
pre_emphasized_snd.pre_emphasize()
spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)



# sfn="soundData"+"_for_"+fn+".log"
# ops=os.path.join(path, sfn)
# with open(ops, 'w') as f:
#     f.write('-----------------------------------------------------------------------------------------\n')
#     print('About:', pitch, file=f)
print("Launching 2 .DATA and 1 .log files, along with generated data plots in : \n")
if countdown(20)!=True:
  try:
      subprocess.Popen(["notepad.exe", formantmatrixSave])
  except:
      pass
  try:
      subprocess.Popen(["notepad.exe", mfccdata])
  except:
      pass
  try:
      subprocess.Popen(["notepad.exe", ops])
  except:
      pass
    
    
   
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



