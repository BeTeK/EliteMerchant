from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5
import ui.OptionsUI
import ui.EdceVerification
import Options as OptionsParams
import EDDB
import EdceWrapper
import time
import traceback

class Options(ui.OptionsUI.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, db, analyzer, parent = None):
        super(QtWidgets.QDialog, self).__init__(parent)
        self.db = db
        self.analyzer = analyzer

        self.setupUi(self)

        self.mainwindow=parent

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

        self.usernameTxt.textEdited.connect(self.onUsernameEdited)
        self.usernameTxt.setText(OptionsParams.get("elite-username", ""))

        self.passwordTxt.textEdited.connect(self.onPasswordEdited)
        self.passwordTxt.setText(OptionsParams.get("elite-password", ""))

        self.soundStartupTxt.setText(OptionsParams.get("sounds-startup", "sounds/startup.wav"))
        self.soundStartupTxt.textEdited.connect(self.onSoundsChanged)
        self.soundStartupBtn.clicked.connect(self.onSoundStartupClicked)
        self.soundSearchTxt.setText(OptionsParams.get("sounds-search", "sounds/search.wav"))
        self.soundSearchTxt.textEdited.connect(self.onSoundsChanged)
        self.soundSearchBtn.clicked.connect(self.onSoundSearchClicked)
        self.soundErrorTxt.setText(OptionsParams.get("sounds-error", "sounds/error.wav"))
        self.soundErrorTxt.textEdited.connect(self.onSoundsChanged)
        self.soundErrorBtn.clicked.connect(self.onSoundErrorClicked)
        self.soundEnabledChk.setChecked( OptionsParams.get("sounds-enabled", "0")=="1" )
        self.soundEnabledChk.stateChanged.connect(self.onSoundsChanged)
        self.soundVolumeSlider.setValue( int(OptionsParams.get("sounds-volume", 100)) )
        self.soundVolumeSlider.sliderReleased.connect(self.onSoundsChanged)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._onTimerEvent)
        self.timer.start(1000)

        self.testEdceBtn.clicked.connect(self.onTestEdceConnectionClicked)
        self.verificationCode = None
        self.startVerification = False
        self.edceWrapper = None


    def onTestEdceConnectionClicked(self):
        path = OptionsParams.get("EDCE-path", "")
        try:
            self.edceConnectionStatusTxt.setText("Testing connection...")
            self.edceWrapper = EdceWrapper.EdceWrapper(path, self.db, self._verificationCheck)
            self.edceWrapper.fetchNewInfo()
        except Exception as ex:
            self.edceConnectionStatusTxt.setText(str(ex))

    def _onTimerEvent(self):
        if self.startVerification:
            self.startVerification = False
            result = self._showVerificationDialog()
            if result is None:
                result = ""
            self.verificationCode = result


        if self.edceWrapper is not None and not self.edceWrapper.isActive():
            try:
                self.edceWrapper.updateResults()
                fail = self.edceWrapper.isDisabled()
                if fail is not None:
                    raise fail

                self.edceConnectionStatusTxt.setText("EDCE connection is working")
                self.edceWrapper = None

            except Exception as ex:
                self.edceConnectionStatusTxt.setText(str(ex))

    def _verificationCheck(self):
        self.startVerification = True
        while self.verificationCode is None:
            time.sleep(0.1)

        code = self.verificationCode
        self.verificationCode = None
        return code

    def _showVerificationDialog(self):
        dialog = ui.EdceVerification.EdceVerification(self)
        dialog.setModal(True)
        dialog.exec()
        return dialog.getResult()

    def onSoundStartupClicked(self):
        path = self._selectFileDialog("Select Sound", self.soundStartupTxt.text(),"Sounds (*.wav)")
        if path is not None:
            self.soundStartupTxt.setText(path)
            OptionsParams.set("sounds-startup", path)

    def onSoundSearchClicked(self):
        path = self._selectFileDialog("Select Sound", self.soundSearchTxt.text(),"Sounds (*.wav)")
        if path is not None:
            self.soundSearchTxt.setText(path)
            OptionsParams.set("sounds-search", path)

    def onSoundErrorClicked(self):
        path = self._selectFileDialog("Select Sound", self.soundErrorTxt.text(),"Sounds (*.wav)")
        if path is not None:
            self.soundErrorTxt.setText(path)
            OptionsParams.set("sounds-error", path)

    def onSoundsChanged(self):
        OptionsParams.set("sounds-startup", self.soundStartupTxt.text() )
        OptionsParams.set("sounds-search",self.soundSearchTxt.text() )
        OptionsParams.set("sounds-error",self.soundErrorTxt.text() )
        OptionsParams.set("sounds-enabled", self.soundEnabledChk.isChecked() and "1" or "0" )
        OptionsParams.set("sounds-volume", self.soundVolumeSlider.value() )
        if self.mainwindow is not None:
          self.mainwindow.sounds.refreshSounds()

    def onUsernameEdited(self):
        OptionsParams.set("elite-username", self.usernameTxt.text())

    def onPasswordEdited(self):
        OptionsParams.set("elite-password", self.passwordTxt.text())

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

    def _selectPathDialog(self, title, origin):
        fileDialog = QtWidgets.QFileDialog(self, title, origin)
        fileDialog.setModal(True)
        fileDialog.setFileMode(QtWidgets.QFileDialog.Directory)
        fileDialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly)
        if fileDialog.exec() and len(fileDialog.selectedFiles()) > 0:
            return fileDialog.selectedFiles()[0]
        else:
            return None

    def _selectFileDialog(self, title, origin,filterstring):
        fileDialog = QtWidgets.QFileDialog(self, title, origin,filterstring)
        fileDialog.setModal(True)
        if fileDialog.exec() and len(fileDialog.selectedFiles()) > 0:
            return fileDialog.selectedFiles()[0]
        else:
            return None

