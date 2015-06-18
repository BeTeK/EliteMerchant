# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\ui\UpdateTab.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(813, 688)
        self.gridLayout_3 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.versionlinkTextBrowser = QtWidgets.QTextBrowser(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionlinkTextBrowser.sizePolicy().hasHeightForWidth())
        self.versionlinkTextBrowser.setSizePolicy(sizePolicy)
        self.versionlinkTextBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.versionlinkTextBrowser.setFrameShadow(QtWidgets.QFrame.Plain)
        self.versionlinkTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.versionlinkTextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.versionlinkTextBrowser.setOpenExternalLinks(True)
        self.versionlinkTextBrowser.setObjectName("versionlinkTextBrowser")
        self.gridLayout_7.addWidget(self.versionlinkTextBrowser, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_7, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.versionlinkTextBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"data:image/jpeg;base64,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\" /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">Elite Merchant update available!</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:24pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Your current version is:</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">v%currentversionstring%</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">The new version is:</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">v%versionstring%</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Click below to download the latest installer:<br /></span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"%newversionlinkstring%\"><span style=\" font-size:14pt; text-decoration: underline; color:#0000ff;\">%newversionlinkstring%</span></a></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Or you can head to our GitHub page to see what\'s up</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://github.com/BeTeK/EliteMerchant\"><span style=\" font-size:14pt; text-decoration: underline; color:#0000ff;\">https://github.com/BeTeK/EliteMerchant</span></a></p></body></html>"))

