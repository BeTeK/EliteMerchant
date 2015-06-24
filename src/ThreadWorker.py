
import threading
import ctypes
import inspect
import sys,traceback

def _async_raise(tid, exctype):
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class ThreadWorker:
    def __init__(self, workFn, finishFn = None):
        self.workFn = workFn
        self.finishFn = finishFn
        self.thread = _Thread(target = self._runner)

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()

    def raiseException(self, ex):
        self.thread.raiseException(ex)

    def terminate(self):
        self.thread.terminate()

    def _runner(self):
        try:
            result = self.workFn()
            if self.finishFn is not None:
                self.finishFn(result)
        except Exception as ex:
            print('Error while executing in thread!')
            # https://docs.python.org/2/library/traceback.html
            print(traceback.format_exc(), file=sys.stderr)
            pass



class _Thread(threading.Thread):
    def raiseException(self, ex):
        if not self.isAlive():
            return

        for tid, tobj in threading._active.items():
            if tobj is self:
                _async_raise(tid, ex)
                return

        # the thread was alive when we entered the loop, but was not found
        # in the dict, hence it must have been already terminated. should we raise
        # an exception here? silently ignore?

    def terminate(self):
        # must raise the SystemExit type, instead of a SystemExit() instance
        # due to a bug in PyThreadState_SetAsyncExc
        self.raiseException(SystemExit)


