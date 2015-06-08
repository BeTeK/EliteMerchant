
import threading

class ThreadWorker:
    def __init__(self, workFn, finishFn = None):
        self.workFn = workFn
        self.finishFn = finishFn
        self.thread = threading.Thread(target = self._runner)

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()

    def _runner(self):
        result = self.workFn()
        if self.finishFn is not None:
            self.finishFn(result)






