import time
from types import TracebackType


class Repeater:

    CONST_TIMEOUT = 0.3

    @staticmethod
    def repeat_procedure(func: callable(object), params: tuple, exception: TracebackType, failure_count: int):
        while True:
            try:
                func(*params)
            except exception as e:
                if failure_count is 0:
                    raise e
                failure_count -= 1
                time.sleep(Repeater.CONST_TIMEOUT)
                continue
            finally:
                return None

    @staticmethod
    def repeat_function(func: callable(object), params: tuple, exception: TracebackType, failure_count: int):
        while True:
            try:
                out = func(*params)
                return out
            except exception as e:
                if failure_count is 0:
                    raise e
                failure_count -= 1
                time.sleep(Repeater.CONST_TIMEOUT)
                continue

