import sys
import threading
import time
from math import fmod

sys.path.append("../Components")
sys.path.append("../build")

import SmoothBno085
from DriveTrain import DriveTrain
from MotorDriver import Motor  # Assuming you have this class

# --- Helper functions ---
def getAngleDifference(target, current):
    diff = fmod(target - current + 180.0, 360.0)
    if diff < 0:
        diff += 360.0
    return diff - 180.0

# --- Global variables ---
Target = 10
kP = -0.025
kP_lock = threading.Lock()
imu = SmoothBno085.SmoothedBNO08x(RefreshFrequency=100)

# --- Background input thread ---
def read_kp_input():
    global kP
    while True:
        try:
            value = input("Enter new kP value: ")
            if value.strip() == "":
                continue
            new_kp = float(value)
            with kP_lock:
                kP = new_kp
            print(f"✅ Updated kP = {kP}")
            
        except ValueError:
            print("⚠️ Invalid number. Try again.")
        except KeyboardInterrupt:
            break

# --- Main control ---
if __name__ == "__main__":
    
    dt = DriveTrain()

    # Start input thread
    threading.Thread(target=read_kp_input, daemon=True).start()

    print("Running... (press Ctrl+C to stop)")
    try:
        while True:
            yaw = imu.getAngle()[0]
            with kP_lock:
                current_kp = kP

            difference = getAngleDifference(Target, yaw)
            dt.drive(0, 0, difference * current_kp)
            imu.update()
            time.sleep(0.02)
            print("imu data",yaw)

    except KeyboardInterrupt:
        dt.drive(0, 0, 0)
        print("\n🛑 Stopping robot.")
