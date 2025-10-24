import gpiod
from gpiod.line import Direction, Value
import time

class Encoder:
    def __init__(self, chan_a, chan_b, chip="/dev/gpiochip0", scale=19.89436789):
        """
        Quadrature encoder reader using libgpiod 2.x
        chan_a, chan_b: BCM pin numbers for encoder channels
        chip: path to GPIO chip (default "/dev/gpiochip0")
        scale: value to divide position for your units
        """
        self.chan_a = chan_a
        self.chan_b = chan_b
        self.chip_path = chip
        self.scale = scale
        self.position = 0
        self.currpos = 0
        self.lasttime = 0
        self.lastpos = 0
        self.velocity = 0
        self.prev_state = (Value.ACTIVE, Value.ACTIVE)  # initialize as high

        # Transition table (same as your previous example)
        self.transition = {
            (Value.INACTIVE, Value.INACTIVE, Value.INACTIVE, Value.ACTIVE): +1,
            (Value.INACTIVE, Value.ACTIVE, Value.ACTIVE, Value.ACTIVE): +1,
            (Value.ACTIVE, Value.ACTIVE, Value.ACTIVE, Value.INACTIVE): +1,
            (Value.ACTIVE, Value.INACTIVE, Value.INACTIVE, Value.INACTIVE): +1,
            (Value.INACTIVE, Value.INACTIVE, Value.ACTIVE, Value.INACTIVE): -1,
            (Value.ACTIVE, Value.INACTIVE, Value.ACTIVE, Value.ACTIVE): -1,
            (Value.ACTIVE, Value.ACTIVE, Value.INACTIVE, Value.ACTIVE): -1,
            (Value.INACTIVE, Value.ACTIVE, Value.INACTIVE, Value.INACTIVE): -1,
        }

        # Open GPIO chip and request lines
        self.chip = gpiod.Chip(self.chip_path)
        self.lines = self.chip.request_lines(
            consumer="encoder",
            config={
                self.chan_a: gpiod.LineSettings(direction=Direction.INPUT),
                self.chan_b: gpiod.LineSettings(direction=Direction.INPUT)
            }
        )

    def read(self):
        """Read current encoder state, update position, and return scaled value"""
        a = self.lines.get_value(self.chan_a)
        b = self.lines.get_value(self.chan_b)
        key = self.prev_state + (a, b)
        self.position += self.transition.get(key, 0)
        self.prev_state = (a, b)
        return self.position / self.scale

    def update(self):
        self.currpos = self.read()
        elapsedtime = time.time() - self.lasttime
        self.velocity = (self.currpos - self.lastpos) / elapsedtime

        self.lasttime = time.time()
        self.lastpos = self.currpos



# Example usage
if __name__ == "__main__":
    encoder1 = Encoder(chan_a=17, chan_b=27)#sidewaysa
    encoder2 = Encoder(chan_a=22, chan_b=23)#frontways
    try:
        while True:
            encoder1.update()
            encoder2.update()
            print(encoder1.currpos)
            print(encoder2.currpos)
    except KeyboardInterrupt:
        print("Exiting")
