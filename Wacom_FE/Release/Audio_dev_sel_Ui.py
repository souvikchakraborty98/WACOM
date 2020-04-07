# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Audio_dev_sel_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox_audio = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox_audio.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox_audio.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_audio.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_audio.setObjectName("buttonBox_audio")
        self.comboBox_audio_in = QtWidgets.QComboBox(Dialog)
        self.comboBox_audio_in.setGeometry(QtCore.QRect(40, 70, 231, 22))
        self.comboBox_audio_in.setObjectName("comboBox_audio_in")
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
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(350, 10, 31, 31))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("refresh.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.PlayBtnTest = QtWidgets.QPushButton(Dialog)
        self.PlayBtnTest.setGeometry(QtCore.QRect(284, 140, 31, 23))
        self.PlayBtnTest.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Play.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlayBtnTest.setIcon(icon1)
        self.PlayBtnTest.setObjectName("PlayBtnTest")

        self.retranslateUi(Dialog)
        self.buttonBox_audio.accepted.connect(Dialog.accept)
        self.buttonBox_audio.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_audio_in.setText(_translate("Dialog", "Audio In:"))
        self.label_audio_out.setText(_translate("Dialog", "Audio Out:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
