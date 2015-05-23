from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5
import ui.OptionsUI
import Options as OptionsParams
import EDDB

class Options(ui.OptionsUI.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, db, analyzer, parent = None):
        super(QtWidgets.QDialog, self).__init__(parent)
        self.db = db
        self.analyzer = analyzer

        self.setupUi(self)
        self.closeBtn.clicked.connect(self.onCloseClicked)
        self._readSettings()

        self.ElitePathBtn.clicked.connect(self.onElitePathClicked)
        self.ElitePathTxt.setText(OptionsParams.get("Elite-path", ""))
        self.ElitePathTxt.textEdited.connect(self.onElitePathTxtChanged)

        self.EDCEPathBtn.clicked.connect(self.onEDCEPathClicked)
        self.EDCEPathTxt.setText(OptionsParams.get("EDCE-path", ""))
        self.EDCEPathTxt.textEdited.connect(self.onEDCEPathTxtChanged)

        self.EDDBUpdateIntervalTxt.valueChanged.connect(self.onCheckIntervalChanged)
        self.EDDBUpdateIntervalTxt.setValue(int(OptionsParams.get("EDDB-check-interval", 1)))

        self.MarketValidVal.valueChanged.connect(self.onMarketValidValChanged)
        self.MarketValidVal.setValue(int(OptionsParams.get("Market-valid-days", 7)))

        self.udpateEDDBBtn.clicked.connect(self.onUpdateEDDBNowClicked)

    def onUpdateEDDBNowClicked(self):
        EDDB.update(self.db,True)

    def onCheckIntervalChanged(self):
        OptionsParams.set("EDDB-check-interval", self.EDDBUpdateIntervalTxt.value())

    def onMarketValidValChanged(self):
        OptionsParams.set("Market-valid-days", self.MarketValidVal.value())

    def onCloseClicked(self):
        self.close()

    def _readSettings(self):
        self.restoreGeometry(OptionsParams.get("Options-geometry", QtCore.QByteArray()))

    def closeEvent(self, event):
        OptionsParams.set("Options-geometry", self.saveGeometry())

    def onEDCEPathTxtChanged(self, txt):
        OptionsParams.set("EDCE-path", self.EDCEPathTxt.text())

    def onEDCEPathClicked(self):
        path = self._selectPathDialog("Select EDCE path", self.EDCEPathTxt.text())

        if path is not None:
            self.EDCEPathTxt.setText(path)
            OptionsParams.set("EDCE-path", path)

    def onElitePathTxtChanged(self, txt):
        OptionsParams.set("Elite-path", self.ElitePathTxt.text())
        self.analyzer.setPath(self.ElitePathTxt.text())

    def onElitePathClicked(self):
        path = self._selectPathDialog("Select Elite path", self.ElitePathTxt.text())

        if path is not None:
            self.ElitePathTxt.setText(path)
            OptionsParams.set("Elite-path", path)
            self.analyzer.setPath(self.ElitePathTxt.text())

    def _selectPathDialog(self, origin, title):
        fileDialog = QtWidgets.QFileDialog(self, title, origin)
        fileDialog.setModal(True)
        fileDialog.setFileMode(QtWidgets.QFileDialog.Directory)
        fileDialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly)
        if fileDialog.exec() and len(fileDialog.selectedFiles()) > 0:
            return fileDialog.selectedFiles()[0]
        else:
            return None