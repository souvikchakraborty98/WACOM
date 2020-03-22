import PyQt5,os
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot as plt

path=""
selMG=""
selSpeech=""
pFlag=False
cFlagMG=False
cFlagSpeech=False
recordMGFlag=False

class External2(QtCore.QThread):
    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, Tname):
        self.Tname=Tname
        QtCore.QThread.__init__(self)

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
        # if countdown(20)!=True:
        subprocess.Popen(["notepad.exe", formantmatrixSave])
        subprocess.Popen(["notepad.exe", mfccdata])
        subprocess.Popen(["notepad.exe", ops])
        # else: 
        #     print("Exiting...")

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
        self.signal.emit("#end")

    def stop(self):
        self.terminate()



class External(QtCore.QThread):
    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):    
        pathMgData = path+"\\MG_Data\\"+selMG+"\\"
        print(f"Micrographia path: {pathMgData}")
        if not os.path.exists(pathMgData):
            os.makedirs(pathMgData)

        filenamecoordNew=pathMgData
        filenamepressNew=pathMgData
        filenamereportNew=pathMgData

        with open("moveFn.log",'w') as moveFn:
                moveFn.write(filenamecoordNew+"+"+filenamepressNew+"+"+filenamereportNew)

        print("\nFolders created..Starting WFE...\n")
        os.startfile("Wacom Feature Extractor.exe")
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


class Ui_DialogAbout(QtWidgets.QDialog):
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("DialogAbout")
        Dialog.resize(283, 201)
        Dialog.setWindowIcon(QtGui.QIcon('logo.ico'))
        Dialog.setFixedSize(Dialog.size())
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(26, 22, 41, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 52, 211, 121))
        self.label_2.setObjectName("label_2")
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "About"))
        self.label.setText(_translate("Dialog", "About"))
        self.label_2.setText(_translate("Dialog", "#ABOUT HERE#"))

class Ui_DialogRecAudio(QtWidgets.QDialog):
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("DialogRecAudio")
        Dialog.resize(331, 380)
        Dialog.setWindowIcon(QtGui.QIcon('mic.ico'))
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
        close = QtWidgets.QMessageBox.question(self,"Confirmation","Are you sure you want to stop recording?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            super(Ui_DialogRecAudio, self).closeEvent(evnt)
            self.newThread.stop()
        else:
            evnt.ignore()
    
    def updateThresholdBtnCLicked(self):
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
        testname=self.TestName.text()
        self.newThread = External2(testname)
        self.newThread.signal.connect(self.updateThreshUI)
        self.recordAudioBtn.setEnabled(False)
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


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
      super().__init__()
      self.setupUi(MainWindow)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(658, 580)
        MainWindow.setWindowIcon(QtGui.QIcon('logo.ico'))
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
        self.ProjName.setFont(font)
        self.ProjName.setFrameShape(QtWidgets.QFrame.Box)
        self.ProjName.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ProjName.setLineWidth(1)
        self.ProjName.setText("")
        self.ProjName.setAlignment(QtCore.Qt.AlignLeft)
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
        self.actionExit.triggered.connect(self.close_application)
        self.actionAbout_Qt.triggered.connect(QtWidgets.QApplication.aboutQt)
        self.actionAbout.triggered.connect(self.dialogAbout)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        app.aboutToQuit.connect(self.exit_message)
        self.recordMG.clicked.connect(self.recordMGData)
        self.recordSpeech.setEnabled(False)
        self.recordSpeech.clicked.connect(self.recordSP)
        self.radioControl2.toggled.connect(self.onClickedControl2)
        self.radioParkinson2.toggled.connect(self.onClickedParkinson2)
        self.WacExtStatus.setText("Extractor Stopped")
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowTitleHint)
        MainWindow.setFixedSize(MainWindow.size())
    
    def recordSP(self):
     Ui_DialogRecAudio().exec_()
     

    def dialogAbout(self):
     Ui_DialogAbout().exec_()

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
            sys.exit()
    
    def exit_message(self):
        close = QtWidgets.QMessageBox.information(self,"Info","Data saved to project folder.\nFor folder structure refer documentation.", QtWidgets.QMessageBox.Ok)
        close.setWindowIcon('logo.ico')
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
            self.ProjName.setText("Name: "+tempFn[0:-6]+"\n"+"Date: "+str(datetime.datetime.now().strftime("%c"))+"\n"+"ID: "+str(datetime.datetime.now().strftime("%f")))
            global pFlag
            pFlag=True
            if cFlagMG==True:
              self.recordMG.setEnabled(True)
            if cFlagSpeech==True:
                self.recordSpeech.setEnabled(True)
    

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
          self.ProjName.setText("Name: "+tempFn[0:-6]+"\n"+"Date: "+temp1[1]+"\n"+"ID: "+temp1[2])
          global pFlag
          pFlag=True
          if cFlagMG==True:
              self.recordMG.setEnabled(True)
          if cFlagSpeech==True:
                self.recordSpeech.setEnabled(True)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "WaFex"))
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
        self.recordMG.setText(_translate("MainWindow", "Record"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
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
            global recordMGFlag
            recordMGFlag=True
            self.WacExtStatus.setText("Extractor Running")
            self.recordMG.setEnabled(False)
            self.actionNew_Project.setEnabled(False)
            self.actionOpen_Project.setEnabled(False)
            self.newThread = External()
            self.newThread.signal.connect(self.finished)
            self.newThread.start()           
             
                
    def finished(self, result):
        if str(result)=="Extractor Stopped":
            self.WacExtStatus.setText(str(result))
        elif str(result)=="Extracting...":
            self.WacExtStatus.setText(str(result))
        if str(result)=="Extractor Stopped":
            if self.radioControl.isChecked()==False and self.radioParkinson.isChecked()==False:
                self.recordMG.setEnabled(False)
            else:
                self.recordMG.setEnabled(True)
            self.actionNew_Project.setEnabled(True)
            self.actionOpen_Project.setEnabled(True)
            global recordMGFlag
            recordMGFlag=False

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
    pixmap = QtGui.QPixmap("splash.jpg")
    splash = QtWidgets.QSplashScreen(pixmap,QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    splash.showMessage("<h3><font color='white'>Intialiasing...</font></h3>", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.black)
    splash.showMessage("<h3><font color='white'>Loading..</font></h3>", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.black)
    app.processEvents()
    try:
        from msvcrt import getch
        import datetime
        import time
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
        import datetime
        import subprocess
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
    INPUT_DEVICE_IN=1

    # MainWindow = QtWidgets.QMainWindow()
    MainWindow=PWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    splash.showMessage("<h3><font color='white'>Done.</font></h3>", QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, QtCore.Qt.black)
    MainWindow.show()
    splash.finish(MainWindow)
    sys.exit(app.exec_())
