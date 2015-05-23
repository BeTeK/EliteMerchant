# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\ui\EdceVerification.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(373, 345)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelBtn = QtWidgets.QPushButton(Dialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout.addWidget(self.cancelBtn)
        self.okBtn = QtWidgets.QPushButton(Dialog)
        self.okBtn.setObjectName("okBtn")
        self.horizontalLayout.addWidget(self.okBtn)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verificationCodeTxt = QtWidgets.QLineEdit(Dialog)
        self.verificationCodeTxt.setObjectName("verificationCodeTxt")
        self.gridLayout_2.addWidget(self.verificationCodeTxt, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.cancelBtn.setText(_translate("Dialog", "Cancel"))
        self.okBtn.setText(_translate("Dialog", "Ok"))
        self.label.setText(_translate("Dialog", "Verification code needed. Check your email and insert code here."))

