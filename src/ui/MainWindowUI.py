# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\ui\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1465, 1042)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("main.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.currenlyAtSystemTxt = QtWidgets.QLineEdit(self.centralwidget)
        self.currenlyAtSystemTxt.setEnabled(False)
        self.currenlyAtSystemTxt.setReadOnly(False)
        self.currenlyAtSystemTxt.setObjectName("currenlyAtSystemTxt")
        self.horizontalLayout.addWidget(self.currenlyAtSystemTxt)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.currentlyNearAtTxt = QtWidgets.QLineEdit(self.centralwidget)
        self.currentlyNearAtTxt.setEnabled(False)
        self.currentlyNearAtTxt.setObjectName("currentlyNearAtTxt")
        self.horizontalLayout.addWidget(self.currentlyNearAtTxt)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.minPadSizeCombo = QtWidgets.QComboBox(self.centralwidget)
        self.minPadSizeCombo.setObjectName("minPadSizeCombo")
        self.minPadSizeCombo.addItem("")
        self.minPadSizeCombo.addItem("")
        self.minPadSizeCombo.addItem("")
        self.horizontalLayout.addWidget(self.minPadSizeCombo)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.jumpRangeTxt = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jumpRangeTxt.sizePolicy().hasHeightForWidth())
        self.jumpRangeTxt.setSizePolicy(sizePolicy)
        self.jumpRangeTxt.setObjectName("jumpRangeTxt")
        self.horizontalLayout.addWidget(self.jumpRangeTxt)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.cargoSizeTxt = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cargoSizeTxt.sizePolicy().hasHeightForWidth())
        self.cargoSizeTxt.setSizePolicy(sizePolicy)
        self.cargoSizeTxt.setObjectName("cargoSizeTxt")
        self.horizontalLayout.addWidget(self.cargoSizeTxt)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.mainTab = QtWidgets.QTabWidget(self.centralwidget)
        self.mainTab.setObjectName("mainTab")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.mainTab.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.mainTab.addTab(self.tab_2, "")
        self.horizontalLayout_2.addWidget(self.mainTab)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_6.addLayout(self.verticalLayout_2)
        self.statusMessageTxt = QtWidgets.QLabel(self.centralwidget)
        self.statusMessageTxt.setText("")
        self.statusMessageTxt.setObjectName("statusMessageTxt")
        self.verticalLayout_6.addWidget(self.statusMessageTxt)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1465, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.editMenu = QtWidgets.QMenu(self.menubar)
        self.editMenu.setObjectName("editMenu")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.optionsMenu = QtWidgets.QAction(MainWindow)
        self.optionsMenu.setObjectName("optionsMenu")
        self.exitMenu = QtWidgets.QAction(MainWindow)
        self.exitMenu.setObjectName("exitMenu")
        self.searchMenuItem = QtWidgets.QAction(MainWindow)
        self.searchMenuItem.setObjectName("searchMenuItem")
        self.statusMenuItem = QtWidgets.QAction(MainWindow)
        self.statusMenuItem.setObjectName("statusMenuItem")
        self.commodityMenuItem = QtWidgets.QAction(MainWindow)
        self.commodityMenuItem.setObjectName("commodityMenuItem")
        self.menuFile.addAction(self.exitMenu)
        self.editMenu.addAction(self.optionsMenu)
        self.menuView.addAction(self.searchMenuItem)
        self.menuView.addAction(self.statusMenuItem)
        self.menuView.addAction(self.commodityMenuItem)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.editMenu.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        self.minPadSizeCombo.setCurrentIndex(2)
        self.mainTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Elite Merchant"))
        self.label.setText(_translate("MainWindow", "Current System:"))
        self.label_2.setText(_translate("MainWindow", "Current Station:"))
        self.label_3.setText(_translate("MainWindow", "Ship info"))
        self.label_4.setText(_translate("MainWindow", "Min Pad Size:"))
        self.minPadSizeCombo.setItemText(0, _translate("MainWindow", "Any"))
        self.minPadSizeCombo.setItemText(1, _translate("MainWindow", "M"))
        self.minPadSizeCombo.setItemText(2, _translate("MainWindow", "L"))
        self.label_5.setText(_translate("MainWindow", "Jump Range:"))
        self.jumpRangeTxt.setText(_translate("MainWindow", "16"))
        self.label_6.setText(_translate("MainWindow", "Cargo space:"))
        self.cargoSizeTxt.setText(_translate("MainWindow", "100"))
        self.mainTab.setTabText(self.mainTab.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.mainTab.setTabText(self.mainTab.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.editMenu.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.optionsMenu.setText(_translate("MainWindow", "Options"))
        self.exitMenu.setText(_translate("MainWindow", "Exit"))
        self.searchMenuItem.setText(_translate("MainWindow", "Add Search"))
        self.statusMenuItem.setText(_translate("MainWindow", "Add Status"))
        self.commodityMenuItem.setText(_translate("MainWindow", "Add Commodity search"))

