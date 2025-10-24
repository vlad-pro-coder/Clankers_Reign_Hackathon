import sys

sys.path.append("../Drivers")
from MotorDriver import Motor

class DriveTrain:
    def __init__(self):
        self.fr = Motor(16, 25)
        self.fl = Motor(20, 11)

        self.fl.SetReverse()  # Reverse one side if needed for forward motion

    def drive(self, x, y, r):
        # Normalize motor power
        d = max(abs(x) + abs(y) + abs(r), 1)

        # Compute motor powers (mecanum-style logic but using only front motors)
        fl = (y + x + r) / d
        fr = (y - x - r) / d

        # Apply power to front motors only
        self.fl.setPower(fl)
        self.fr.setPower(fr)
