# from PyQt5 import QtCore, QtGui, QtWidgets

# class Ui_Dialog(object):
#     def setupUi(self, Dialog):
#         Dialog.setObjectName("Dialog")
#         Dialog.resize(358, 126)
#         self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
#         self.verticalLayout.setObjectName("verticalLayout")
#         self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
#         self.horizontalLayout_3.setObjectName("horizontalLayout_3")
#         self.dialoglabel = QtWidgets.QLabel(Dialog)
#         self.dialoglabel.setObjectName("dialoglabel")
#         self.horizontalLayout_3.addWidget(self.dialoglabel)
#         self.verticalLayout.addLayout(self.horizontalLayout_3)
#         self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
#         self.horizontalLayout_2.setObjectName("horizontalLayout_2")
#         self.dialoglineedit = QtWidgets.QLineEdit(Dialog)
#         self.dialoglineedit.setObjectName("dialoglineedit")
#         self.horizontalLayout_2.addWidget(self.dialoglineedit)
#         self.verticalLayout.addLayout(self.horizontalLayout_2)
#         self.horizontalLayout = QtWidgets.QHBoxLayout()
#         self.horizontalLayout.setObjectName("horizontalLayout")
#         self.pushButton_2 = QtWidgets.QPushButton(Dialog)
#         self.pushButton_2.setObjectName("pushButton_2")
#         self.horizontalLayout.addWidget(self.pushButton_2)
#         self.pushButton = QtWidgets.QPushButton(Dialog)
#         self.pushButton.setObjectName("pushButton")
#         self.horizontalLayout.addWidget(self.pushButton)
#         self.verticalLayout.addLayout(self.horizontalLayout)

#         self.retranslateUi(Dialog)
#         QtCore.QMetaObject.connectSlotsByName(Dialog)

#         # connect the two functions
     
#     def retranslateUi(self, Dialog):
#         _translate = QtCore.QCoreApplication.translate
#         Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
#         self.dialoglabel.setText(_translate("Dialog", "dialoglabel"))
#         self.pushButton_2.setText(_translate("Dialog", "Acept"))
#         self.pushButton.setText(_translate("Dialog", "Cancel"))

#     # 2 sample functions
#     def return_accept(self):
#         print("yes")

#     def return_cancel(self):
#         print("no")

# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(670, 492)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
#         self.verticalLayout.setObjectName("verticalLayout")
#         self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
#         self.horizontalLayout_2.setObjectName("horizontalLayout_2")
#         self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
#         self.tableWidget.setObjectName("tableWidget")
#         self.tableWidget.setColumnCount(3)
#         self.tableWidget.setRowCount(0)
#         item = QtWidgets.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(0, item)
#         item = QtWidgets.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(1, item)
#         item = QtWidgets.QTableWidgetItem()
#         self.tableWidget.setHorizontalHeaderItem(2, item)
#         self.horizontalLayout_2.addWidget(self.tableWidget)
#         self.verticalLayout.addLayout(self.horizontalLayout_2)
#         self.horizontalLayout = QtWidgets.QHBoxLayout()
#         self.horizontalLayout.setObjectName("horizontalLayout")
#         self.firstbutton = QtWidgets.QPushButton(self.centralwidget)
#         self.firstbutton.setObjectName("firstbutton")
#         self.horizontalLayout.addWidget(self.firstbutton)
#         self.secondbutton = QtWidgets.QPushButton(self.centralwidget)
#         self.secondbutton.setObjectName("secondbutton")
#         self.horizontalLayout.addWidget(self.secondbutton)
#         self.verticalLayout.addLayout(self.horizontalLayout)
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 670, 21))
#         self.menubar.setObjectName("menubar")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)

#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)

#         self.firstbutton.clicked.connect(self.open_dialog)

#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         item = self.tableWidget.horizontalHeaderItem(0)
#         item.setText(_translate("MainWindow", "First column"))
#         item = self.tableWidget.horizontalHeaderItem(1)
#         item.setText(_translate("MainWindow", "Second column"))
#         item = self.tableWidget.horizontalHeaderItem(2)
#         item.setText(_translate("MainWindow", "Third"))
#         self.firstbutton.setText(_translate("MainWindow", "Add"))
#         self.secondbutton.setText(_translate("MainWindow", "Delete"))

#     def open_dialog(self):
#         dialog = QtWidgets.QDialog()
#         dialog.ui.setupUi(dialog)
#         dialog.exec_()
#         dialog.show()


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())