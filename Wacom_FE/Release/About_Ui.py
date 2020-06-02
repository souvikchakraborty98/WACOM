# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\About_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(492, 365)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(20, 60, 451, 281))
        self.textBrowser.setAutoFillBackground(True)
        self.textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textBrowser.setLineWidth(0)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "About"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Open Sans\'; font-size:8pt; color:#444444; background-color:#fcfcfc;\">Copyright 2020 </span> <a href=\"https://github.com/souvikchakraborty98/WACOM/blob/master/README.md\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">Souvik Chakraborty</span></a></p>\n"
"<p style=\" margin-top:0px; margin-bottom:25px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#fcfcfc;\"><span style=\" font-family:\'Open Sans\'; font-size:8pt; font-weight:600; color:#444444; background-color:#fcfcfc;\">TEST COPY</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:25px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#fcfcfc;\"><span style=\" font-family:\'Open Sans\'; font-size:8pt; color:#444444; background-color:#fcfcfc;\">Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:25px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#fcfcfc;\"><span style=\" font-family:\'Open Sans\'; font-size:8pt; color:#444444; background-color:#fcfcfc;\">1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:25px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#fcfcfc;\"><span style=\" font-family:\'Open Sans\'; font-size:8pt; color:#444444; background-color:#fcfcfc;\">2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:25px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#fcfcfc;\"><span style=\" font-family:\'Open Sans\'; font-size:8pt; color:#444444; background-color:#fcfcfc;\">3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:25px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#fcfcfc;\"><span style=\" font-family:\'Open Sans\'; font-size:8pt; color:#444444; background-color:#fcfcfc;\">THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS &quot;AS IS&quot; AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
