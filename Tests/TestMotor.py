import sys

sys.path.append("../Drivers")

from MotorDriver import Motor

if __name__ == "__main__":
    pin = int(input("enter pwm pin: "))
    pindir = int(input("enter direction pin: "))
    motor = Motor(pin,pindir)
    print("PWM running. Enter new frequency and duty cycle anytime (or CTRL+C to stop).")

    try:
        while True:
            user_input = float(input("enter power: "))
            motor.setPower(user_input)
    except KeyboardInterrupt:
        print("\nStopping PWM...")

#front right pin 16 dir 25
#front left pin 20 dir 11
#back right pin 19 dir 9
#back left pin 26 dir 8