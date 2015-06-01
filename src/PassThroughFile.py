
class PassThroughFile:
    def __init__(self, file):
        self.file = file
        self.listeners = []
        self.lastLine = ""

    def addListener(self, fn):
        self.listeners.append(fn)

    def close(self):
        self.file.close()

    def flush(self):
        self.file.flush()

    def write(self, txt):
        self.file.write(txt)
        self.lastLine += txt
        self._alertListeners()

    def _alertListeners(self):
        pos = self.lastLine.find("\n")
        if pos < 0:
            return

        line = self.lastLine[:pos]
        self.lastLine = self.lastLine[pos + 1:]

        for i in self.listeners:
            i(line)

        self._alertListeners()
