import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot as plt

path=""

pathAudInstruction=""
selMG=""
selSpeech=""
audioListFile=[]

pFlag=False
cFlagMG=False
cFlagSpeech=False
recordMGFlag=False
recordRunning=False
instructionPlaying=False

IpDevCurrentInd=0
OpDevCurrentInd=0

sprecNamesCG=[]
sptestNamesCG=[]
sprecNamesPD=[]
sptestNamesPD=[]
mgtesttypesCG=[]
mgtestNamesCG=[]
mgtesttypesPD=[]
mgtestNamesPD=[]


class SpeechWorker(QtCore.QThread):
    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, Tname):
        self.Tname=Tname
        QtCore.QThread.__init__(self)
        global recordRunning
        recordRunning=True

    def run(self):        
        p = pyaudio.PyAudio() 
        pathSound=path+'/'+'Speech_Data'+'/'+selSpeech+"/"+str(self.Tname)+"/"
        print(f"speech path: {pathSound}")
        if not os.path.exists(pathSound):
            os.makedirs(pathSound)

        xb=self.Tname
        fcurmil=str(datetime.datetime.now().strftime("%f"))+"_TestName_"+xb
        fn=fcurmil+".wav"

        mfccfn="MFCC_features_for_"+fcurmil+".DATA"
        mfccdata=os.path.join(pathSound, mfccfn)

        formantfn="Formant_features_for_"+fcurmil+".DATA"
        formantmatrixSave=os.path.join(pathSound,formantfn)        

        def is_silent(self,snd_data):
            return max(snd_data) < THRESHOLD

        def normalize(self,snd_data):
            MAXIMUM = 16384  #increasing this might increase noise
            times = float(MAXIMUM)/max(abs(i) for i in snd_data)

            r = array('h')
            for i in snd_data:
                r.append(int(i*times))
            return r

        def trim(self,snd_data):
            def trim1(self,snd_data):
                snd_started = False
                r = array('h')

                for i in snd_data:
                    if not snd_started and abs(i)>THRESHOLD:
                        snd_started = True
                        r.append(i)
                    elif snd_started:
                        r.append(i)
                return r


            snd_data = trim1(self,snd_data) #samne
            snd_data.reverse()
            snd_data = trim1(self,snd_data) #piche
            snd_data.reverse()
            return snd_data

        def add_silence(self,snd_data, seconds):
            r = array('h', [0 for i in range(int(seconds*RATE))]) #samne
            r.extend(snd_data)
            r.extend([0 for i in range(int(seconds*RATE))]) #piche
            return r

        def record(self):
            try:
                stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE, input_device_index=INPUT_DEVICE_IND)
            except:
                try:
                    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE)
                except Exception as e:
                    print(str(e))
                    consent = QtWidgets.QMessageBox.warning(self,"Warning","An Error occured! Please ensure resources are not being used by other applications.",QtWidgets.QMessageBox.Ok)
                    if consent==QtWidgets.QMessageBox.Ok:
                        sys.exit()
            
            num_silent = 0
            snd_started = False

            r = array('h')

            while 1:
                snd_data = array('h', stream.read(CHUNK_SIZE))
                if byteorder == 'big':
                    snd_data.byteswap()
                r.extend(snd_data)
                print(max(snd_data))
                self.signal.emit(str(max(snd_data))+"\n")
                silent = is_silent(self,snd_data)

                if silent and snd_started:
                    num_silent += 1
                elif not silent and not snd_started:
                    snd_started = True

                if snd_started and num_silent > 300: #increase this to increase timeout
                    break

            sample_width = p.get_sample_size(FORMAT)
            stream.stop_stream()
            stream.close()
            p.terminate()

            r = normalize(self,r)
            r = trim(self,r)
            r = add_silence(self,r, 0.5)
            return sample_width, r

        def record_to_file(self,path):
            sample_width, data = record(self)
            data = pack('<' + ('h'*len(data)), *data)

            wf = wave.open(path, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(sample_width)
            wf.setframerate(RATE)
            wf.writeframes(data)
            wf.close()
            self.signal.emit("#record_end")
            self.signal.emit("Done...Written to "+os.path.join(pathSound, fn)+"\n")

        
        print("Listening..")    
        record_to_file(self,os.path.join(pathSound, fn))
        global recordRunning
        recordRunning=False
        print("Done...Written to "+os.path.join(pathSound, fn)+"\n")
        

        sep.set()
        snd = parselmouth.Sound((os.path.join(pathSound, fn)))
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
        ops=os.path.join(pathSound, sfn)
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
        
        subprocess.Popen(["notepad.exe", formantmatrixSave])
        subprocess.Popen(["notepad.exe", mfccdata])
        subprocess.Popen(["notepad.exe", ops])

        plt.figure(num=self.Tname) 
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
        plt.draw()
        plt.show()
        f.close()
        self.signal.emit("#end")

    def stop(self):
        global recordRunning
        recordRunning=False
        self.terminate()



class MGWorker(QtCore.QThread):
    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self,Tname):
        self.Tname=Tname
        QtCore.QThread.__init__(self)

    def run(self): 

        if self.Tname=="Arch.Guided Spiral":
            appendAtLast="Arch_Guided_Spiral"
        elif self.Tname=="Repeat Letters":
            appendAtLast="Repeat_Letters"
        elif self.Tname=="Copy Sentence":
            appendAtLast="Copy_Sentence"
        elif self.Tname=="Switching Letters":
            appendAtLast="Switching_Letters"

        pathMgData = path+"\\MG_Data\\"+selMG+"\\"+appendAtLast+"\\"
        print(f"Micrographia path: {pathMgData}")
        if not os.path.exists(pathMgData):
            os.makedirs(pathMgData)

        filenamecoordNew=pathMgData
        filenamepressNew=pathMgData
        filenamereportNew=pathMgData

        with open("moveFn.log",'w') as moveFn:
                moveFn.write(filenamecoordNew+"+"+filenamepressNew+"+"+filenamereportNew)

        print("\nFolders created..Starting WFE...\n")
        try:
            os.startfile("Wacom Feature Extractor.exe")
        except Exception as e:
                self.signal.emit("Error")
                
        listener=[]
        running=True

        while running==True:
             c = wmi.WMI ()
             print("\n\ncalled wmi\n\n")
             for process in c.Win32_process(): 
                p=str(process.Name)
                print(p)
                try:
                  if p=="Wacom Feature Extractor.exe":
                     listener.append(p)
                     print("\n\nfound\n\n")
                     break
                except Exception as e:
                         print(e)
                         pass
            
             if "Wacom Feature Extractor.exe" in listener:
                 print("WFE running..",end="\r")
                 self.signal.emit("Extracting...") 
                 listener.clear()   
             else:
                 running=False
             sleep(2)
        
        print("\nWFE now stopped.")
        self.signal.emit("Extractor Stopped")
    
    def stop(self):
        self.terminate()

class playTestSoundWorker(QtCore.QThread):
    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self,Fname):
        self.Fname=Fname
        QtCore.QThread.__init__(self)

    def run(self):    
        filename =self.Fname
        chunk = 1024  
        self.wf = wave.open(filename, 'rb')
        self.p = pyaudio.PyAudio()
        try:
            self.stream = self.p.open(format = self.p.get_format_from_width(self.wf.getsampwidth()), channels = self.wf.getnchannels(), rate = self.wf.getframerate(),output_device_index=OUTPUT_DEVICE_IND, output = True)
        except:
            self.stream = self.p.open(format = self.p.get_format_from_width(self.wf.getsampwidth()), channels = self.wf.getnchannels(), rate = self.wf.getframerate(), output = True)
        data = self.wf.readframes(chunk)
        try:
            while data != b'':
                self.stream.write(data)
                data = self.wf.readframes(chunk)
        except:
            pass
        
        self.wf.close()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.signal.emit("Stopped")
    
    def stop(self):
        try:
            self.wf.close()
        except:
            pass
        try:
            self.stream.stop_stream()
        except:
            pass
        try:
            self.stream.close()
        except:
            pass
        try:
            self.p.terminate()
        except:
            pass
        self.signal.emit("Stopped")
        print("Wav player terminated.")
        self.terminate()


class Ui_DialogPreRecordedInst(QtWidgets.QDialog):
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(507, 399)
        Dialog.setWindowIcon(QtGui.QIcon('appRes/mic.png'))
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Dialog.setFixedSize(Dialog.size())
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(130, 350, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.audioList = QtWidgets.QListWidget(Dialog)
        self.audioList.setGeometry(QtCore.QRect(20, 20, 471, 251))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.audioList.setFont(font)
        self.audioList.setObjectName("audioList")

        try:
            global audioListFile
            with open('appRes/store.dat', 'rb') as f:
                audioListFile = pickle.load(f)
                self.audioList.addItems(audioListFile)
        except:
            print("Initialize store.dat")
            pass

        self.addItems = QtWidgets.QPushButton(Dialog)
        self.addItems.setGeometry(QtCore.QRect(20, 290, 91, 23))
        self.addItems.setObjectName("addItems")
        self.deleteItems = QtWidgets.QPushButton(Dialog)
        self.deleteItems.setGeometry(QtCore.QRect(140, 290, 91, 23))
        self.deleteItems.setObjectName("deleteItems")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.addItems.clicked.connect(self.onClickedAddItemsBtn)
        self.deleteItems.clicked.connect(self.onClickedDeleteItemsBtn)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Pre Recorded Instructions"))
        self.addItems.setText(_translate("Dialog", "Add Item.."))
        self.deleteItems.setText(_translate("Dialog", "Delete Item.."))

    def onClickedAddItemsBtn(self):
        global audioListFile
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Add Audio", "", "WAV Audio Files (*.wav);;All Files (*)") 
        if fileName:
            global pathAudInstruction
            temp=str(fileName).split('/')
            tempFn=temp[len(temp)-1]
            if self.audioList.findItems(tempFn,QtCore.Qt.MatchContains):
                tempRow=self.audioList.row((self.audioList.findItems(tempFn,QtCore.Qt.MatchContains))[0])
                consent = QtWidgets.QMessageBox.question(self,"Confirmation","Item already exists. Replace?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if consent == QtWidgets.QMessageBox.Yes:
                    try:
                        self.audioList.takeItem(tempRow)
                        print("Item Deleted")
                        pathAudInstruction=os.path.dirname(fileName)
                        print(pathAudInstruction)
                        print(tempFn)
                        shutil.copy(fileName,'appRes/recordings/')
                        self.audioList.addItem(tempFn)
                        print("Item Replaced")
                    except Exception as e:
                        consent = QtWidgets.QMessageBox.warning(self,"Warning","An Error occured! Please ensure resources are not being used by other applications.",QtWidgets.QMessageBox.Ok)
                        print(e)
                        pass
            else:
                try:
                    pathAudInstruction=os.path.dirname(fileName)
                    print(pathAudInstruction)
                    print(tempFn)
                    shutil.copy(fileName,'appRes/recordings/')
                    self.audioList.addItem(tempFn)
                    audioListFile.append(tempFn)
                    with open('appRes/store.dat', 'wb') as f:
                        pickle.dump(audioListFile, f)
                    print("Added to list")
                except Exception as e:
                    consent = QtWidgets.QMessageBox.warning(self,"Warning","An Error occured! Please ensure resources are not being used by other applications.",QtWidgets.QMessageBox.Ok)
                    print(e)
                    pass
    
    def onClickedDeleteItemsBtn(self):
        if self.audioList.currentItem():
            currentText=str(self.audioList.currentItem().text())
            consent = QtWidgets.QMessageBox.question(self,"Confirmation",f"Delete Item \"{currentText}\"?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if consent == QtWidgets.QMessageBox.Yes:
                self.audioList.takeItem(self.audioList.currentRow())
                try:
                    global audioListFile
                    audioListFile.remove(currentText)
                    with open('appRes/store.dat', 'wb') as f:
                        pickle.dump(audioListFile, f)
                    if os.path.exists(f"appRes/recordings/{currentText}"):
                         os.remove(f"appRes/recordings/{currentText}")
                    print("Removed from list")
                except Exception as e:
                    print(f"Value error: {e}")
                    consent = QtWidgets.QMessageBox.warning(self,"Warning","An Error occured! Please ensure resources are not being used by other applications.",QtWidgets.QMessageBox.Ok)
                    pass     
        else:
            consent = QtWidgets.QMessageBox.information(self,"Information","Nothing selected!",QtWidgets.QMessageBox.Ok)
    

class Ui_DialogPlayInstruction(QtWidgets.QDialog):
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 150)
        Dialog.setWindowIcon(QtGui.QIcon('appRes/ins.ico'))
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Dialog.setFixedSize(Dialog.size())
        self.label_choose = QtWidgets.QLabel(Dialog)
        self.label_choose.setGeometry(QtCore.QRect(20, 20, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_choose.setFont(font)
        self.label_choose.setObjectName("label_choose")
        self.chooseInstCombo = QtWidgets.QComboBox(Dialog)
        self.chooseInstCombo.setGeometry(QtCore.QRect(20, 60, 301, 22))
        self.chooseInstCombo.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.chooseInstCombo.setFont(font)
        self.chooseInstCombo.setObjectName("chooseInstCombo")
        self.playInstBtn = QtWidgets.QPushButton(Dialog)
        self.playInstBtn.setGeometry(QtCore.QRect(340, 52, 31, 31))
        self.playInstBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("appRes/Play.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playInstBtn.setIcon(icon)
        self.playInstBtn.setObjectName("playInstBtn")
        self.playInstBtn.clicked.connect(self.onClickedplayInstBtn)
        self.continueToRecordBtn = QtWidgets.QPushButton(Dialog)
        self.continueToRecordBtn.setGeometry(QtCore.QRect(274, 110, 81, 23))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.continueToRecordBtn.setFont(font)
        self.continueToRecordBtn.setObjectName("continueToRecordBtn")
        self.cancelRecord = QtWidgets.QPushButton(Dialog)
        self.cancelRecord.setGeometry(QtCore.QRect(10, 110, 104, 23))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.cancelRecord.setFont(font)
        self.cancelRecord.setObjectName("cancelRecord")
        self.continueToRecordBtn.clicked.connect(self.onClickedContinueToRecordBtn)
        self.cancelRecord.clicked.connect(self.onClickedCancelRecordBtn)
        self.retranslateUi(Dialog)

        if len(audioListFile)==0:
            self.chooseInstCombo.addItem("No Instructions Found")
            self.playInstBtn.setEnabled(False)
        else:
            self.chooseInstCombo.addItems(audioListFile)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Pre Recorded Instructions Player"))
        self.label_choose.setText(_translate("Dialog", "Choose Instruction:"))
        self.continueToRecordBtn.setText(_translate("Dialog", "Continue"))
        self.cancelRecord.setText(_translate("Dialog", "Terminate Record"))

    def onClickedplayInstBtn(self):
        self.playInstBtn.setEnabled(False)
        global instructionPlaying
        if not instructionPlaying:           
            instructionPlaying=True
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("appRes/Stop.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.playInstBtn.setIcon(icon)
            self.newThread = playTestSoundWorker(f'appRes/recordings/{self.chooseInstCombo.currentText()}')
            self.newThread.signal.connect(self.instructionPlayerSignals)
            try:
                self.newThread.start()
            except:
                pass
            self.playInstBtn.setEnabled(True)
        else:
            try:
                self.newThread.stop()
            except:
                pass
            instructionPlaying=False
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("appRes/Play.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.playInstBtn.setIcon(icon)
            self.playInstBtn.setEnabled(True)


    def instructionPlayerSignals(self):
        global instructionPlaying
        print("Stopped")
        instructionPlaying=False
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("appRes/Play.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playInstBtn.setIcon(icon)

    def closeEvent(self,evnt):
        global instructionPlaying
        close = QtWidgets.QMessageBox.question(self,"Confirmation","Are you sure you want to stop playing instruction?\nControl will pass to recorder.",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            if instructionPlaying:
                instructionPlaying=False
                try:
                    self.newThread.stop()
                except:
                    pass
            super(Ui_DialogPlayInstruction, self).closeEvent(evnt)
        else:
            evnt.ignore()

    def onClickedContinueToRecordBtn(self):
        global instructionPlaying 
        close = QtWidgets.QMessageBox.question(self,"Confirmation","Are you sure you want to continue?\nControl will pass to recorder.",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
             if instructionPlaying:
                self.newThread.stop()
                instructionPlaying=False
             self.done(0)

    def onClickedCancelRecordBtn(self):
        global instructionPlaying 
        close = QtWidgets.QMessageBox.question(self,"Confirmation","Are you sure you want to force terminate?\nControl will NOT pass to recorder.",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
             if instructionPlaying:
                self.newThread.stop()
                instructionPlaying=False
             self.done(2)
    

class Ui_DialogAbout(QtWidgets.QDialog):
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("DialogAbout")
        Dialog.resize(496, 365)
        Dialog.setWindowIcon(QtGui.QIcon('appRes/logo.ico'))
        Dialog.setFixedSize(Dialog.size())
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(20, 60, 451, 281))
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "About PDFE"))
        self.label.setText(_translate("Dialog", "About"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Copyright 2020 <a href=\"https://github.com/souvikchakraborty98/WACOM/blob/master/README.md\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">Souvik Chakraborty</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the &quot;Software&quot;), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">THE SOFTWARE IS PROVIDED &quot;AS IS&quot;, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</span></p></body></html>"))


class Ui_DialogAudioDevSel(QtWidgets.QDialog):
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.listIPDev()
        self.listOPDev()
        
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setWindowIcon(QtGui.QIcon('appRes/mic.png'))
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Dialog.setFixedSize(Dialog.size())
        self.buttonBox_audio = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox_audio.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox_audio.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_audio.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_audio.setObjectName("buttonBox_audio")
        self.comboBox_audio_in = QtWidgets.QComboBox(Dialog)
        self.comboBox_audio_in.setGeometry(QtCore.QRect(40, 70, 231, 22))
        self.comboBox_audio_in.setObjectName("comboBox_audio_in")
        self.comboBox_audio_in.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.label_audio_in = QtWidgets.QLabel(Dialog)
        self.label_audio_in.setGeometry(QtCore.QRect(40, 30, 51, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_audio_in.setFont(font)
        self.label_audio_in.setObjectName("label_audio_in")
        self.label_audio_out = QtWidgets.QLabel(Dialog)
        self.label_audio_out.setGeometry(QtCore.QRect(40, 110, 61, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_audio_out.setFont(font)
        self.label_audio_out.setObjectName("label_audio_out")
        self.comboBox_audio_out = QtWidgets.QComboBox(Dialog)
        self.comboBox_audio_out.setGeometry(QtCore.QRect(40, 140, 231, 22))
        self.comboBox_audio_out.setObjectName("comboBox_audio_out")
        self.comboBox_audio_out.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.refreshBtn = QtWidgets.QPushButton(Dialog)
        self.refreshBtn.setGeometry(QtCore.QRect(350, 10, 31, 31))
        self.refreshBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("appRes/refresh.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshBtn.setIcon(icon)
        self.refreshBtn.setObjectName("refreshBtn")
        self.PlayBtnTest = QtWidgets.QPushButton(Dialog)
        self.PlayBtnTest.setGeometry(QtCore.QRect(284, 140, 31, 23))
        self.PlayBtnTest.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("appRes/Play.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlayBtnTest.setIcon(icon1)
        self.PlayBtnTest.setObjectName("PlayBtnTest")

        self.retranslateUi(Dialog)

        self.buttonBox_audio.accepted.connect(Dialog.accept)
        self.buttonBox_audio.rejected.connect(Dialog.reject)
        self.refreshBtn.clicked.connect(self.refreshDevList)
        self.PlayBtnTest.clicked.connect(self.testDevSound)
        self.comboBox_audio_in.activated.connect(self.ipSel)
        self.comboBox_audio_out.activated.connect(self.opSel)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Audio Device Selection"))
        self.label_audio_in.setText(_translate("Dialog", "Audio In:"))
        self.label_audio_out.setText(_translate("Dialog", "Audio Out:"))

    def testDevSound(self):
        self.newThread = playTestSoundWorker('appRes/tone.wav')
        self.newThread.signal.connect(self.testSoundPlayStopped)
        self.newThread.start()


    def testSoundPlayStopped(self,result):
        # self.newThread.stop()
         print('Test Play Stopped')
        
        
    def closeEvent(self, evnt):
         super(Ui_DialogAudioDevSel, self).closeEvent(evnt)

    def refreshDevList(self):
        self.listIPDev()
        self.listOPDev()
         
    def accept(self):
        try:
            tempIndex= (self.comboBox_audio_in.currentText()).split(".")
            global INPUT_DEVICE_IND
            INPUT_DEVICE_IND=int(tempIndex[0])
            tempIndex= (self.comboBox_audio_out.currentText()).split(".")
            global OUTPUT_DEVICE_IND
            OUTPUT_DEVICE_IND=int(tempIndex[0])
            print(f"INPUT_DEVICE_IND: {INPUT_DEVICE_IND}\nOUTPUT_DEVICE_IND: {OUTPUT_DEVICE_IND}")
        except:
            pass
        super(Ui_DialogAudioDevSel, self).accept()
        
    def reject(self):
        print("Nope")
        super(Ui_DialogAudioDevSel, self).reject()

    def listIPDev(self):
        Ipdvc=[]
        try:
          p=pyaudio.PyAudio()
        except:
            pass
        self.comboBox_audio_in.clear()
        for i in range(p.get_device_count()):
            if p.get_device_count()!=0:
                if p.get_device_info_by_index(i).get('maxInputChannels')>0 and '@' not in p.get_device_info_by_index(i).get('name') and int(p.get_device_info_by_index(i).get('hostApi'))==0 and p.get_device_info_by_index(i).get('name')!="Microsoft Sound Mapper - Input":
                    Ipdvc.append(f"{str(p.get_device_info_by_index(i).get('index'))}. {str(p.get_device_info_by_index(i).get('name'))}...")
            
        if len(Ipdvc)==0:
             Ipdvc.append("No I/P Devices found")
        p.terminate()
        self.comboBox_audio_in.insertItems(0,Ipdvc)
        tempIndex= (self.comboBox_audio_in.currentText()).split(".")
        global INPUT_DEVICE_IND
        INPUT_DEVICE_IND=int(tempIndex[0])
        try:
           self.comboBox_audio_in.setCurrentIndex(IpDevCurrentInd)
        except Exception as e:
            print(e)
            pass


    def listOPDev(self):
        Opdvc=[]
        try:
         p=pyaudio.PyAudio()
        except Exception as e:
            print(e)
            pass
        self.comboBox_audio_out.clear()
        for i in range(p.get_device_count()):
            if p.get_device_info_by_index(i).get('maxOutputChannels')>=2 and '@' not in p.get_device_info_by_index(i).get('name') and int(p.get_device_info_by_index(i).get('hostApi'))==0 and p.get_device_info_by_index(i).get('name')!="Microsoft Sound Mapper - Output":
                Opdvc.append(f"{str(p.get_device_info_by_index(i).get('index'))}. {str(p.get_device_info_by_index(i).get('name'))}...")
           
        if len(Opdvc)==0:
             Opdvc.append("No O/P Devices found")
        p.terminate()
        self.comboBox_audio_out.insertItems(0,Opdvc)
        tempIndex= (self.comboBox_audio_out.currentText()).split(".")
        global OUTPUT_DEVICE_IND
        OUTPUT_DEVICE_IND=int(tempIndex[0])
        try:
            self.comboBox_audio_out.setCurrentIndex(OpDevCurrentInd)
        except:
            pass


    def ipSel(self,i):
        try:
            tempIndex= (self.comboBox_audio_in.currentText()).split(".")
            global INPUT_DEVICE_IND
            INPUT_DEVICE_IND=int(tempIndex[0])
            print(f"IP Dev Index: {INPUT_DEVICE_IND}")
            global IpDevCurrentInd
            IpDevCurrentInd=i
        except:
            pass


    def opSel(self,i):
        try:
            tempIndex= (self.comboBox_audio_out.currentText()).split(".")
            global OUTPUT_DEVICE_IND
            OUTPUT_DEVICE_IND=int(tempIndex[0])
            print(f"OP Dev Index: {OUTPUT_DEVICE_IND}")
            global OpDevCurrentInd
            OpDevCurrentInd=i
        except:
            pass
        

class Ui_DialogRecAudio(QtWidgets.QDialog):
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("DialogRecAudio")
        Dialog.resize(331, 380)
        Dialog.setWindowIcon(QtGui.QIcon('appRes/mic.png'))
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Dialog.setFixedSize(Dialog.size())
        self.updateThresholdBtn = QtWidgets.QPushButton(Dialog)
        self.updateThresholdBtn.setGeometry(QtCore.QRect(180, 60, 101, 23))
        self.updateThresholdBtn.setObjectName("updateThresholdBtn")
        QtWidgets.QToolTip.setFont(QtGui.QFont('SansSerif', 8))
        self.inputThreshold = QtWidgets.QLineEdit(Dialog)
        self.inputThreshold.setToolTip('Only accepts 0000-9999 range')
        self.inputThreshold.setGeometry(QtCore.QRect(180, 30, 113, 20))
        self.inputThreshold.setObjectName("inputThreshold")
        self.inputThreshold.textChanged.connect(self.thresholdUpdated)
        self.audioThreshValues = QtWidgets.QPlainTextEdit(Dialog)
        self.audioThreshValues.setGeometry(QtCore.QRect(20, 130, 271, 221))
        self.audioThreshValues.setObjectName("audioThreshValues")
        self.label_at = QtWidgets.QLabel(Dialog)
        self.label_at.setGeometry(QtCore.QRect(20, 110, 121, 16))
        self.label_at.setObjectName("label_at")
        self.recordAudioBtn = QtWidgets.QPushButton(Dialog)
        self.recordAudioBtn.setGeometry(QtCore.QRect(20, 60, 100, 23))
        self.recordAudioBtn.setObjectName("recordAudioBtn")
        self.recordAudioBtn.setEnabled(False)
        self.TestName = QtWidgets.QLineEdit(Dialog)
        self.TestName.setGeometry(QtCore.QRect(20, 30, 113, 20))
        self.TestName.setObjectName("TestName")
        self.TestName.textChanged.connect(self.TestNameChanged)
        self.label_tn = QtWidgets.QLabel(Dialog)
        self.label_tn.setGeometry(QtCore.QRect(20, 10, 50, 13))
        self.label_tn.setObjectName("label_tn")
        self.label_thres = QtWidgets.QLabel(Dialog)
        self.label_thres.setGeometry(QtCore.QRect(180, 10, 50, 13))
        self.label_thres.setObjectName("label_thres")

        self.retranslateUi(Dialog)

        self.inputThreshold.setInputMask("9999")
        self.updateThresholdBtn.clicked.connect(self.updateThresholdBtnCLicked)
        self.recordAudioBtn.clicked.connect(self.recordBtnClicked)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Record Audio"))
        self.updateThresholdBtn.setText(_translate("Dialog", "Update Threshold"))
        self.inputThreshold.setText(_translate("Dialog", str(THRESHOLD)))
        self.label_at.setText(_translate("Dialog", "Audio Threshold Values:"))
        self.recordAudioBtn.setText(_translate("Dialog", "Record"))
        self.label_tn.setText(_translate("Dialog", "Test Name"))
        self.label_thres.setText(_translate("Dialog", "Threshold"))
        self.TestName.setFocus()

    def thresholdUpdated(self):
        self.updateThresholdBtn.setText("Update Threshold")
    
    def closeEvent(self, evnt):
        if recordRunning==True:
            close = QtWidgets.QMessageBox.question(self,"Confirmation","Are you sure you want to stop recording?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if close == QtWidgets.QMessageBox.Yes:
                super(Ui_DialogRecAudio, self).closeEvent(evnt)
                self.newThread.stop()
            else:
                evnt.ignore()
        else:
            super(Ui_DialogRecAudio, self).closeEvent(evnt)
    
    def updateThresholdBtnCLicked(self):
        if self.inputThreshold.text():
            th=self.inputThreshold.text()
            global THRESHOLD
            THRESHOLD=int(th)
            print(THRESHOLD)
            self.updateThresholdBtn.setText("Updated")
    
    def TestNameChanged(self):
        if len(self.TestName.text())==0:
            self.recordAudioBtn.setEnabled(False)
        else:
            self.recordAudioBtn.setEnabled(True)
    
    def recordBtnClicked(self):
        if Ui_DialogPlayInstruction().exec_()!=2:
            testname=self.TestName.text()
            self.newThread = SpeechWorker(testname)
            self.newThread.signal.connect(self.updateThreshUI)
            self.recordAudioBtn.setEnabled(False)
            self.TestName.setEnabled(False)
            self.recordAudioBtn.setText("Listening..")
            self.newThread.start()

            
    def updateThreshUI(self, result):
        if result!="#end" and result!="#record_end":
          self.audioThreshValues.appendPlainText(result)
        elif result=="#record_end":
            self.recordAudioBtn.setText("Extracting..")
        elif result=="#end":
            self.recordAudioBtn.setText("Record")
            self.recordAudioBtn.setEnabled(True)
            self.TestName.setEnabled(True)


class Ui_DialogMgRepViewer(QtWidgets.QDialog):
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(708, 566)
        Dialog.setWindowIcon(QtGui.QIcon('appRes/logo.ico'))
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Dialog.setFixedSize(Dialog.size())
        self.MgCgTnList = QtWidgets.QListWidget(Dialog)
        self.MgCgTnList.setGeometry(QtCore.QRect(358, 313, 331, 211))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.MgCgTnList.setFont(font)
        self.MgCgTnList.setObjectName("MgCgTnList")
        self.mgviewResPD = QtWidgets.QPushButton(Dialog)
        self.mgviewResPD.setGeometry(QtCore.QRect(500, 251, 90, 23))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.mgviewResPD.setFont(font)
        self.mgviewResPD.setObjectName("mgviewResPD")
        self.label_MgPdTn = QtWidgets.QLabel(Dialog)
        self.label_MgPdTn.setGeometry(QtCore.QRect(358, 14, 231, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_MgPdTn.setFont(font)
        self.label_MgPdTn.setObjectName("label_MgPdTn")
        self.label_MgCgTn = QtWidgets.QLabel(Dialog)
        self.label_MgCgTn.setGeometry(QtCore.QRect(358, 291, 231, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_MgCgTn.setFont(font)
        self.label_MgCgTn.setObjectName("label_MgCgTn")
        self.mgviewResCG = QtWidgets.QPushButton(Dialog)
        self.mgviewResCG.setGeometry(QtCore.QRect(500, 530, 90, 23))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.mgviewResCG.setFont(font)
        self.mgviewResCG.setObjectName("mgviewResCG")
        self.MgPdTnList = QtWidgets.QListWidget(Dialog)
        self.MgPdTnList.setGeometry(QtCore.QRect(358, 33, 331, 211))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.MgPdTnList.setFont(font)
        self.MgPdTnList.setObjectName("MgPdTnList")
        self.MgPdRecTypeList = QtWidgets.QListWidget(Dialog)
        self.MgPdRecTypeList.setGeometry(QtCore.QRect(20, 33, 251, 211))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.MgPdRecTypeList.setFont(font)
        self.MgPdRecTypeList.setObjectName("MgPdRecTypeList")
        self.MgCgRecTypeList = QtWidgets.QListWidget(Dialog)
        self.MgCgRecTypeList.setGeometry(QtCore.QRect(20, 313, 251, 211))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.MgCgRecTypeList.setFont(font)
        self.MgCgRecTypeList.setObjectName("MgCgRecTypeList")
        self.viewMgPdTnBtn = QtWidgets.QPushButton(Dialog)
        self.viewMgPdTnBtn.setGeometry(QtCore.QRect(282, 117, 65, 51))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.viewMgPdTnBtn.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("appRes/right.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.viewMgPdTnBtn.setIcon(icon)
        self.viewMgPdTnBtn.setObjectName("viewMgPdTnBtn")
        self.viewMgCgTnBtn = QtWidgets.QPushButton(Dialog)
        self.viewMgCgTnBtn.setGeometry(QtCore.QRect(282, 397, 65, 51))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.viewMgCgTnBtn.setFont(font)
        self.viewMgCgTnBtn.setIcon(icon)
        self.viewMgCgTnBtn.setObjectName("viewMgCgTnBtn")
        self.label_MgPdTt = QtWidgets.QLabel(Dialog)
        self.label_MgPdTt.setGeometry(QtCore.QRect(20, 13, 241, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_MgPdTt.setFont(font)
        self.label_MgPdTt.setObjectName("label_MgPdTt")
        self.label_MgCgTt = QtWidgets.QLabel(Dialog)
        self.label_MgCgTt.setGeometry(QtCore.QRect(20, 290, 231, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_MgCgTt.setFont(font)
        self.label_MgCgTt.setObjectName("label_MgCgTt")

        self.retranslateUi(Dialog)
        self.MgPdRecTypeList.addItems(mgtesttypesPD)
        self.MgCgRecTypeList.addItems(mgtesttypesCG)
        self.viewMgPdTnBtn.clicked.connect(self.onClickedViewMgPdTnBtn)
        self.viewMgCgTnBtn.clicked.connect(self.onClickedViewMgCgTnBtn)
        self.mgviewResCG.clicked.connect(self.onClickedViewResCG)
        self.mgviewResPD.clicked.connect(self.onClickedViewResPD)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MG Report Viewer"))
        self.mgviewResPD.setText(_translate("Dialog", "View Result.."))
        self.label_MgPdTn.setText(_translate("Dialog", "PD Testnames of Selected Record:"))
        self.label_MgCgTn.setText(_translate("Dialog", "CG Testnames of Selected Record:"))
        self.mgviewResCG.setText(_translate("Dialog", "View Result.."))
        self.viewMgPdTnBtn.setText(_translate("Dialog", "View\nTests"))
        self.viewMgCgTnBtn.setText(_translate("Dialog", "View\nTests"))
        self.label_MgPdTt.setText(_translate("Dialog", "PD Test-types of Selected Record:"))
        self.label_MgCgTt.setText(_translate("Dialog", "CG Test-types of Selected Record:"))

    def onClickedViewMgPdTnBtn(self):
        if self.MgPdRecTypeList.selectedItems():
            self.MgPdTnList.clear()
            pathTemp=self.MgPdRecTypeList.currentItem().text()
            newPathTemp=path+'/MG_Data/PD/'+pathTemp
            print(f"{newPathTemp} clicked")
            fpdCount=0
            for _, _, filenames in os.walk(newPathTemp):
                if not len(filenames)==0:
                    print(filenames)
                    fpdCount+=len(filenames)
                    for i in filenames:
                        if i[len(i)-3:len(i)]=='log':
                            self.MgPdTnList.addItem(i[0:len(i)-4])
                            print(i[0:len(i)-4])
            
            if fpdCount==0:
                QtWidgets.QMessageBox.information(self,"Information","No tests found.\nTry refreshing via \"Get Report\" in the home page!", QtWidgets.QMessageBox.Ok)
        else:
           QtWidgets.QMessageBox.information(self,"Information","Nothing Selected!", QtWidgets.QMessageBox.Ok)


    def onClickedViewMgCgTnBtn(self):
        if self.MgCgRecTypeList.selectedItems():
            self.MgCgTnList.clear()
            pathTemp=self.MgCgRecTypeList.currentItem().text()
            newPathTemp=path+'/MG_Data/CG/'+pathTemp
            print(f"{newPathTemp} clicked")
            fcgCount=0
            for _, _, filenames in os.walk(newPathTemp):
                if not len(filenames)==0:
                    print(filenames)
                    fcgCount+=len(filenames)
                    for i in filenames:
                        if i[len(i)-3:len(i)]=='log':
                            self.MgCgTnList.addItem(i[0:len(i)-4])
                            print(i[0:len(i)-4])
            if fcgCount==0:
                QtWidgets.QMessageBox.information(self,"Information","No tests found.\nTry refreshing via \"Get Report\" in the home page!", QtWidgets.QMessageBox.Ok)
        else:
           QtWidgets.QMessageBox.information(self,"Information","Nothing Selected!", QtWidgets.QMessageBox.Ok)

    def onClickedViewResCG(self):
        if self.MgCgTnList.selectedItems():
            searchFileRoot=""
            newPathTemp=path+'/MG_Data/CG'
            search=self.MgCgTnList.currentItem().text()
            searchFn=search+".log"
            for root, _, filenames in os.walk(newPathTemp):
                for i in filenames:
                    if i==searchFn:
                        searchFileRoot=root
            print(searchFileRoot)
            accessError=False
            notOtherData=True
            for root, _, filenames in os.walk(searchFileRoot):
                for i in filenames:
                    notOtherData=True
                    fnName=(i.split('.'))[0]
                    try:
                        print(f"\n fnName: {fnName[len(fnName)-(len(search)-21):len(fnName)]}\nSearch: {search[21:len(search)]}\n")
                        if fnName[len(fnName)-(len(search)-21):len(fnName)]==search[21:len(search)]:
                            notOtherData=False
                    except:
                        accessError=True
                        pass
                    if notOtherData==False:
                        try:
                            if i[len(i)-3:len(i)]=='log':
                                subprocess.Popen(["notepad.exe", root+"/"+i])
                            else:
                                os.startfile(root+"/"+i)
                        except:
                            accessError==True
                            pass
                    if accessError==True:
                        QtWidgets.QMessageBox.warning(self,"Warning","Some files could not be opened!\nMake sure they aren't opened elsewhere.", QtWidgets.QMessageBox.Ok)
    
            try:
                coord=searchFileRoot+"/Coordinate Data Time"+search[21:len(search)]+".csv"
                press=searchFileRoot+"/Pressure Data Time"+search[21:len(search)]+".csv"
                self.plotViewer(coord,press,search) 
            except Exception as e:
                print(f"File Access Error: {e}")
                QtWidgets.QMessageBox.warning(self,"Warning","Some files could not be opened!\nMake sure they aren't opened elsewhere.", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(self,"Information","Nothing Selected!", QtWidgets.QMessageBox.Ok)


    def onClickedViewResPD(self):
        if self.MgPdTnList.selectedItems():
            searchFileRoot=""
            newPathTemp=path+'/MG_Data/PD'
            search=self.MgPdTnList.currentItem().text()
            searchFn=search+".log"
            for root, _, filenames in os.walk(newPathTemp):
                for i in filenames:
                    if i==searchFn:
                        searchFileRoot=root
            print(searchFileRoot)
            accessError=False
            notOtherData=True
            for root, _, filenames in os.walk(searchFileRoot):
                for i in filenames:
                    notOtherData=True
                    fnName=(i.split('.'))[0]
                    try:
                        print(f"\n fnName: {fnName[len(fnName)-(len(search)-21):len(fnName)]}\nSearch: {search[21:len(search)]}\n")
                        if fnName[len(fnName)-(len(search)-21):len(fnName)]==search[21:len(search)]:
                            notOtherData=False
                    except:
                        accessError=True
                        pass
                    if notOtherData==False:
                        try:
                            if i[len(i)-3:len(i)]=='log':
                                subprocess.Popen(["notepad.exe", root+"/"+i])
                            else:
                                os.startfile(root+"/"+i)
                        except:
                            accessError==True
                            pass
                    if accessError==True:
                        QtWidgets.QMessageBox.warning(self,"Warning","Some files could not be opened!\nMake sure they aren't opened elsewhere.", QtWidgets.QMessageBox.Ok)
    
            try:
                coord=searchFileRoot+"/Coordinate Data Time"+search[21:len(search)]+".csv"
                press=searchFileRoot+"/Pressure Data Time"+search[21:len(search)]+".csv"
                self.plotViewer(coord,press,search) 
            except Exception as e:
                print(f"File Access Error: {e}")
                QtWidgets.QMessageBox.warning(self,"Warning","Some files could not be opened!\nMake sure they aren't opened elsewhere.", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(self,"Information","Nothing Selected!", QtWidgets.QMessageBox.Ok)


    def plotViewer(self,coord,press,name):
        x=[]
        y=[]
        xp=[]
        with open(coord,'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                x.append(int(row[0]))
                y.append(int(row[1]))

        with open(press,'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                xp.append(int(row[0]))

        plt.figure(num=name)
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

        plt.subplot(2,1,2)
        plt.plot(xp, label='xy plot')
        plt.xlabel('Coordinate plot pressure points (x)')
        plt.ylabel('Pressure (y)')
        plt.title('Presssure data 2D plot')
        plt.legend()
        plt.tight_layout(pad=0.4)

        mng=plt.get_current_fig_manager()
        mng.window.state("zoomed")
        mplcursors.cursor(hover=True)

        plt.draw()
        plt.show()

class Ui_DialogSpeechRepViewer(QtWidgets.QDialog):
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(678, 564)
        Dialog.setWindowIcon(QtGui.QIcon('appRes/mic.png'))
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Dialog.setFixedSize(Dialog.size())
        self.SpCgRecList = QtWidgets.QListWidget(Dialog)
        self.SpCgRecList.setGeometry(QtCore.QRect(20, 310, 281, 211))
        self.SpCgRecList.setObjectName("SpCgRecList")
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.SpCgRecList.setFont(font)
        self.viewSpPdTnBtn = QtWidgets.QPushButton(Dialog)
        self.viewSpPdTnBtn.setGeometry(QtCore.QRect(303, 110, 65, 51))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.viewSpPdTnBtn.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("appRes/right.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.viewSpPdTnBtn.setIcon(icon)
        self.viewSpPdTnBtn.setObjectName("viewSpPdTnBtn")
        self.label_SpPdRep = QtWidgets.QLabel(Dialog)
        self.label_SpPdRep.setGeometry(QtCore.QRect(20, 10, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_SpPdRep.setFont(font)
        self.label_SpPdRep.setObjectName("label_SpPdRep")
        self.label_SpCgRep = QtWidgets.QLabel(Dialog)
        self.label_SpCgRep.setGeometry(QtCore.QRect(20, 290, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_SpCgRep.setFont(font)
        self.label_SpCgRep.setObjectName("label_SpCgRep")
        self.viewSpCgTnBtn = QtWidgets.QPushButton(Dialog)
        self.viewSpCgTnBtn.setGeometry(QtCore.QRect(303, 393, 65, 51))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.viewSpCgTnBtn.setFont(font)
        self.viewSpCgTnBtn.setIcon(icon)
        self.viewSpCgTnBtn.setObjectName("viewSpCgTnBtn")
        self.SpPdRecList = QtWidgets.QListWidget(Dialog)
        self.SpPdRecList.setGeometry(QtCore.QRect(20, 30, 281, 211))
        self.SpPdRecList.setObjectName("SpPdRecList")
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.SpPdRecList.setFont(font)
        self.SpPdTnList = QtWidgets.QListWidget(Dialog)
        self.SpPdTnList.setGeometry(QtCore.QRect(370, 30, 281, 211))
        self.SpPdTnList.setObjectName("SpPdTnList")
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.SpPdTnList.setFont(font)
        self.SpCgTnList = QtWidgets.QListWidget(Dialog)
        self.SpCgTnList.setGeometry(QtCore.QRect(370, 310, 281, 211))
        self.SpCgTnList.setObjectName("SpCgTnList")
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.SpCgTnList.setFont(font)
        self.label_SpPdTn = QtWidgets.QLabel(Dialog)
        self.label_SpPdTn.setGeometry(QtCore.QRect(370, 10, 500, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_SpPdTn.setFont(font)
        self.label_SpPdTn.setObjectName("label_SpPdTn")
        self.label_SpCgTn = QtWidgets.QLabel(Dialog)
        self.label_SpCgTn.setGeometry(QtCore.QRect(370, 290, 500, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_SpCgTn.setFont(font)
        self.label_SpCgTn.setObjectName("label_SpCgTn")
        self.viewResPD = QtWidgets.QPushButton(Dialog)
        self.viewResPD.setGeometry(QtCore.QRect(562, 250, 90, 23))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.viewResPD.setFont(font)
        self.viewResPD.setObjectName("viewResPD")
        self.viewResCG = QtWidgets.QPushButton(Dialog)
        self.viewResCG.setGeometry(QtCore.QRect(563, 530, 90, 23))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.viewResCG.setFont(font)
        self.viewResCG.setObjectName("viewResCG")

        self.retranslateUi(Dialog)

        self.SpPdRecList.addItems(sprecNamesPD)
        self.SpCgRecList.addItems(sprecNamesCG)
        self.viewSpPdTnBtn.clicked.connect(self.onClickedViewSpPdTnBtn)
        self.viewSpCgTnBtn.clicked.connect(self.onClickedViewSpCgTnBtn)
        self.viewResPD.clicked.connect(self.onClickedViewResPD)
        self.viewResCG.clicked.connect(self.onClickedViewResCG)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Speech Report Viewer"))
        self.viewSpPdTnBtn.setText(_translate("Dialog", "View\nTests"))
        self.label_SpPdRep.setText(_translate("Dialog", "PD Records:"))
        self.label_SpCgRep.setText(_translate("Dialog", "CG Records:"))
        self.viewSpCgTnBtn.setText(_translate("Dialog", "View\nTests"))
        self.label_SpPdTn.setText(_translate("Dialog", "PD Testnames of Selected Record:"))
        self.label_SpCgTn.setText(_translate("Dialog", "CG Testnames of Selected Record:"))
        self.viewResPD.setText(_translate("Dialog", "View Result.."))
        self.viewResCG.setText(_translate("Dialog", "View Result.."))

    def onClickedViewSpPdTnBtn(self):
        if self.SpPdRecList.selectedItems():
            self.SpPdTnList.clear()
            pathTemp=self.SpPdRecList.currentItem().text()
            newPathTemp=path+'/Speech_Data/PD/'+pathTemp
            print(f"{newPathTemp} clicked")
            fpdCount=0
            for _, _, filenames in os.walk(newPathTemp):
                if not len(filenames)==0:
                    print(filenames)
                    fpdCount+=len(filenames)
                    for i in filenames:
                        if i[len(i)-3:len(i)]=='wav':
                            self.SpPdTnList.addItem(i[0:len(i)-4])
                            print(i[0:len(i)-4])
            
            if fpdCount==0:
                QtWidgets.QMessageBox.information(self,"Information","No tests found.\nTry refreshing via \"Get Report\" in the home page!", QtWidgets.QMessageBox.Ok)
        else:
           QtWidgets.QMessageBox.information(self,"Information","Nothing Selected!", QtWidgets.QMessageBox.Ok)

    def onClickedViewSpCgTnBtn(self):
        if self.SpCgRecList.selectedItems():
            self.SpCgTnList.clear()
            pathTemp=self.SpCgRecList.currentItem().text()
            newPathTemp=path+'/Speech_Data/CG/'+pathTemp
            print(f"{newPathTemp} clicked")
            fcgCount=0
            for _, _, filenames in os.walk(newPathTemp):
                if not len(filenames)==0:
                    print(filenames)
                    fcgCount+=len(filenames)
                    for i in filenames:
                        if i[len(i)-3:len(i)]=='wav':
                            self.SpCgTnList.addItem(i[0:len(i)-4])
                            print(i[0:len(i)-4])
            if fcgCount==0:
                QtWidgets.QMessageBox.information(self,"Information","No tests found.\nTry refreshing via \"Get Report\" in the home page!", QtWidgets.QMessageBox.Ok)
        else:
           QtWidgets.QMessageBox.information(self,"Information","Nothing Selected!", QtWidgets.QMessageBox.Ok)

    def onClickedViewResCG(self):
        if self.SpCgTnList.selectedItems():
            searchFileRoot=""
            newPathTemp=path+'/Speech_Data/CG'
            search=self.SpCgTnList.currentItem().text()
            searchFn=search+".wav"
            for root, _, filenames in os.walk(newPathTemp):
                for i in filenames:
                    if i==searchFn:
                        searchFileRoot=root
            print(searchFileRoot)
            accessError=False
            notOtherData=True
            for root, _, filenames in os.walk(searchFileRoot):
                for i in filenames:
                    notOtherData=True
                    fnName=(i.split('.'))[0]
                    try:
                        if fnName[len(fnName)-len(search):len(fnName)]==search:
                            notOtherData=False
                    except:
                        accessError=True
                        pass
                    if i!=searchFn and i[len(i)-3:len(i)]!='wav' and notOtherData==False:
                        try:
                            subprocess.Popen(["notepad.exe", root+"/"+i])
                        except:
                            pass
                    if accessError==True:
                        QtWidgets.QMessageBox.warning(self,"Warning","Some files could not be opened!\nMake sure they aren't opened elsewhere.", QtWidgets.QMessageBox.Ok)
            
            try:
                snd = parselmouth.Sound(searchFileRoot+"\\"+searchFn)
                self.plotViewer(snd,search)
            except:
                print("File Access Error")
                QtWidgets.QMessageBox.warning(self,"Warning","Some files could not be opened!\nMake sure they aren't opened elsewhere.", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(self,"Information","Nothing Selected!", QtWidgets.QMessageBox.Ok)


    def onClickedViewResPD(self):
        if self.SpPdTnList.selectedItems():
            searchFileRoot=""
            newPathTemp=path+'/Speech_Data/PD'
            search=self.SpPdTnList.currentItem().text()
            searchFn=search+".wav"
            for root, _, filenames in os.walk(newPathTemp):
                for i in filenames:
                    if i==searchFn:
                        searchFileRoot=root
            print(searchFileRoot)
            accessError=False
            notOtherData=True
            for root, _, filenames in os.walk(searchFileRoot):
                for i in filenames:
                    notOtherData=True
                    fnName=(i.split('.'))[0]
                    try:
                        if fnName[len(fnName)-len(search):len(fnName)]==search:
                            notOtherData=False
                    except:
                        accessError=True
                        pass
                    if i!=searchFn and i[len(i)-3:len(i)]!='wav' and notOtherData==False:
                        try:
                            subprocess.Popen(["notepad.exe", root+"/"+i])
                        except:
                            pass
                    if accessError==True:
                        QtWidgets.QMessageBox.warning(self,"Warning","Some files could not be opened!\nMake sure they aren't opened elsewhere.", QtWidgets.QMessageBox.Ok)
            
            try:
                snd = parselmouth.Sound(searchFileRoot+"\\"+searchFn)
                self.plotViewer(snd,search)
            except:
                print("File Access Error")
                QtWidgets.QMessageBox.warning(self,"Warning","Some files could not be opened!\nMake sure they aren't opened elsewhere.", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(self,"Information","Nothing Selected!", QtWidgets.QMessageBox.Ok)

    def plotViewer(self,snd,search):
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
        plt.figure(num=search) 
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
        plt.draw()
        plt.show()

            



class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
      super().__init__()
      self.setupUi(MainWindow)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 552)
        MainWindow.setWindowIcon(QtGui.QIcon('appRes/logo.ico'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(2, 20, 16, 101))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(11, 20, 10, 3))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(10, 120, 250, 3))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(27, 12, 81, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(110, 20, 151, 3))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(253, 20, 16, 101))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(11, 140, 10, 3))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(26, 132, 85, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setGeometry(QtCore.QRect(114, 140, 145, 3))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.line_8 = QtWidgets.QFrame(self.centralwidget)
        self.line_8.setGeometry(QtCore.QRect(252, 140, 16, 88))
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.line_9 = QtWidgets.QFrame(self.centralwidget)
        self.line_9.setGeometry(QtCore.QRect(2, 140, 16, 88))
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.line_10 = QtWidgets.QFrame(self.centralwidget)
        self.line_10.setGeometry(QtCore.QRect(10, 228, 250, 3))
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.line_11 = QtWidgets.QFrame(self.centralwidget)
        self.line_11.setGeometry(QtCore.QRect(2, 240, 16, 260))
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.line_12 = QtWidgets.QFrame(self.centralwidget)
        self.line_12.setGeometry(QtCore.QRect(252, 240, 16, 260))
        self.line_12.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.line_13 = QtWidgets.QFrame(self.centralwidget)
        self.line_13.setGeometry(QtCore.QRect(123, 240, 137, 3))
        self.line_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.line_14 = QtWidgets.QFrame(self.centralwidget)
        self.line_14.setGeometry(QtCore.QRect(11, 240, 10, 3))
        self.line_14.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(26, 232, 101, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.line_15 = QtWidgets.QFrame(self.centralwidget)
        self.line_15.setGeometry(QtCore.QRect(10, 500, 250, 3))
        self.line_15.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        self.line_16 = QtWidgets.QFrame(self.centralwidget)
        self.line_16.setGeometry(QtCore.QRect(12, 270, 16, 90))
        self.line_16.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_16.setObjectName("line_16")
        self.line_17 = QtWidgets.QFrame(self.centralwidget)
        self.line_17.setGeometry(QtCore.QRect(240, 270, 16, 90))
        self.line_17.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_17.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_17.setObjectName("line_17")
        self.line_18 = QtWidgets.QFrame(self.centralwidget)
        self.line_18.setGeometry(QtCore.QRect(104, 270, 143, 3))
        self.line_18.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_18.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_18.setObjectName("line_18")
        self.line_19 = QtWidgets.QFrame(self.centralwidget)
        self.line_19.setGeometry(QtCore.QRect(21, 270, 10, 3))
        self.line_19.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_19.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_19.setObjectName("line_19")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(36, 262, 65, 13))
        self.label_4.setObjectName("label_4")
        self.line_20 = QtWidgets.QFrame(self.centralwidget)
        self.line_20.setGeometry(QtCore.QRect(20, 360, 228, 3))
        self.line_20.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_20.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_20.setObjectName("line_20")
        self.line_21 = QtWidgets.QFrame(self.centralwidget)
        self.line_21.setGeometry(QtCore.QRect(19, 390, 10, 3))
        self.line_21.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_21.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_21.setObjectName("line_21")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(36, 382, 35, 13))
        self.label_5.setObjectName("label_5")
        self.line_22 = QtWidgets.QFrame(self.centralwidget)
        self.line_22.setGeometry(QtCore.QRect(240, 390, 16, 90))
        self.line_22.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_22.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_22.setObjectName("line_22")
        self.line_23 = QtWidgets.QFrame(self.centralwidget)
        self.line_23.setGeometry(QtCore.QRect(75, 390, 172, 3))
        self.line_23.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_23.setObjectName("line_23")
        self.line_24 = QtWidgets.QFrame(self.centralwidget)
        self.line_24.setGeometry(QtCore.QRect(20, 480, 228, 3))
        self.line_24.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_24.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_24.setObjectName("line_24")
        self.line_25 = QtWidgets.QFrame(self.centralwidget)
        self.line_25.setGeometry(QtCore.QRect(12, 390, 16, 90))
        self.line_25.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_25.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_25.setObjectName("line_25")
        self.line_26 = QtWidgets.QFrame(self.centralwidget)
        self.line_26.setGeometry(QtCore.QRect(330, 270, 16, 210))
        self.line_26.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_26.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_26.setObjectName("line_26")
        self.line_27 = QtWidgets.QFrame(self.centralwidget)
        self.line_27.setGeometry(QtCore.QRect(388, 20, 240, 3))
        self.line_27.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_27.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_27.setObjectName("line_27")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(355, 262, 35, 13))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(345, 12, 41, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.line_28 = QtWidgets.QFrame(self.centralwidget)
        self.line_28.setGeometry(QtCore.QRect(610, 50, 16, 200))
        self.line_28.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_28.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_28.setObjectName("line_28")
        self.line_29 = QtWidgets.QFrame(self.centralwidget)
        self.line_29.setGeometry(QtCore.QRect(395, 270, 222, 3))
        self.line_29.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_29.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_29.setObjectName("line_29")
        self.line_30 = QtWidgets.QFrame(self.centralwidget)
        self.line_30.setGeometry(QtCore.QRect(328, 500, 300, 3))
        self.line_30.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_30.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_30.setObjectName("line_30")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(355, 42, 65, 13))
        self.label_8.setObjectName("label_8")
        self.line_31 = QtWidgets.QFrame(self.centralwidget)
        self.line_31.setGeometry(QtCore.QRect(338, 250, 280, 3))
        self.line_31.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_31.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_31.setObjectName("line_31")
        self.line_32 = QtWidgets.QFrame(self.centralwidget)
        self.line_32.setGeometry(QtCore.QRect(620, 20, 16, 480))
        self.line_32.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_32.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_32.setObjectName("line_32")
        self.line_33 = QtWidgets.QFrame(self.centralwidget)
        self.line_33.setGeometry(QtCore.QRect(610, 270, 16, 210))
        self.line_33.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_33.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_33.setObjectName("line_33")
        self.line_34 = QtWidgets.QFrame(self.centralwidget)
        self.line_34.setGeometry(QtCore.QRect(420, 50, 198, 3))
        self.line_34.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_34.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_34.setObjectName("line_34")
        self.line_35 = QtWidgets.QFrame(self.centralwidget)
        self.line_35.setGeometry(QtCore.QRect(339, 270, 10, 3))
        self.line_35.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_35.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_35.setObjectName("line_35")
        self.line_36 = QtWidgets.QFrame(self.centralwidget)
        self.line_36.setGeometry(QtCore.QRect(330, 50, 16, 200))
        self.line_36.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_36.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_36.setObjectName("line_36")
        self.line_37 = QtWidgets.QFrame(self.centralwidget)
        self.line_37.setGeometry(QtCore.QRect(329, 20, 10, 3))
        self.line_37.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_37.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_37.setObjectName("line_37")
        self.line_38 = QtWidgets.QFrame(self.centralwidget)
        self.line_38.setGeometry(QtCore.QRect(339, 50, 10, 3))
        self.line_38.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_38.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_38.setObjectName("line_38")
        self.line_39 = QtWidgets.QFrame(self.centralwidget)
        self.line_39.setGeometry(QtCore.QRect(320, 20, 16, 480))
        self.line_39.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_39.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_39.setObjectName("line_39")
        self.line_40 = QtWidgets.QFrame(self.centralwidget)
        self.line_40.setGeometry(QtCore.QRect(338, 480, 280, 3))
        self.line_40.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_40.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_40.setObjectName("line_40")
        self.recordMG = QtWidgets.QPushButton(self.centralwidget)
        self.recordMG.setGeometry(QtCore.QRect(30, 280, 75, 23))
        self.recordMG.setObjectName("recordMG")
        self.recordMG.setEnabled(False)
        self.radioControl = QtWidgets.QRadioButton(self.centralwidget)
        self.radioControl.setGeometry(QtCore.QRect(30, 310, 61, 17))
        self.radioControl.setObjectName("radioControl")
        self.radioControl.toggled.connect(self.onClickedControl)
        self.radioControl.toggled.connect(lambda:self.btnstate(self.radioControl))
        self.radioParkinson = QtWidgets.QRadioButton(self.centralwidget)
        self.radioParkinson.setGeometry(QtCore.QRect(90, 310, 82, 17))
        self.radioParkinson.toggled.connect(self.onClickedParkinson)
        self.radioParkinson.toggled.connect(lambda:self.btnstate(self.radioParkinson))
        self.radioParkinson.setObjectName("radioParkinson")
        self.ProjName = QtWidgets.QLabel(self.centralwidget)
        self.ProjName.setGeometry(QtCore.QRect(20, 160, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setItalic(True)
        self.ProjName.setFont(font)
        self.ProjName.setFrameShape(QtWidgets.QFrame.Box)
        self.ProjName.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ProjName.setLineWidth(1)
        self.ProjName.setText("")
        self.ProjName.setAlignment(QtCore.Qt.AlignCenter)
        # self.ProjName.setAlignment(QtCore.Qt.AlignLeft)
        self.ProjName.setWordWrap(True)
        self.ProjName.setObjectName("ProjName")
        self.WacExtStatus = QtWidgets.QLabel(self.centralwidget)
        self.WacExtStatus.setGeometry(QtCore.QRect(30, 330, 208, 20))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.WacExtStatus.setFont(font)
        self.WacExtStatus.setFrameShape(QtWidgets.QFrame.Box)
        self.WacExtStatus.setFrameShadow(QtWidgets.QFrame.Raised)
        self.WacExtStatus.setLineWidth(1)
        self.WacExtStatus.setText("")
        self.WacExtStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.WacExtStatus.setWordWrap(True)
        self.WacExtStatus.setObjectName("WacExtStatus")
        self.recordSpeech = QtWidgets.QPushButton(self.centralwidget)
        self.recordSpeech.setGeometry(QtCore.QRect(30, 400, 75, 23))
        self.recordSpeech.setObjectName("recordSpeech")
        self.radioControl2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioControl2.setGeometry(QtCore.QRect(30, 440, 61, 17))
        self.radioControl2.setObjectName("radioControl2")
        self.radioControl2.toggled.connect(lambda:self.btnstate2(self.radioControl2))
        self.radioParkinson2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioParkinson2.setGeometry(QtCore.QRect(90, 440, 82, 17))
        self.radioParkinson2.setObjectName("radioParkinson2")
        self.radioParkinson2.toggled.connect(lambda:self.btnstate2(self.radioParkinson2))
        self.TestNameCombo = QtWidgets.QComboBox(self.centralwidget)
        self.TestNameCombo.setGeometry(QtCore.QRect(115, 280, 122, 23))
        self.TestNameCombo.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        self.TestNameCombo.setFont(font)
        self.TestNameCombo.setObjectName("TestNameCombo")
        self.spRepMainWin = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.spRepMainWin.setGeometry(QtCore.QRect(350, 330, 251, 91))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.spRepMainWin.setFont(font)
        self.spRepMainWin.setFrameShape(QtWidgets.QFrame.Box)
        self.spRepMainWin.setFrameShadow(QtWidgets.QFrame.Raised)
        self.spRepMainWin.setPlainText("")
        self.spRepMainWin.setObjectName("spRepMainWin")
        self.spRepMainWin.setReadOnly(True)
        self.labelSpRep = QtWidgets.QLabel(self.centralwidget)
        self.labelSpRep.setGeometry(QtCore.QRect(350, 300, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelSpRep.setFont(font)
        self.labelSpRep.setObjectName("labelSpRep")
        self.spViewMoreBtn = QtWidgets.QPushButton(self.centralwidget)
        self.spViewMoreBtn.setGeometry(QtCore.QRect(520, 440, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.spViewMoreBtn.setFont(font)
        self.spViewMoreBtn.setObjectName("spViewMoreBtn")
        self.getSpRepBtn = QtWidgets.QPushButton(self.centralwidget)
        self.getSpRepBtn.setGeometry(QtCore.QRect(512, 280, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.getSpRepBtn.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("appRes/refresh.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.getSpRepBtn.setIcon(icon)
        self.getSpRepBtn.setObjectName("getSpRepBtn")
        self.mgViewMoreBtn = QtWidgets.QPushButton(self.centralwidget)
        self.mgViewMoreBtn.setGeometry(QtCore.QRect(520, 220, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.mgViewMoreBtn.setFont(font)
        self.mgViewMoreBtn.setObjectName("mgViewMoreBtn")
        self.getMgRepBtn = QtWidgets.QPushButton(self.centralwidget)
        self.getMgRepBtn.setGeometry(QtCore.QRect(512, 60, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(True)
        font.setWeight(75)
        self.getMgRepBtn.setFont(font)
        self.getMgRepBtn.setIcon(icon)
        self.getMgRepBtn.setObjectName("getMgRepBtn")
        self.labelMgRep = QtWidgets.QLabel(self.centralwidget)
        self.labelMgRep.setGeometry(QtCore.QRect(350, 80, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelMgRep.setFont(font)
        self.labelMgRep.setObjectName("labelMgRep")
        self.mgRepMainWin = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.mgRepMainWin.setGeometry(QtCore.QRect(350, 110, 251, 91))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.mgRepMainWin.setFont(font)
        self.mgRepMainWin.setFrameShape(QtWidgets.QFrame.Box)
        self.mgRepMainWin.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mgRepMainWin.setPlainText("")
        self.mgRepMainWin.setReadOnly(True)
        self.mgRepMainWin.setObjectName("mgRepMainWin")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 658, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuPreferences = QtWidgets.QMenu(self.menubar)
        self.menuPreferences.setObjectName("menuPreferences")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionPre_recorded_Instructions = QtWidgets.QAction(MainWindow)
        self.actionPre_recorded_Instructions.setObjectName("actionPre_recorded_Instructions")
        self.actionAudio_Device_selection = QtWidgets.QAction(MainWindow)
        self.actionAudio_Device_selection.setObjectName("actionAudio_Device_selection")
        self.actionGeneral = QtWidgets.QAction(MainWindow)
        self.actionGeneral.setObjectName("actionGeneral")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionNew_Project = QtWidgets.QAction(MainWindow)
        self.actionNew_Project.setObjectName("actionNew_Project")
        self.actionOpen_Project = QtWidgets.QAction(MainWindow)
        self.actionOpen_Project.setObjectName("actionOpen_Project")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addAction(self.actionOpen_Project)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuPreferences.addAction(self.actionPre_recorded_Instructions)
        self.menuPreferences.addAction(self.actionAudio_Device_selection)
        self.menuPreferences.addAction(self.actionGeneral)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.actionNew_Project.triggered.connect(self.new_project)
        self.actionOpen_Project.triggered.connect(self.open_project)
        self.spViewMoreBtn.clicked.connect(self.onClickedSpViewMoreBtn)
        self.mgViewMoreBtn.clicked.connect(self.onClickedMgViewMoreBtn)
        self.actionExit.triggered.connect(self.close_application)
        self.actionAbout_Qt.triggered.connect(QtWidgets.QApplication.aboutQt)
        self.actionAbout.triggered.connect(self.dialogAbout)
        self.actionAudio_Device_selection.triggered.connect(self.onClickedAudioDevSelBtn)
        self.actionPre_recorded_Instructions.triggered.connect(self.onClickedPreRecordedInstructions)

        self.retranslateUi(MainWindow)
        try:
            global audioListFile
            with open('appRes/store.dat', 'rb') as f:
                    audioListFile = pickle.load(f)
        except:
            print("Fresh Install")
            pass

        if not os.path.exists("appRes/recordings/"):
            os.makedirs("appRes/recordings/")

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        app.aboutToQuit.connect(self.exit_message)
        self.recordMG.clicked.connect(self.recordMGData)
        self.recordSpeech.setEnabled(False)
        self.spViewMoreBtn.setEnabled(False)
        self.getSpRepBtn.setEnabled(False)
        self.getMgRepBtn.setEnabled(False)
        self.mgViewMoreBtn.setEnabled(False)
        self.TestNameCombo.insertItems(0,['Arch.Guided Spiral','Repeat Letters','Copy Sentence','Switching Letters'])
        self.recordSpeech.clicked.connect(self.recordSP)
        self.getSpRepBtn.clicked.connect(self.onClickedGetSpRepBtn)
        self.getMgRepBtn.clicked.connect(self.onClickedGetMgRepBtn)
        self.radioControl2.toggled.connect(self.onClickedControl2)
        self.radioParkinson2.toggled.connect(self.onClickedParkinson2)
        self.WacExtStatus.setText("Extractor Stopped")
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowTitleHint)
        MainWindow.setFixedSize(MainWindow.size())
        MainWindow.setWindowState(QtCore.Qt.WindowActive)
        MainWindow.activateWindow()
        
    def recordSP(self):
        Ui_DialogRecAudio().exec_()

    def onClickedAudioDevSelBtn(self):
        Ui_DialogAudioDevSel().exec_()
     
    def onClickedPreRecordedInstructions(self):
        Ui_DialogPreRecordedInst().exec_()

    def dialogAbout(self):
     Ui_DialogAbout().exec_()

    def onClickedMgViewMoreBtn(self):
        Ui_DialogMgRepViewer().exec_()

    def onClickedSpViewMoreBtn(self):
        Ui_DialogSpeechRepViewer().exec_()
    
    def onClickedGetMgRepBtn(self):
        global mgtesttypesCG
        global mgtestNamesCG
        global mgtesttypesPD
        global mgtestNamesPD
        mgtesttypesCG=[]
        mgtestNamesCG=[]
        mgtesttypesPD=[]
        mgtestNamesPD=[]
        pathTemp=path+'/'+'MG_Data'
        if os.path.exists(pathTemp):
            pathTemp=pathTemp+'/'+'CG'
            if os.path.exists(pathTemp):
                for _, dirnames, filenames in os.walk(pathTemp):
                    if not len(dirnames)==0:
                        mgtesttypesCG.extend(dirnames)
                    if not len(filenames)==0:
                        for i in filenames:
                            if i[len(i)-3:len(i)]=='log':
                                mgtestNamesCG.append(i[0:len(i)-4])
                    print(dirnames)
                    print(filenames)
                print(f"\n\nResult : {mgtesttypesCG}  {mgtestNamesCG}\n\n")
               
            pathTemp=path+'/'+'MG_Data'+'/'+'PD'
            if os.path.exists(pathTemp):
                for _, dirnames, filenames in os.walk(pathTemp):
                    if not len(dirnames)==0:
                        mgtesttypesPD.extend(dirnames)
                    if not len(filenames)==0:
                        for i in filenames:
                            if i[len(i)-3:len(i)]=='log':
                                mgtestNamesPD.append(i[0:len(i)-4])
                    print(dirnames)
                    print(filenames)
                print(f"\n\nResult : {mgtesttypesPD}  {mgtestNamesPD}\n\n")

            self.mgRepMainWin.setPlainText(f"Found {len(mgtesttypesPD)} PD Records:\n\n{mgtesttypesPD}\n\nwith {len(mgtestNamesPD)} TestNames:\n\n{mgtestNamesPD}\n\nFound {len(mgtesttypesCG)} CG Records:\n\n{mgtesttypesCG}\n\nwith {len(mgtestNamesCG)} TestNames:\n\n{mgtestNamesCG}\n\n")           
            self.mgViewMoreBtn.setEnabled(True)
        else:
            self.mgRepMainWin.setPlainText("No MG data found.")

    def onClickedGetSpRepBtn(self):
        global sprecNamesCG
        global sptestNamesCG
        global sprecNamesPD
        global sptestNamesPD
        sprecNamesCG=[]
        sptestNamesCG=[]
        sprecNamesPD=[]
        sptestNamesPD=[]
        pathTemp=path+'/'+'Speech_Data'
        if os.path.exists(pathTemp):
            pathTemp=pathTemp+'/'+'CG'
            if os.path.exists(pathTemp):
                for _, dirnames, filenames in os.walk(pathTemp):
                    if not len(dirnames)==0:
                        sprecNamesCG.extend(dirnames)
                    if not len(filenames)==0:
                        for i in filenames:
                            if i[len(i)-3:len(i)]=='wav':
                                sptestNamesCG.append(i[0:len(i)-4])
                    print(dirnames)
                    print(filenames)
                print(f"\n\nResult : {sprecNamesCG}  {sptestNamesCG}\n\n")
               
            pathTemp=path+'/'+'Speech_Data'+'/'+'PD'
            if os.path.exists(pathTemp):
                for _, dirnames, filenames in os.walk(pathTemp):
                    if not len(dirnames)==0:
                        sprecNamesPD.extend(dirnames)
                    if not len(filenames)==0:
                        for i in filenames:
                            if i[len(i)-3:len(i)]=='wav':
                                sptestNamesPD.append(i[0:len(i)-4])
                    print(dirnames)
                    print(filenames)
                print(f"\n\nResult : {sprecNamesPD}  {sptestNamesPD}\n\n")

            
            self.spRepMainWin.setPlainText(f"Found {len(sprecNamesPD)} PD Records:\n\n{sprecNamesPD}\n\nwith {len(sptestNamesPD)} TestNames:\n\n{sptestNamesPD}\n\nFound {len(sprecNamesCG)} CG Records:\n\n{sprecNamesCG}\n\nwith {len(sptestNamesCG)} TestNames:\n\n{sptestNamesCG}\n\n")
            self.spViewMoreBtn.setEnabled(True)
        else:
            self.spRepMainWin.setPlainText("No Speech data found.")
                
       
    def btnstate(self,b):
        if b.text() == "Control":
            if b.isChecked() == False:
                self.recordMG.setEnabled(False)
        elif b.text() == "Parkinson's":
            if b.isChecked() == False:
                self.recordMG.setEnabled(False)
    
    def btnstate2(self,b):
        if b.text() == "Control":
            if b.isChecked() == False:
                self.recordSpeech.setEnabled(False)
        elif b.text() == "Parkinson's":
            if b.isChecked() == False:
                self.recordSpeech.setEnabled(False)

    def close_application(self):
        close = QtWidgets.QMessageBox.question(self,"Confirmation","Are you sure you want to exit?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            close2 = QtWidgets.QMessageBox.information(self,"Info","Data saved to project folder.\nFor folder structure refer documentation.", QtWidgets.QMessageBox.Ok)
            if close2 == QtWidgets.QMessageBox.Ok:
                sys.exit()

    def exit_message(self):
        close = QtWidgets.QMessageBox.information(self,"Info","Data saved to project folder.\nFor folder structure refer documentation.", QtWidgets.QMessageBox.Ok)
        if close == QtWidgets.QMessageBox.Ok:
            sys.exit()

    def onClickedControl2(self):
        radioButton = self.radioControl2
        global selSpeech
        if radioButton.isChecked():
            print("CG")
            selSpeech="CG"
            global cFlagSpeech
            cFlagSpeech=True
            if pFlag==True:
                self.recordSpeech.setEnabled(True)


    def onClickedParkinson2(self):
        radioButton = self.radioParkinson2
        global selSpeech
        if radioButton.isChecked():
            print("PD")
            selSpeech="PD"
            global cFlagSpeech
            cFlagSpeech=True
            if pFlag==True:
                self.recordSpeech.setEnabled(True)
    
    def onClickedControl(self):
        radioButton = self.radioControl
        global selMG
        if radioButton.isChecked():
            print("CG")
            selMG="CG"
            global cFlagMG
            cFlagMG=True
            if pFlag==True and recordMGFlag==False:
              self.recordMG.setEnabled(True)


    def onClickedParkinson(self):
        radioButton = self.radioParkinson
        global selMG
        if radioButton.isChecked():
            print("PD")
            selMG="PD"
            global cFlagMG
            cFlagMG=True
            if pFlag==True and recordMGFlag==False:
              self.recordMG.setEnabled(True)


    def new_project(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, "New Project", "", "WaFex Files (*.wafex );;All Files (*)") 
        if fileName:
            global path
            path=os.path.dirname(fileName)
            temp=str(fileName).split('/')
            tempFn=str(temp[len(temp)-1])
            path=path+"/"+tempFn[0:-6]+"/"
            path = os.path.dirname(path)
            print(path)
            if not os.path.exists(path):
               os.makedirs(path)

            fnName=path+"/"+tempFn
            print(fnName)
            with open(fnName,'w') as proj:
                proj.write(str(fnName)+"#")
                proj.write(str(datetime.datetime.now().strftime("%c")+"#"))
                proj.write(str(datetime.datetime.now().strftime("%f"))+"#")

            
            # temp=str(fileName).split('/')
            # tempFn=str(temp[len(temp)-1])
            font = QtGui.QFont()
            font.setFamily("Consolas")
            font.setPointSize(10)
            font.setItalic(False)
            self.ProjName.setFont(font)
            self.ProjName.setAlignment(QtCore.Qt.AlignLeft)
            self.ProjName.setText("Name: "+tempFn[0:-6]+"\n"+"Date: "+str(datetime.datetime.now().strftime("%c"))+"\n"+"ID: "+str(datetime.datetime.now().strftime("%f")))
            global pFlag
            pFlag=True
            if cFlagMG and (self.radioControl.isChecked()==True or self.radioParkinson.isChecked()==True):
              self.recordMG.setEnabled(True)
            if cFlagSpeech==True and (self.radioControl2.isChecked()==True or self.radioParkinson2.isChecked()==True):
                self.recordSpeech.setEnabled(True)
            self.getSpRepBtn.setEnabled(True)
            self.getMgRepBtn.setEnabled(True)
    

    def open_project(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open Project", "", "WaFex Files (*.wafex );;All Files (*)")
        if fileName:
          global path
          path=os.path.dirname(fileName)
          data=""
          with open(fileName, "r") as f:
             for z in f:
                 data=data+z      
          
          temp1=str(data).split('#')
          temp=str(temp1[0]).split('/')
          tempFn=str(temp[len(temp)-1])
          font = QtGui.QFont()
          font.setFamily("Consolas")
          font.setPointSize(10)
          font.setItalic(False)
          self.ProjName.setFont(font)
          self.ProjName.setAlignment(QtCore.Qt.AlignLeft)
          self.ProjName.setText("Name: "+tempFn[0:-6]+"\n"+"Date: "+temp1[1]+"\n"+"ID: "+temp1[2])
          global pFlag
          pFlag=True
          if cFlagMG and (self.radioControl.isChecked()==True or self.radioParkinson.isChecked()==True):
              self.recordMG.setEnabled(True)
          if cFlagSpeech==True and (self.radioControl2.isChecked()==True or self.radioParkinson2.isChecked()==True):
              self.recordSpeech.setEnabled(True)
          self.getSpRepBtn.setEnabled(True)
          self.getMgRepBtn.setEnabled(True)
        

        print(path)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PDFE"))
        self.label.setText(_translate("MainWindow", "Device Status"))
        self.label_2.setText(_translate("MainWindow", "Project Details"))
        self.label_3.setText(_translate("MainWindow", "Data Acquisition"))
        self.label_4.setText(_translate("MainWindow", "Micrographia"))
        self.label_5.setText(_translate("MainWindow", "Speech"))
        self.label_6.setText(_translate("MainWindow", "Speech"))
        self.label_7.setText(_translate("MainWindow", "Viewer"))
        self.label_8.setText(_translate("MainWindow", "Micrographia"))
        self.radioControl.setText(_translate("MainWindow", "Control"))
        self.radioParkinson.setText(_translate("MainWindow", "Parkinson\'s"))
        self.ProjName.setText(_translate("MainWindow", "No projects opened."))
        self.labelSpRep.setText(_translate("MainWindow", "Record Report:"))
        self.spViewMoreBtn.setText(_translate("MainWindow", "View More.."))
        self.getSpRepBtn.setText(_translate("MainWindow", "Get Report"))
        self.mgViewMoreBtn.setText(_translate("MainWindow", "View More.."))
        self.getMgRepBtn.setText(_translate("MainWindow", "Get Report"))
        self.labelMgRep.setText(_translate("MainWindow", "Record Report:"))
        self.recordMG.setText(_translate("MainWindow", "Record"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.TestNameCombo.setToolTip(_translate("MainWindow", "Select Type"))
        self.menuPreferences.setTitle(_translate("MainWindow", "Preferences"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionPre_recorded_Instructions.setText(_translate("MainWindow", "Pre-recorded Instructions"))
        self.actionAudio_Device_selection.setText(_translate("MainWindow", "Audio Device Selection"))
        self.actionGeneral.setText(_translate("MainWindow", "General"))
        self.actionAbout.setText(_translate("MainWindow", "About PDFE"))
        self.actionNew_Project.setText(_translate("MainWindow", "New Project.."))
        self.actionOpen_Project.setText(_translate("MainWindow", "Open Project.."))
        self.recordSpeech.setText(_translate("MainWindow", "Record.."))
        self.radioControl2.setText(_translate("MainWindow", "Control"))
        self.radioParkinson2.setText(_translate("MainWindow", "Parkinson\'s"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))


    def recordMGData(self):
            consent = QtWidgets.QMessageBox.question(self,"Confirmation","You will not be able to cancel later on!\nAre you sure to continue?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if consent==QtWidgets.QMessageBox.Yes:
                if Ui_DialogPlayInstruction().exec_()!=2:
                    global recordMGFlag
                    recordMGFlag=True
                    self.WacExtStatus.setText("Extractor Running")
                    self.recordMG.setEnabled(False)
                    self.actionNew_Project.setEnabled(False)
                    self.actionOpen_Project.setEnabled(False)
                    testname=self.TestNameCombo.currentText()
                    self.newThread = MGWorker(testname)
                    print(f'MG TestName: {testname}')
                    self.newThread.signal.connect(self.finished)
                    self.newThread.start() 
            else:
                consent = QtWidgets.QMessageBox.information(self,"Information","Record Cancelled.",QtWidgets.QMessageBox.Ok)            
             
                
    def finished(self, result):
        global recordMGFlag
        if str(result)=="Error":
            self.newThread.stop()
            if self.radioControl.isChecked()==False and self.radioParkinson.isChecked()==False:
                self.recordMG.setEnabled(False)
            else:
                self.recordMG.setEnabled(True)
            self.actionNew_Project.setEnabled(True)
            self.actionOpen_Project.setEnabled(True)
            self.WacExtStatus.setText("Extractor Stopped")
            recordMGFlag=False
        elif str(result)=="Extractor Stopped":
            self.WacExtStatus.setText(str(result))
            if self.radioControl.isChecked()==False and self.radioParkinson.isChecked()==False:
                self.recordMG.setEnabled(False)
            else:
                self.recordMG.setEnabled(True)
            self.actionNew_Project.setEnabled(True)
            self.actionOpen_Project.setEnabled(True)
            recordMGFlag=False
        elif str(result)=="Extracting...":
            self.WacExtStatus.setText(str(result))
            

class PWindow(QtWidgets.QMainWindow):
    def closeEvent(self,event):
       close = QtWidgets.QMessageBox.question(self,"Confirmation","Are you sure you want to exit?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
       if close == QtWidgets.QMessageBox.Yes:
            event.accept()
       else:
            event.ignore()  


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pixmap = QtGui.QPixmap("appRes/splash.jpg")
    splash = QtWidgets.QSplashScreen(pixmap,QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    splash.showMessage("<h3><font color='white'>Intialiasing...</font></h3>", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.black)
    splash.showMessage("<h3><font color='white'>Loading..</font></h3>", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.black)
    app.processEvents()
    try:
        from msvcrt import getch
        import datetime
        import time
        import pickle
        from time import sleep
        import wmi
        splash.showMessage("<h3><font color='white'>Loading module wmi..</font></h3>", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.black)
        print("WMI")
        import parselmouth
        splash.showMessage("<h3><font color='white'>Loading module parselmouth..</font></h3>", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.black)
        print("Parselmouth")
        import numpy as np
        import seaborn as sep
        splash.showMessage("<h3><font color='white'>Loading module seaborn..</font></h3>", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.black)
        print("Seaborn")
        import pyaudio
        splash.showMessage("<h3><font color='white'>Loading module pyaudio..</font></h3>", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.black)
        print("PyAudio")
        import wave
        splash.showMessage("<h3><font color='white'>Loading module wave..</font></h3>", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.black)
        print("Wave")
        import mplcursors
        import csv
        import datetime
        import subprocess
        import os
        import shutil
        from sys import byteorder
        from array import array
        from struct import pack
        import statistics
        splash.showMessage("<h3><font color='white'>Loading module statistics..</font></h3>", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.black)
        print("Statistics") 
    except Exception as e:
        print(e) 
        splash.showMessage("<h3><font color='white'>Error loading modules.</font></h3>", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.black)


    CHUNK_SIZE = 1024
    CHANNELS=1
    FORMAT = pyaudio.paInt16 # 16 bit res
    RATE = 48000
    THRESHOLD = 3200
    INPUT_DEVICE_IND=1
    OUTPUT_DEVICE_IND=1

    # MainWindow = QtWidgets.QMainWindow()
    MainWindow=PWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    splash.showMessage("<h3><font color='white'>Done.</font></h3>", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.black)
    MainWindow.show()
    splash.finish(MainWindow)
    if len(audioListFile)==0:
        QtWidgets.QMessageBox.information(MainWindow,"Information","PDFE detected no \"Pre-recorded Instructions\".\nTo record one, go to Menu-bar-->Preferences-->Pre-recorded Instructions",QtWidgets.QMessageBox.Ok)
    sys.exit(app.exec_())