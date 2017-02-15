arr = [1, 2, 3]

class Machine:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def gettpm(self):
        return self.tpm

    def talk(self):
        return "I am a" + self.getName()

class Cyborg(Machine):

    tpm = {}

    def __init__(self, name):
        self.name = name

    def getName(self):
        return Machine.getName(self)

    def change_array(self):
        for num in arr:
            print(num)



a = Machine("paul")
b = Cyborg("george")