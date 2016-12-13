from PyQt4 import QtCore, QtGui
import http.server
import socketserver
import socket
import subprocess
import os
import random
from threading import Thread

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_HTTPServer(object):
    def setupUi(self, HTTPServer):
        HTTPServer.setObjectName(_fromUtf8("HTTPServer"))
        HTTPServer.resize(469, 334)
        self.centralwidget = QtGui.QWidget(HTTPServer)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 40, 341, 155))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.password_label = QtGui.QLabel(self.gridLayoutWidget)
        self.password_label.setObjectName(_fromUtf8("password_label"))
        self.gridLayout.addWidget(self.password_label, 1, 0, 1, 1)
        self.repassword_label = QtGui.QLabel(self.gridLayoutWidget)
        self.repassword_label.setObjectName(_fromUtf8("repassword_label"))
        self.gridLayout.addWidget(self.repassword_label, 2, 0, 1, 1)
        self.username = QtGui.QLineEdit(self.gridLayoutWidget)
        self.username.setObjectName(_fromUtf8("username"))
        self.gridLayout.addWidget(self.username, 0, 1, 1, 1)
        self.password = QtGui.QLineEdit(self.gridLayoutWidget)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.gridLayout.addWidget(self.password, 1, 1, 1, 1)
        self.repassword = QtGui.QLineEdit(self.gridLayoutWidget)
        self.repassword.setText(_fromUtf8(""))
        self.repassword.setEchoMode(QtGui.QLineEdit.Password)
        self.repassword.setObjectName(_fromUtf8("repassword"))
        self.gridLayout.addWidget(self.repassword, 2, 1, 1, 1)
        self.username_label = QtGui.QLabel(self.gridLayoutWidget)
        self.username_label.setObjectName(_fromUtf8("username_label"))
        self.gridLayout.addWidget(self.username_label, 0, 0, 1, 1)
        self.sharedfolder = QtGui.QLineEdit(self.gridLayoutWidget)
        self.sharedfolder.setPlaceholderText(_fromUtf8(""))
        self.sharedfolder.setObjectName(_fromUtf8("sharedfolder"))
        self.gridLayout.addWidget(self.sharedfolder, 5, 1, 1, 1)
        self.sharedfolder_label = QtGui.QLabel(self.gridLayoutWidget)
        self.sharedfolder_label.setObjectName(_fromUtf8("sharedfolder_label"))
        self.gridLayout.addWidget(self.sharedfolder_label, 5, 0, 1, 1)
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(120, 230, 211, 80))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.startserver = QtGui.QPushButton(self.verticalLayoutWidget)
        self.startserver.setObjectName(_fromUtf8("startserver"))
        self.verticalLayout.addWidget(self.startserver)
        self.directory_link = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.directory_link.setAlignment(QtCore.Qt.AlignCenter)
        self.directory_link.setObjectName(_fromUtf8("directory_link"))
        self.verticalLayout.addWidget(self.directory_link)
        self.stopserver = QtGui.QPushButton(self.verticalLayoutWidget)
        self.stopserver.setObjectName(_fromUtf8("stopserver"))
        self.verticalLayout.addWidget(self.stopserver)
        self.browse = QtGui.QPushButton(self.centralwidget)
        self.browse.setGeometry(QtCore.QRect(320, 200, 81, 23))
        self.browse.setObjectName(_fromUtf8("browse"))
        HTTPServer.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(HTTPServer)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        HTTPServer.setStatusBar(self.statusbar)


        HTTPServer.setFocus()
        self.startserver.clicked.connect(self.taskrunthread)
        self.stopserver.clicked.connect(self.taskstop)
        self.browse.clicked.connect(self.browsefunc)

        self.retranslateUi(HTTPServer)
        QtCore.QMetaObject.connectSlotsByName(HTTPServer)

    def browsefunc(self):
        open_dir = QtGui.QFileDialog.getExistingDirectory(HTTPServer,caption="Select Directory")
        open_dir=QtCore.QDir.toNativeSeparators(open_dir)
        os.chdir(open_dir)
        self.sharedfolder.setText(open_dir)

    def passchk(self):
        password=self.password.text()
        repass=self.repassword.text()
        if password!=repass:
            QtGui.QMessageBox.warning(HTTPServer,"Passwords unmatch","Please re enter the same password as above.")
            return 0

    def taskrunthread(self):
        t=Thread(target=self.taskcode)
        t.start()


    def taskcode(self):
        if self.passchk()!=0:
            username=self.username.text()
            password=self.password.text()
            ipadrs = str(socket.gethostbyname(socket.gethostname()))
            PORT = random.randint(8000, 20000)
            self.directory_link.setText(str('Open http://' + ipadrs + ':' + str(PORT) + ' in browser'))
            os.system('netsh wlan set hostednetwork mode=allow ssid=' + username + ' key=' + password)
            os.system('netsh wlan start hostednetwork')
            Handler = http.server.SimpleHTTPRequestHandler
            httpd = socketserver.TCPServer(("", PORT), Handler)

            httpd.serve_forever()

        else:
            self.password.setText("")
            self.repassword.setText("")

    def taskstop(self):
        os.system('netsh wlan stop hostednetwork')
        self.directory_link.setText("Server Stopped!")

    def retranslateUi(self, HTTPServer):
        HTTPServer.setWindowTitle(_translate("HTTPServer", "HTTP Server", None))
        self.password_label.setText(_translate("HTTPServer", "Password", None))
        self.repassword_label.setText(_translate("HTTPServer", "Re-enter Password", None))
        self.username.setPlaceholderText(_translate("HTTPServer", "Username for wifi hotspot", None))
        self.password.setPlaceholderText(_translate("HTTPServer", "Password for wifi hotspot", None))
        self.repassword.setPlaceholderText(_translate("HTTPServer", "re enter the same password", None))
        self.username_label.setText(_translate("HTTPServer", "UserName", None))
        self.sharedfolder_label.setText(_translate("HTTPServer", "Shared Folder", None))
        self.startserver.setText(_translate("HTTPServer", "Start Server", None))
        self.directory_link.setPlaceholderText(_translate("HTTPServer", "Directory link", None))
        self.stopserver.setText(_translate("HTTPServer", "Stop Server", None))
        self.browse.setText(_translate("HTTPServer", "Browse...", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    HTTPServer = QtGui.QMainWindow()
    ui = Ui_HTTPServer()
    ui.setupUi(HTTPServer)
    HTTPServer.show()
    app.exec_()
