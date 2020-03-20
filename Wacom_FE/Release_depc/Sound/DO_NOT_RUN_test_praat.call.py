import parselmouth
import os
from msvcrt import getch
path = os.path.dirname(os.path.abspath(__file__))+"\\output"
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
tnames=[]
for i in listOfFiles:
    temp=i.split('\\')
    tnames.append(str(temp[len(temp)-1]))
for i in tnames:
    if i[len(i)-3:len(i)] == "wav":
          print(i)
 
print("\n\nEnter .wav files to display. 🛈 Copy filenames from above and paste them below.")
search=input()
path=path+"\\"+search[0:-4]
try:
  snd = parselmouth.Sound((os.path.join(path, search)))
except:
      print("Could not read audio!")
      getch()
      exit()
sound = parselmouth.Sound(snd) 
harmonicity = parselmouth.praat.call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
pitch = parselmouth.praat.call(sound, "To Pitch (cc)", 0, 75, 15, 'no', 0.03, 0.45, 0.01, 0.35, 0.14, 600)
pointProcess = parselmouth.praat.call(sound, "To PointProcess (periodic, cc)", 75, 600)
formants = parselmouth.praat.call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
mfcc=parselmouth.praat.call(sound, "To MFCC",12, 0.015, 0.005, 100, 100, 0)
melfilter=parselmouth.praat.call(sound, "To MelFilter",0.015, 0.005, 100, 100, 0)


formantfn="formant_features_for_.DATA"
formantmatrix=os.path.join(path, formantfn)
