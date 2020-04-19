# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\playInstruction_UI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 150)
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

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_choose.setText(_translate("Dialog", "Choose Instruction:"))
        self.continueToRecordBtn.setText(_translate("Dialog", "Continue"))
        self.cancelRecord.setText(_translate("Dialog", "Terminate Record"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
