import matplotlib.pyplot as plt
import csv
import os
import mplcursors
import time
import msvcrt
from msvcrt import getch

x = []
y = []

path = os.path.dirname(os.path.abspath(__file__))+"\\"

data=""
f = open("filename.log", "r")

for z in f:
    data=data+z

# def countdown(t):
#     aborted=False
#     while t>-1 and aborted==False:
#         mins, secs = divmod(t, 60)
#         timefmt = '{:02d}:{:02d}'.format(mins, secs)
#         print(timefmt, end='\r')
#         time.sleep(1)
#         if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():
#             aborted=True
#             return True
#         t -= 1
        
filenamelist=data.split("+")
filenamecoord=filenamelist[0]
filenamepress=filenamelist[1]
filenamereport=path+"Report Generated Time_"+filenamecoord[21:len(filenamecoord)-3]+"log"

try:    
  with open(filenamecoord,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(int(row[1]))
except:
    print("Access Error")
    getch()

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

with open(filenamepress,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))

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

plt.draw()
#os.startfile("Wacom Feature Extractor.exe")

#print("Launching 2 .csv data files in..Press 'esc' to exit.")
#if countdown(6)!=True:
os.startfile(filenamecoord)
os.startfile(filenamepress)
os.startfile(filenamereport)
#else:
#print("Exiting...")

plt.show()