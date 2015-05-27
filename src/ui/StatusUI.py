# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\ui\Status.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(522, 441)
        self.gridLayout_3 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_32 = QtWidgets.QLabel(Dialog)
        self.label_32.setObjectName("label_32")
        self.gridLayout_7.addWidget(self.label_32, 2, 0, 1, 1)
        self.currenlyAtSystemTxt = QtWidgets.QLineEdit(Dialog)
        self.currenlyAtSystemTxt.setReadOnly(True)
        self.currenlyAtSystemTxt.setObjectName("currenlyAtSystemTxt")
        self.gridLayout_7.addWidget(self.currenlyAtSystemTxt, 2, 1, 1, 1)
        self.label_33 = QtWidgets.QLabel(Dialog)
        self.label_33.setObjectName("label_33")
        self.gridLayout_7.addWidget(self.label_33, 3, 0, 1, 1)
        self.loadedRangeTXt = QtWidgets.QLineEdit(Dialog)
        self.loadedRangeTXt.setObjectName("loadedRangeTXt")
        self.gridLayout_7.addWidget(self.loadedRangeTXt, 1, 1, 1, 1)
        self.label_34 = QtWidgets.QLabel(Dialog)
        self.label_34.setObjectName("label_34")
        self.gridLayout_7.addWidget(self.label_34, 4, 0, 1, 1)
        self.dockingRequestStatusTxt = QtWidgets.QLineEdit(Dialog)
        self.dockingRequestStatusTxt.setReadOnly(True)
        self.dockingRequestStatusTxt.setObjectName("dockingRequestStatusTxt")
        self.gridLayout_7.addWidget(self.dockingRequestStatusTxt, 4, 1, 1, 1)
        self.label_30 = QtWidgets.QLabel(Dialog)
        self.label_30.setObjectName("label_30")
        self.gridLayout_7.addWidget(self.label_30, 0, 0, 1, 1)
        self.currentlyNearAtTxt = QtWidgets.QLineEdit(Dialog)
        self.currentlyNearAtTxt.setReadOnly(True)
        self.currentlyNearAtTxt.setObjectName("currentlyNearAtTxt")
        self.gridLayout_7.addWidget(self.currentlyNearAtTxt, 3, 1, 1, 1)
        self.label_31 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)
        self.label_31.setObjectName("label_31")
        self.gridLayout_7.addWidget(self.label_31, 1, 0, 1, 1)
        self.unladenRangeTxt = QtWidgets.QLineEdit(Dialog)
        self.unladenRangeTxt.setObjectName("unladenRangeTxt")
        self.gridLayout_7.addWidget(self.unladenRangeTxt, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem, 5, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_7, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_32.setText(_translate("Dialog", "Current system"))
        self.label_33.setText(_translate("Dialog", "Curretly near at"))
        self.label_34.setText(_translate("Dialog", "Docking request sent"))
        self.label_30.setText(_translate("Dialog", "Ship unladen jump range"))
        self.label_31.setText(_translate("Dialog", "Ship fully loaded jump range"))

