import sys

sys.path.append("../Drivers")
from MotorDriver import Motor

class DriveTrain:
    def __init__(self):
        self.fr = Motor(16,25)
        self.fl = Motor(20,11)
        self.br = Motor(19,9)
        self.bl = Motor(26,8)

        self.bl.SetReverse()
        self.fl.SetReverse()

    def drive(self,x,y,r):
        d = max(abs(x) + abs(y) + abs(r), 1)
        
        fl = (y + x + r) / d
        bl = (y - x + r) / d
        fr = (y - x - r) / d
        br = (y + x - r) / d

        self.fl.setPower(fl)
        self.fr.setPower(fr)
        self.bl.setPower(bl)
        self.br.setPower(br)
