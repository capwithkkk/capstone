from singleton import SingletonInstance
import datetime
import traceback
import sys


class BaseWriter(SingletonInstance):

    def __init__(self, filename):
        self.file = filename

    def append(self, string: str):
        self.io_append(string)

    def io_append(self, string: str):
        file = open(self.file,"a",encoding='utf8')
        file.write(string + "\n")
        file.close()

    def append_exception(self, exception: Exception):
        pass


class LogWriter(BaseWriter):

    def __init__(self):
        BaseWriter.__init__(self, "./Log.txt")

    def append(self, string: str):
        date = datetime.datetime.now()
        date_str_form = date.strftime('%Y-%m-%d %H:%M:%S')
        self.io_append(string + "(" + date_str_form + ")\n===============================================\n")


class ExceptionWriter(LogWriter):

    def __init__(self):
        BaseWriter.__init__(self, "./Exceptions.txt")

    def append_exception(self, exception: Exception):
        self.append("Exceptions: " + str(exception.args) + " traceback : " + traceback.format_exc() + "\n")


class SubstitutionTrialWriter(BaseWriter):

    def __init__(self):
        BaseWriter.__init__(self, "./subTrial.txt")
        self.set = set()
        self.append("전체")
        self.io_load()

    def append(self, string: str):
        size = len(self.set)
        self.set.add(string)
        if len(self.set) > size:
            self.io_append(string)

    def delete(self, string: str):
        size = len(self.set)
        self.set.remove(string)
        if len(self.set) < size:
            self.io_write()

    def io_load(self):
        file = open(self.file, "r", encoding='utf8')
        while True:
            line = file.readline()
            if not line:
                break
            self.set.add(line[:-1])
        file.close()

    def io_write(self):
        file = open(self.file, "w", encoding='utf8')
        file.truncate()
        for item in self.set:
            file.write(item + "\n")
        file.close()
