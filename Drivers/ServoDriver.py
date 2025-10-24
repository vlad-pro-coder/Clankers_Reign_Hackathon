

#Updated PWM: 50 Hz, 11.2% duty
#Enter freq,duty: 50,1 servo

from SoftwarePWM import SoftwarePWM
import gpiod
from gpiod.line import Direction, Value

class Servo:
    def __init__(self,pwmpin):
        self.pwmpin = pwmpin
        self.chip = "/dev/gpiochip0"
        self.PWM = SoftwarePWM(self.chip,self.pwmpin)
        self.PWM.start()
        self.freq = 50
        self.currentAngle = -1

    def setAngle(self,angle):
        if self.currentAngle == angle:
            return
        self.currentAngle == angle
        procentage = angle / 355.0
        duty = 1 + procentage * (11.2 - 1)
        self.PWM.update(frequency=float(self.freq), duty_cycle=float(duty))

        