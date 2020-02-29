import matplotlib.pyplot as plt
import csv
import os
import mplcursors
from msvcrt import getch
import time
import msvcrt
import keyboard

x = []
y = []

print("/*View recorded micrographia data*/\n")
print("Pressure/Coordinate DATA\n")

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        try:
           fullPath = os.path.join(dirName, entry)
           if os.path.isdir(fullPath):
              allFiles = allFiles + getListOfFiles(fullPath)
           else:
              allFiles.append(fullPath)
        except:
            pass
                
    return allFiles  

def countdown(t):
    aborted=False
    while t>-1 and aborted==False:
        mins, secs = divmod(t, 60)
        timefmt = '{:02d}:{:02d}'.format(mins, secs)
        print(timefmt, end='\r')
        time.sleep(1)

        if msvcrt.kbhit():
            keypress=msvcrt.getch()
            if keypress == chr(27).encode():
              aborted=True
              return True
            elif keypress == chr(13).encode():
              aborted=True
              return False

        # if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():
        #     aborted=True
        #     return True
        # elif msvcrt.kbhit() and msvcrt.getch() == chr(13).encode():
        #     aborted=True
        #     return False
        t -= 1
        
path = os.path.dirname(os.path.abspath(__file__))+"\\"

if not os.path.exists(path):
    os.makedirs(path)

basepath = path

listOfFiles = getListOfFiles(basepath)
count=1
for i in listOfFiles:
    temp=i.split('\\')
    tempFn=str(temp[len(temp)-1])
    if tempFn[0:5] == "Coord":
      print("\n------------------------------------------------------------------------------------------------------------------------------------\n")  
      print(str(count)+") Filename: "+tempFn+" :--\n")
      count+=1
      print("Copy this:- "+i+"\n")

print("\n\nEnter .csv files to display. 🛈 Copy filenames from above and paste them below.")
search=input()

filenamelist=search.split("\\")
filenamecoord=filenamelist[len(filenamelist)-1]
pathcsv=""
for i in range(len(filenamelist)-1):
    pathcsv=pathcsv+filenamelist[i]+"\\"
filenamepress=pathcsv+"Pressure Data Time_"+filenamecoord[21:len(filenamecoord)]
filenamereport=pathcsv+"Report Generated Time_"+filenamecoord[21:len(filenamecoord)-3]+"log"
try:
   with open(search,'r') as csvfile:
       plots = csv.reader(csvfile, delimiter=',')
       for row in plots:
           x.append(int(row[0]))
           y.append(int(row[1]))
except:
    print("\nCoordinate file not found\nPress any key to exit..")
    getch()
    exit()
plt.subplot(2,1,1)
plt.plot(x,y,'o',label='Pressure Points')
plt.plot(x,y,'-k',label='Tip movement')
ax = plt.gca()
ax.set_ylim(ax.get_ylim()[::-1])
plt.xlabel('x pixels')
plt.ylabel('y pixels')
plt.title('Coordinate data Scatter plot')
plt.tight_layout(pad=0.4)
plt.legend()

x = []

try:
    with open(filenamepress,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(int(row[0]))
except:
    print("\nPressure file not found\nPress any key to exit..")
    getch()
    exit()

plt.subplot(2,1,2)
plt.plot(x, label='xy plot')
plt.xlabel('Coordinate plot pressure points (x)')
plt.ylabel('Pressure (y)')
plt.title('Presssure data 2D plot')
plt.legend()
plt.tight_layout(pad=0.4)


mng=plt.get_current_fig_manager()
mng.window.state("zoomed")
mplcursors.cursor(hover=True)
plt.show()

print("Launching 2 .csv data files and 1 .log file in..Press 'esc' to exit. Double-Tap 'Enter' to open now.")
repNotGen=False
repNotFound=False
repAlreadyShown=False
if countdown(6)!=True:
   try:
       os.startfile(filenamereport)
       repAlreadyShown=True
   except:
       repNotFound=True
       print("\n\nNo generated report found...Generate report? Y/N.\n")
       consent=input()
       if consent.lower()=="y":
         noofcoordinates=0
         with open(search,'r') as csvfile:
           plots = csv.reader(csvfile, delimiter=',')
           for row in plots:
                 noofcoordinates+=1
  
         tempPress=0
         cpenup=0
         c=0
         noofpressurepoints=0
         pressureSum=0
         with open(filenamepress,'r') as csvfile:
           plots = csv.reader(csvfile, delimiter=',')
           for row in plots:
             if int(row[0])!=0 and tempPress==0:
                 cpenup+=1
             if int(row[0])!=0:
                 noofpressurepoints+=1
                 if c<1:
                     start=time.time()
                     c+=1
                 finish=time.time()

             tempPress=int(row[0])
             pressureSum = pressureSum + int(row[0])
  
         elapsedtime=(finish-start)*10000
         avgpressure = pressureSum/noofpressurepoints
         avgspeed=noofcoordinates/elapsedtime
         cisp=avgpressure*avgspeed

         with open(filenamereport, 'w') as f:
             f.write("Automatic Report Generated for +"+filenamecoord+"+ and +"+"Pressure Data Time_"+filenamecoord[21:len(filenamecoord)]+"+\n")
             f.write("=======================================================================================================\n\n")
             f.write("Pen UP-Down Count="+str(cpenup)+"\n")
             f.write("Weighted Average Pen Pressure="+str(avgpressure)+" units\n")
             f.write("Elapsed Time(for drawing)="+str(elapsedtime)+" seconds\n")
             f.write("Weighted Average Speed="+str(avgspeed)+" pixels/sec\n")
             f.write("No. of Pressure Points="+str(noofpressurepoints)+" pixels\n")
             f.write("Composite Index of Speed and Pen-pressure="+str(cisp)+" pixels.units/sec\n\n")
             f.write("----------------End Of File----------------")
       else:
           print("\nReport not generated.\n")
           repNotGen=True

   if repNotFound==True and repNotGen==False and repAlreadyShown==False:
      os.startfile(filenamereport)
   os.startfile(search)
   os.startfile(filenamepress)
else:
    print("Exiting...")
