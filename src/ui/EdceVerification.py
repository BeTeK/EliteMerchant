from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5
import ui.EdceVerificationUI
import Options as OptionsParams
import EDDB

class EdceVerification(ui.EdceVerificationUI.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, parent):
        super(QtWidgets.QDialog, self).__init__(parent)

        self.setupUi(self)
        self.okBtn.clicked.connect(self._onOkClicked)
        self.cancelBtn.clicked.connect(self._onCancelClicked)
        self._readSettings()
        self.result = None

    def _readSettings(self):
        self.restoreGeometry(OptionsParams.get("edce-verification-geometry", QtCore.QByteArray()))

    def closeEvent(self, event):
        OptionsParams.set("edce-verification-geometry", self.saveGeometry())

    def getResult(self):
        return self.result

    def _onOkClicked(self):
        self.result = self.verificationCodeTxt.text()
        self.close()

    def _onCancelClicked(self):
        self.close()