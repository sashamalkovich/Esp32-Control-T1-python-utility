
import serial.tools.list_ports

class CheckPorts():
    def __init__(self):
        self.switch = True
        self.iter = 0


    def checkPorts(self):
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        _a = 0
        for i in range(len(myports)):
            stringSpl = myports[i] [1]
            temp = stringSpl.split(' ')
            for match in temp:
                if match == 'CP2102' and self.switch is True and self.iter < 2:
                    _a = i
                    print(myports[_a][0])
                    return myports[_a][0]
                elif match == 'CP2102' and self.switch is False and self.iter < 2:
                    print('Match =>')
                    print(match)
                    self.switch = True
                    continue
                elif match == 'CP2102' and self.switch is True and self.iter >= 2 and self.iter < 4:
                    print('Match =>')
                    print(match)
                    self.switch = False
                    continue
                elif match == 'CP2102' and self.switch is False and self.iter >= 2 and self.iter < 4:
                    print('Match =>')
                    print(match)
                    self.switch = False
                    continue

        print('self.switch => ')
        print(self.switch)


    def switchChange(self):
        if self.switch is True:
            self.switch = False
        self.iter += 1
        if self.iter > 1:
            self.iter = 0

    def reset(self):
        self.iter = 0
        self.switch = True

    def smooth(self, q, bool):
        print(q)
        print(bool)


