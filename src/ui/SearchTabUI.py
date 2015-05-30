# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\ui\SearchTab.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1349, 795)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.maxDistanceTxt = QtWidgets.QLineEdit(Dialog)
        self.maxDistanceTxt.setObjectName("maxDistanceTxt")
        self.gridLayout.addWidget(self.maxDistanceTxt, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.currentSystemTxt = QtWidgets.QLineEdit(Dialog)
        self.currentSystemTxt.setObjectName("currentSystemTxt")
        self.horizontalLayout_3.addWidget(self.currentSystemTxt)
        self.getCurrentBtn = QtWidgets.QPushButton(Dialog)
        self.getCurrentBtn.setObjectName("getCurrentBtn")
        self.horizontalLayout_3.addWidget(self.getCurrentBtn)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.minProfitTxt = QtWidgets.QLineEdit(Dialog)
        self.minProfitTxt.setObjectName("minProfitTxt")
        self.horizontalLayout.addWidget(self.minProfitTxt)
        self.profitPhChk = QtWidgets.QCheckBox(Dialog)
        self.profitPhChk.setChecked(False)
        self.profitPhChk.setObjectName("profitPhChk")
        self.horizontalLayout.addWidget(self.profitPhChk)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 1, 1, 1)
        self.windowCountTxt = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.windowCountTxt.sizePolicy().hasHeightForWidth())
        self.windowCountTxt.setSizePolicy(sizePolicy)
        self.windowCountTxt.setObjectName("windowCountTxt")
        self.gridLayout.addWidget(self.windowCountTxt, 4, 5, 1, 1)
        self.windowSizeTxt = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.windowSizeTxt.sizePolicy().hasHeightForWidth())
        self.windowSizeTxt.setSizePolicy(sizePolicy)
        self.windowSizeTxt.setObjectName("windowSizeTxt")
        self.gridLayout.addWidget(self.windowSizeTxt, 3, 5, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 4, 1, 1)
        self.searchTypeCombo = QtWidgets.QComboBox(Dialog)
        self.searchTypeCombo.setObjectName("searchTypeCombo")
        self.searchTypeCombo.addItem("")
        self.searchTypeCombo.addItem("")
        self.searchTypeCombo.addItem("")
        self.searchTypeCombo.addItem("")
        self.searchTypeCombo.addItem("")
        self.gridLayout.addWidget(self.searchTypeCombo, 1, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 2, 1, 1)
        self.graphDepthSpin = QtWidgets.QSpinBox(Dialog)
        self.graphDepthSpin.setMinimum(1)
        self.graphDepthSpin.setMaximum(99)
        self.graphDepthSpin.setProperty("value", 5)
        self.graphDepthSpin.setObjectName("graphDepthSpin")
        self.gridLayout.addWidget(self.graphDepthSpin, 3, 3, 1, 1)
        self.graphMinDepthSpin = QtWidgets.QSpinBox(Dialog)
        self.graphMinDepthSpin.setMinimum(1)
        self.graphMinDepthSpin.setProperty("value", 1)
        self.graphMinDepthSpin.setObjectName("graphMinDepthSpin")
        self.gridLayout.addWidget(self.graphMinDepthSpin, 4, 3, 1, 1)
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 4, 2, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout)
        self.searchBtn = QtWidgets.QPushButton(Dialog)
        self.searchBtn.setAutoDefault(False)
        self.searchBtn.setDefault(False)
        self.searchBtn.setObjectName("searchBtn")
        self.verticalLayout_5.addWidget(self.searchBtn)
        self.SearchResultTable = QtWidgets.QTableView(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchResultTable.sizePolicy().hasHeightForWidth())
        self.SearchResultTable.setSizePolicy(sizePolicy)
        self.SearchResultTable.setToolTipDuration(1)
        self.SearchResultTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.SearchResultTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.SearchResultTable.setSortingEnabled(False)
        self.SearchResultTable.setCornerButtonEnabled(False)
        self.SearchResultTable.setObjectName("SearchResultTable")
        self.SearchResultTable.horizontalHeader().setCascadingSectionResizes(True)
        self.SearchResultTable.horizontalHeader().setHighlightSections(False)
        self.SearchResultTable.horizontalHeader().setMinimumSectionSize(10)
        self.SearchResultTable.horizontalHeader().setSortIndicatorShown(False)
        self.SearchResultTable.horizontalHeader().setStretchLastSection(False)
        self.SearchResultTable.verticalHeader().setVisible(False)
        self.SearchResultTable.verticalHeader().setCascadingSectionResizes(False)
        self.SearchResultTable.verticalHeader().setHighlightSections(False)
        self.verticalLayout_5.addWidget(self.SearchResultTable)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.retranslateUi(Dialog)
        self.searchTypeCombo.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_3.setText(_translate("Dialog", "Max distance"))
        self.maxDistanceTxt.setText(_translate("Dialog", "50"))
        self.label_4.setText(_translate("Dialog", "Min profit"))
        self.currentSystemTxt.setText(_translate("Dialog", "Sol"))
        self.getCurrentBtn.setText(_translate("Dialog", "Get current"))
        self.label.setText(_translate("Dialog", "Starting system"))
        self.minProfitTxt.setText(_translate("Dialog", "1000"))
        self.profitPhChk.setText(_translate("Dialog", "Cr/h"))
        self.windowCountTxt.setText(_translate("Dialog", "7"))
        self.windowSizeTxt.setText(_translate("Dialog", "200"))
        self.label_6.setText(_translate("Dialog", "Search windows"))
        self.label_2.setText(_translate("Dialog", "Search window size"))
        self.searchTypeCombo.setItemText(0, _translate("Dialog", "Exports from current Station"))
        self.searchTypeCombo.setItemText(1, _translate("Dialog", "Exports from current System"))
        self.searchTypeCombo.setItemText(2, _translate("Dialog", "Loop route"))
        self.searchTypeCombo.setItemText(3, _translate("Dialog", "Long route"))
        self.searchTypeCombo.setItemText(4, _translate("Dialog", "Single trades"))
        self.label_7.setText(_translate("Dialog", "Search Type"))
        self.label_8.setText(_translate("Dialog", "Max hops"))
        self.label_14.setText(_translate("Dialog", "Min hops"))
        self.searchBtn.setText(_translate("Dialog", "Search"))

