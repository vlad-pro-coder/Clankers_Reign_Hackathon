import time

class HardwarePWM:
    def __init__(self, pwm_chip=0, pwm_channel=0, frequency=50):
        self.pwm_chip = pwm_chip
        self.pwm_channel = pwm_channel
        self.frequency = frequency
        self.base_path = f"/sys/class/pwm/pwmchip{self.pwm_chip}"
        self.pwm_path = f"{self.base_path}/device/pwm{self.pwm_channel}"
        self.period_ns = int(1e9 / self.frequency)  # period in nanoseconds

        # Export the PWM channel
        self._write_file(f"{self.base_path}/export", self.pwm_channel)
        time.sleep(0.1)  # wait for sysfs to create files

        # Set the PWM period
        self._write_file(f"{self.pwm_path}/period", self.period_ns)

        # Enable PWM
        self._write_file(f"{self.pwm_path}/enable", 1)

    def _write_file(self, path, value):
        with open(path, "w") as f:
            f.write(str(value))

    def set_duty_cycle_percent(self, duty_percent):
        """Set duty cycle in percent (0–100%)"""
        if duty_percent < 0 or duty_percent > 100:
            raise ValueError("Duty cycle must be 0–100%")
        duty_ns = int(self.period_ns * duty_percent / 100)
        self._write_file(f"{self.pwm_path}/duty_cycle", duty_ns)

    def cleanup(self):
        """Disable PWM and unexport"""
        self._write_file(f"{self.pwm_path}/enable", 0)
        self._write_file(f"{self.base_path}/unexport", self.pwm_channel)


# -----------------------
# Example usage in console
# -----------------------
if __name__ == "__main__":
    pwm = HardwarePWM(pwm_chip=0, pwm_channel=0, frequency=50)

    try:
        while True:
            duty = input("Enter duty cycle (0-100%): ")
            try:
                duty = float(duty)
                pwm.set_duty_cycle_percent(duty)
                print(f"Duty cycle set to {duty}%")
            except ValueError:
                print("Invalid input! Enter a number between 0 and 100.")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        pwm.cleanup()
