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
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
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
        self.statusMessageTxt = QtWidgets.QLabel(self.centralwidget)
        self.statusMessageTxt.setText("")
        self.statusMessageTxt.setObjectName("statusMessageTxt")
        self.horizontalLayout_2.addWidget(self.statusMessageTxt)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_6.addLayout(self.verticalLayout_2)
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
        self.menuFile.addAction(self.exitMenu)
        self.editMenu.addAction(self.optionsMenu)
        self.menuView.addAction(self.searchMenuItem)
        self.menuView.addAction(self.statusMenuItem)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.editMenu.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        self.mainTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Elite Merchant"))
        self.mainTab.setTabText(self.mainTab.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.mainTab.setTabText(self.mainTab.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.editMenu.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.optionsMenu.setText(_translate("MainWindow", "Options"))
        self.exitMenu.setText(_translate("MainWindow", "Exit"))
        self.searchMenuItem.setText(_translate("MainWindow", "Add Search"))
        self.statusMenuItem.setText(_translate("MainWindow", "Add Status"))

