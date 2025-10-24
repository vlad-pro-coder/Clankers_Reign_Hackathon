import sys

sys.path.append("../Drivers")

from ServoDriver import Servo

if __name__ == "__main__":
    pin = int(input("Enter GPIO pin (BCM number): "))
    servo = Servo(pin)
    print("PWM running. Enter new frequency and duty cycle anytime (or CTRL+C to stop).")

    try:
        while True:
            user_input = int(input("enter angle: "))
            servo.setAngle(user_input)
    except KeyboardInterrupt:
        print("\nStopping PWM...")