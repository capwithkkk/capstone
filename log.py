from singleton import SingletonInstance


class SubstitutionTrialWriter(SingletonInstance):

    def __init__(self):
        self.substitution_trial_list_file = "./subTrial.txt"
        self.set = set(["전체"])
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
        file = open(self.substitution_trial_list_file,"r")
        while True:
            line = file.readline()
            if not line:
                break
            self.set.add(line[:-1])
        file.close()

    def io_append(self, string: str):
        file = open(self.substitution_trial_list_file,"a")
        file.write(string + "\n")
        file.close()

    def io_write(self):
        file = open(self.substitution_trial_list_file,"w")
        file.truncate()
        for item in self.set:
            file.write(item + "\n")
        file.close()
