from SoftwarePWM import SoftwarePWM
import gpiod
from gpiod.line import Direction, Value

class Motor:
    def __init__(self, pwmpin, reversepin):
        self.pwmpin = pwmpin
        self.reversepin = reversepin
        self.chip = "/dev/gpiochip0"
        self.PWM = SoftwarePWM(self.chip, self.pwmpin)
        self.freq = 1000
        self.direct = 1

        self.direction = False
        self.dictdirection = {
            False: Value.INACTIVE,
            True: Value.ACTIVE,
        }
        self.currentPower = -2

        self.directionrequest = gpiod.request_lines(
            self.chip,
            consumer="direction",
            config={
                self.reversepin: gpiod.LineSettings(
                    direction=Direction.OUTPUT,
                    output_value=Value.INACTIVE
                )
            }
        )

        # ✅ Start PWM thread here
        self.PWM.start()

        # Initialize power to 0
        self.setPower(0)

    def __del__(self):
        self.PWM.stop()

    def setPower(self, power):
        # Avoid redundant updates
        power = self.direct * power
        if self.currentPower == power:
            return

        self.currentPower = power

        if power == 0:
            self.PWM.stop()
            self.PWM.request.set_value(self.pwmpin, Value.INACTIVE)
            return
        else:
            if not self.PWM._running:
                self.PWM.start()

        # Direction control
        if power <= 0:
            self.directionrequest.set_value(
                self.reversepin, self.dictdirection[not self.direction])
        else:
            self.directionrequest.set_value(
                self.reversepin, self.dictdirection[self.direction])

        # PWM update
        self.PWM.update(
            frequency=float(self.freq),
            duty_cycle=abs(float(power) * 100)
        )

    def ChangeDirection(self):
        self.direction = not self.direction

    def SetForward(self):
        self.direct = 1
    def SetReverse(self):
        self.direct = -1


        