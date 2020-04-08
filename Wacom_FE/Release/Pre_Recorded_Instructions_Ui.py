# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Pre_Recorded_Instructions_UI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(507, 399)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(130, 350, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
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
        self.addItems = QtWidgets.QPushButton(Dialog)
        self.addItems.setGeometry(QtCore.QRect(20, 290, 91, 23))
        self.addItems.setObjectName("addItems")
        self.deleteItems = QtWidgets.QPushButton(Dialog)
        self.deleteItems.setGeometry(QtCore.QRect(140, 290, 91, 23))
        self.deleteItems.setObjectName("deleteItems")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.addItems.setText(_translate("Dialog", "Add Item.."))
        self.deleteItems.setText(_translate("Dialog", "Delete Item.."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
