import gpiod
import time
import threading
from gpiod.line import Direction, Value

class SoftwarePWM:
    def __init__(self, chip_path, pin, frequency=1000, duty_cycle=50):
        self.chip_path = chip_path
        self.pin = pin
        self.frequency = frequency
        self.duty_cycle = duty_cycle
        self._running = False
        self._lock = threading.Lock()

        self.request = gpiod.request_lines(
            self.chip_path,
            consumer="pwm",
            config={self.pin: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)}
        )

    def start(self):
        self._running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        while self._running:
            with self._lock:
                period = 1.0 / self.frequency
                on_time = period * (self.duty_cycle / 100)
                off_time = period - on_time

            self.request.set_value(self.pin, Value.ACTIVE)
            time.sleep(on_time)
            self.request.set_value(self.pin, Value.INACTIVE)
            time.sleep(off_time)

    def update(self, frequency=None, duty_cycle=None):
        with self._lock:
            if frequency is not None:
                self.frequency = frequency
            if duty_cycle is not None:
                self.duty_cycle = duty_cycle

    def stop(self):
        self._running = False
        self.thread.join()
        self.request.set_value(self.pin, Value.INACTIVE)