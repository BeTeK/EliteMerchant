# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\ui\CommodityTab.ui'
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
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.currentSystemCombo = QtWidgets.QComboBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.currentSystemCombo.sizePolicy().hasHeightForWidth())
        self.currentSystemCombo.setSizePolicy(sizePolicy)
        self.currentSystemCombo.setEditable(True)
        self.currentSystemCombo.setMaxVisibleItems(100)
        self.currentSystemCombo.setObjectName("currentSystemCombo")
        self.horizontalLayout_3.addWidget(self.currentSystemCombo)
        self.getCurrentBtn = QtWidgets.QPushButton(Dialog)
        self.getCurrentBtn.setObjectName("getCurrentBtn")
        self.horizontalLayout_3.addWidget(self.getCurrentBtn)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 3, 1, 1)
        self.importComboBox = QtWidgets.QComboBox(Dialog)
        self.importComboBox.setObjectName("importComboBox")
        self.importComboBox.addItem("")
        self.importComboBox.addItem("")
        self.gridLayout.addWidget(self.importComboBox, 2, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 5, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)
        self.commodityCombobox = QtWidgets.QComboBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commodityCombobox.sizePolicy().hasHeightForWidth())
        self.commodityCombobox.setSizePolicy(sizePolicy)
        self.commodityCombobox.setEditable(True)
        self.commodityCombobox.setMaxVisibleItems(100)
        self.commodityCombobox.setObjectName("commodityCombobox")
        self.gridLayout.addWidget(self.commodityCombobox, 2, 3, 1, 1)
        self.maxDistanceSpinBox = QtWidgets.QSpinBox(Dialog)
        self.maxDistanceSpinBox.setMinimumSize(QtCore.QSize(75, 0))
        self.maxDistanceSpinBox.setMaximum(99999999)
        self.maxDistanceSpinBox.setProperty("value", 100)
        self.maxDistanceSpinBox.setObjectName("maxDistanceSpinBox")
        self.gridLayout.addWidget(self.maxDistanceSpinBox, 1, 6, 1, 1)
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
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.currentSystemCombo, self.getCurrentBtn)
        Dialog.setTabOrder(self.getCurrentBtn, self.commodityCombobox)
        Dialog.setTabOrder(self.commodityCombobox, self.importComboBox)
        Dialog.setTabOrder(self.importComboBox, self.maxDistanceSpinBox)
        Dialog.setTabOrder(self.maxDistanceSpinBox, self.searchBtn)
        Dialog.setTabOrder(self.searchBtn, self.SearchResultTable)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Starting system"))
        self.getCurrentBtn.setText(_translate("Dialog", "Get current"))
        self.importComboBox.setItemText(0, _translate("Dialog", "Imports"))
        self.importComboBox.setItemText(1, _translate("Dialog", "Exports"))
        self.label_2.setText(_translate("Dialog", "Max distance"))
        self.label_4.setText(_translate("Dialog", "Commodity"))
        self.searchBtn.setText(_translate("Dialog", "Search"))

