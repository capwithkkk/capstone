from threading import Lock


def synchronized(method):
    def new_synchronized_method(self, *args, **kwargs):
        if not hasattr(self, "_auto_lock"):
            self._auto_lock = Lock()
        with self._auto_lock:
            return method(self, *args, **kwargs)
    return new_synchronized_method