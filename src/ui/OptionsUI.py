# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\ui\Options.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(551, 445)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.closeBtn = QtWidgets.QPushButton(Dialog)
        self.closeBtn.setObjectName("closeBtn")
        self.horizontalLayout_5.addWidget(self.closeBtn)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 5, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 4, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.EDCEPathTxt = QtWidgets.QLineEdit(Dialog)
        self.EDCEPathTxt.setObjectName("EDCEPathTxt")
        self.horizontalLayout_4.addWidget(self.EDCEPathTxt)
        self.EDCEPathBtn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EDCEPathBtn.sizePolicy().hasHeightForWidth())
        self.EDCEPathBtn.setSizePolicy(sizePolicy)
        self.EDCEPathBtn.setObjectName("EDCEPathBtn")
        self.horizontalLayout_4.addWidget(self.EDCEPathBtn)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 2, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ElitePathTxt = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ElitePathTxt.sizePolicy().hasHeightForWidth())
        self.ElitePathTxt.setSizePolicy(sizePolicy)
        self.ElitePathTxt.setObjectName("ElitePathTxt")
        self.horizontalLayout_3.addWidget(self.ElitePathTxt)
        self.ElitePathBtn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ElitePathBtn.sizePolicy().hasHeightForWidth())
        self.ElitePathBtn.setSizePolicy(sizePolicy)
        self.ElitePathBtn.setObjectName("ElitePathBtn")
        self.horizontalLayout_3.addWidget(self.ElitePathBtn)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.EDDBUpdateIntervalTxt = QtWidgets.QSpinBox(Dialog)
        self.EDDBUpdateIntervalTxt.setObjectName("EDDBUpdateIntervalTxt")
        self.horizontalLayout_2.addWidget(self.EDDBUpdateIntervalTxt)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.udpateEDDBBtn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.udpateEDDBBtn.sizePolicy().hasHeightForWidth())
        self.udpateEDDBBtn.setSizePolicy(sizePolicy)
        self.udpateEDDBBtn.setObjectName("udpateEDDBBtn")
        self.horizontalLayout_2.addWidget(self.udpateEDDBBtn)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)
        self.MarketValidVal = QtWidgets.QSpinBox(Dialog)
        self.MarketValidVal.setObjectName("MarketValidVal")
        self.gridLayout_2.addWidget(self.MarketValidVal, 3, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.closeBtn.setText(_translate("Dialog", "Close"))
        self.EDCEPathBtn.setText(_translate("Dialog", "..."))
        self.ElitePathBtn.setText(_translate("Dialog", "..."))
        self.label_2.setText(_translate("Dialog", "h"))
        self.udpateEDDBBtn.setText(_translate("Dialog", "Update now"))
        self.label_3.setText(_translate("Dialog", "Elite path"))
        self.label.setText(_translate("Dialog", "EDDB update interval"))
        self.label_4.setText(_translate("Dialog", "EDCE path"))
        self.label_5.setText(_translate("Dialog", "Market expire days"))

