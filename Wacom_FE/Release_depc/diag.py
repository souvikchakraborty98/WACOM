import matplotlib.pyplot as plt
import csv
import os
import mplcursors
import time
import msvcrt
import shutil
from msvcrt import getch
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():        
 x = []
 y = []

 path = os.path.dirname(os.path.abspath(__file__))+"\\"

 if not os.path.exists(path):
      os.makedirs(path)

 data=""
 with open("filename.log", "r") as f:
    for z in f:
     data=data+z


        
 filenamelist=data.split("+")
 filenamecoord=filenamelist[0]
 filenamepress=filenamelist[1]
 filenamereport="Report Generated Time_"+filenamecoord[21:len(filenamecoord)-3]+"log"


 datanew=""
 with open("moveFn.log",'r') as moveFn:
      for z in moveFn:
        datanew=datanew+z

 filenamelistnew=datanew.split("+")
 filenamecoordNew=filenamelistnew[0]+filenamecoord
 filenamepressNew=filenamelistnew[1]+filenamepress
 filenamereportNew=filenamelistnew[2]+filenamereport

 
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


 shutil.move(filenamecoord, filenamecoordNew)
 shutil.move(filenamepress, filenamepressNew)
 shutil.move(filenamereport,filenamereportNew)
 
 os.startfile(filenamecoordNew)
 os.startfile(filenamepressNew)
 os.startfile(filenamereportNew)

 plt.show()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1) # change the 4th param to "" later (.exe)