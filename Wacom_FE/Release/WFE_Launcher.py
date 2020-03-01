import os
import ctypes
import sys
import psutil
import shutil
from msvcrt import getch
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # origPath=os.path.dirname(os.path.abspath(__file__))+"\\"
    path = os.path.dirname(os.path.abspath(__file__))+"\\MG_Data\\"

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
          #path to MG_Data/CG/
          foldernameCG=input("Enter folder name..\"PD\" is reserved!\n")
          if foldernameCG.lower()=="pd":
              print("Unauthorised")
              getch()
              exit()
          path=path+"CG\\"+foldernameCG+"\\"
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
          if not os.path.exists(path):
             os.makedirs(path)
          #path to MG_Data/foldername/
          badOp=False
       else:
           print("Bad Option\n")

    filenamecoordNew=path
    filenamepressNew=path
    filenamereportNew=path

    
    with open("moveFn.log",'w') as moveFn:
        moveFn.write(filenamecoordNew+"+"+filenamepressNew+"+"+filenamereportNew)

    print("\nFolders created..Starting WFE...\n")
    os.startfile("Wacom Feature Extractor.exe")
    listener=[]
    running=True
    while running==True:
      for p in psutil.process_iter():
         try:
             if(p.name()=="Wacom Feature Extractor.exe"):
                  listener.append(str(p.name()))
         except:
             pass
        
      if "Wacom Feature Extractor.exe" in listener:
          print("WFE running..",end="\r") 
          listener.clear()   
      else:
          running=False

    print("\nWFE now stopped. Press any key to exit..")
    getch()

    # time.sleep(2)

    # data=""
    # with open('filename.log','r') as fl:
    #     for z in fl:
    #       data=data+z

    # filenamelist=data.split("+")

    # filenamecoord=filenamelist[0]
    # filenamepress=filenamelist[1]
    # filenamereport="Report Generated Time_"+filenamecoord[21:len(filenamecoord)-3]+"log"

    
    # shutil.copy(filenamecoord, filenamecoordNew)
    # shutil.copy(filenamepress, filenamepressNew)
    # shutil.copy(filenamereport,filenamereportNew)

    
    # getch()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1) # change the 4th param to "" later (.exe)



