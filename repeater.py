import time


class Repeater:

    @staticmethod
    def repeat_procedure(func, params: tuple, exception: Exception, failure_count: int):
        while True:
            try:
                func(*params)
            except exception as e:
                if failure_count is 0:
                    raise e
                failure_count -= 1
                time.sleep(0.1)
                continue
            finally:
                return None

    @staticmethod
    def repeat_function(func, params: tuple, exception: Exception, failure_count: int) -> object:
        while True:
            try:
                return func(*params)
            except exception as e:
                if failure_count is 0:
                    raise e
                failure_count -= 1
                time.sleep(0.1)
                continue

