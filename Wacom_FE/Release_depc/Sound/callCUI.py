import parselmouth
import os
import subprocess
import datetime
from msvcrt import getch
import pickle

print("/*Does a data dump of Praat Objects*/ © Souvik Chakraborty,2020\n")

objListname=[]
objList=[]

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
tnames=[]
listOfFiles = getListOfFiles(basepath) 
for i in listOfFiles:
    temp=i.split('\\')
    tnames.append(str(temp[len(temp)-1]))
for i in tnames:
    if i[len(i)-3:len(i)] == "wav":
          print(i)


 
print("\n\nEnter .wav files to display. 🛈 Copy filenames from above and paste them below.")
search=input()
x=input("Save As?\n")
sfn="dataDump"+"_for_"+x+".log"

path0 = os.path.dirname(os.path.abspath(__file__))+"\\dataDump"

path=path+"\\"+search[0:-4]

if not os.path.exists(path0):
    os.makedirs(path0)
ops=os.path.join(path0, sfn)


try:
  snd = parselmouth.Sound(os.path.join(path,search))
except:
      print("Could not read audio!\n")
      print("Press any key to exit")
      getch()
      exit()

sound = parselmouth.Sound(snd) 
harmonicity = parselmouth.praat.call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
pitch = parselmouth.praat.call(sound, "To Pitch (cc)", 0, 75, 15, 'no', 0.03, 0.45, 0.01, 0.35, 0.14, 600)
pointProcess = parselmouth.praat.call(sound, "To PointProcess (periodic, cc)", 75, 600)
formant = parselmouth.praat.call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
mfcc=parselmouth.praat.call(sound, "To MFCC",12, 0.015, 0.005, 100, 100, 0)
melfilter=parselmouth.praat.call(sound, "To MelFilter",0.015, 0.005, 100, 100, 0)

objdict=[]
objdict.append(harmonicity)
objdict.append(pitch)
objdict.append(pointProcess)
objdict.append(formant)
objdict.append(sound)
objdict.append(mfcc)
objdict.append(melfilter)


path2 = os.path.dirname(os.path.abspath(__file__))+"\\dataDump\\db"
if not os.path.exists(path2):
    os.makedirs(path2)
dfn="dictPickle.log"
dictPickle=os.path.join(path2,dfn)

try:
     with open(dictPickle, "rb") as fp:  
        objdict=pickle.load(fp)
except:
    pass
try:
     with open(dictPickle, "wb") as fp:  
        pickle.dump(objdict, fp)
except Exception as e:
     print(e)
     print("\nPickling still doesn't work :( \n")
     pass


noofpraatdata=input("No. of data variables required(parselmouth.data)? E.g: call([sound, pointProcess]..., 2 in this case\n")
print("Enter these one by one in order and press return.\n")

for i in range(int(noofpraatdata)):
     objListname.append(input())
     
for i in range(int(noofpraatdata)):
     objListname[i].lower()

objdictnames=[]
for i in range(len(objdict)):
        objdictnames.append(type(objdict[i]).__name__.lower())

for i in range(len(objListname)):
      for j in range(len(objdict)):
            if objListname[i]==objdictnames[j]:
               objList.append(objdict[j])

strCommand=input("\nEnter EXACT call command. E.g: \"Get jitter (local)\" (without quotes)\n")

noofparams=input("\nEnter no. of parameters. E.g: parselmouth.praat.call(snd, \"To PointProcess (periodic, cc)\", 75, 600)...2 in this case\n")

noofparams=int(noofparams)

try:
     if noofparams==0 or not objList:
           tempobj=parselmouth.praat.call(strCommand)
     elif noofparams==1:
           print("\nEnter 1 param/s in order.\n")
           p1=input()
           tempobj=parselmouth.praat.call(objList,strCommand,float(p1))
     elif noofparams==2:
           print("\nEnter 2 param/s in order.\n")
           p1=input()
           p2=input()
           tempobj=parselmouth.praat.call(objList,strCommand,float(p1),float(p2))
     elif noofparams==3:
           print("\nEnter 3 param/s in order.\n")
           p1=input()
           p2=input()
           p3=input()
           tempobj=parselmouth.praat.call(objList,strCommand,float(p1),float(p2),float(p3))
     elif noofparams==4:
           print("\nEnter 4 param/s in order.\n")
           p1=input()
           p2=input()
           p3=input()
           p4=input()
           tempobj=parselmouth.praat.call(objList,strCommand,float(p1),float(p2),float(p3),float(p4))
     elif noofparams==5:
           print("\nEnter 5 param/s in order.\n")
           p1=input()
           p2=input()
           p3=input()
           p4=input()
           p5=input()
           tempobj=parselmouth.praat.call(objList,strCommand,float(p1),float(p2),float(p3),float(p4),float(p5))
     elif noofparams==6:
           print("\nEnter 6 param/s in order.\n")
           p1=input()
           p2=input()
           p3=input()
           p4=input()
           p5=input()
           p6=input()
           tempobj=parselmouth.praat.call(objList,strCommand,float(p1),float(p2),float(p3),float(p4),float(p5),float(p6))
     elif noofparams==7:
           print("\nEnter 7 param/s in order.\n")
           p1=input()
           p2=input()
           p3=input()
           p4=input()
           p5=input()
           p6=input()
           p7=input()
           tempobj=parselmouth.praat.call(objList,strCommand,float(p1),float(p2),float(p3),float(p4),float(p5),float(p6),float(p7))
     elif noofparams==8:
           print("\nEnter 8 param/s in order.\n")
           p1=input()
           p2=input()
           p3=input()
           p4=input()
           p5=input()
           p6=input()
           p7=input()
           p8=input()
           tempobj=parselmouth.praat.call(objList,strCommand,float(p1),float(p2),float(p3),float(p4),float(p5),float(p6),float(p7),float(p8))
except Exception as e:
     print("Error.\n")
     print(e)
     print("\npress any key to exit")
     junk=getch()
     exit()
     


with open(ops, 'w') as f:
    f.write('-----------------------------------------------------------------------------------------\n')
    print("Dump :\n ", tempobj, file=f)
    f.write('-----------------------------------------------------------------------------------------\n')
    f.close




print("Data dumped @ /dataDump\n")

with open(ops,'r') as fi:
    print(fi.readlines())


os.startfile(ops)

print("press any key to exit")
junk=getch()