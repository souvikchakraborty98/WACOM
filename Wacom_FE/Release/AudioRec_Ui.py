# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AudioRec_UI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(331, 380)
        self.updateThresholdBtn = QtWidgets.QPushButton(Dialog)
        self.updateThresholdBtn.setGeometry(QtCore.QRect(180, 60, 101, 23))
        self.updateThresholdBtn.setObjectName("updateThresholdBtn")
        self.inputThreshold = QtWidgets.QLineEdit(Dialog)
        self.inputThreshold.setGeometry(QtCore.QRect(180, 30, 113, 20))
        self.inputThreshold.setObjectName("inputThreshold")
        self.audioThreshValues = QtWidgets.QPlainTextEdit(Dialog)
        self.audioThreshValues.setGeometry(QtCore.QRect(20, 130, 271, 221))
        self.audioThreshValues.setObjectName("audioThreshValues")
        self.label_at = QtWidgets.QLabel(Dialog)
        self.label_at.setGeometry(QtCore.QRect(20, 110, 121, 16))
        self.label_at.setObjectName("label_at")
        self.recordAudioBtn = QtWidgets.QPushButton(Dialog)
        self.recordAudioBtn.setGeometry(QtCore.QRect(20, 60, 75, 23))
        self.recordAudioBtn.setObjectName("recordAudioBtn")
        self.TestName = QtWidgets.QLineEdit(Dialog)
        self.TestName.setGeometry(QtCore.QRect(20, 30, 113, 20))
        self.TestName.setObjectName("TestName")
        self.label_tn = QtWidgets.QLabel(Dialog)
        self.label_tn.setGeometry(QtCore.QRect(20, 10, 50, 13))
        self.label_tn.setObjectName("label_tn")
        self.label_thres = QtWidgets.QLabel(Dialog)
        self.label_thres.setGeometry(QtCore.QRect(180, 10, 50, 13))
        self.label_thres.setObjectName("label_thres")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.updateThresholdBtn.setText(_translate("Dialog", "Update Threshold"))
        self.inputThreshold.setText(_translate("Dialog", "2500"))
        self.label_at.setText(_translate("Dialog", "Audio Threshold Values:"))
        self.recordAudioBtn.setText(_translate("Dialog", "Record"))
        self.label_tn.setText(_translate("Dialog", "Test Name"))
        self.label_thres.setText(_translate("Dialog", "Threshold"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
