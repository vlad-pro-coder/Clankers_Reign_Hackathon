import sys
sys.path.append("../build")

import SmoothBno085
import time
imu = SmoothBno085.SmoothedBNO08x(RefreshFrequency = 100)

while True:
    vel = imu.getVelocity()
    euler = imu.getAngle()
    if euler and vel:
        yaw, pitch, roll = euler
        yawvel, pitchvel, rollvel = vel
        print(f"Yaw vel: {yawvel:.2f}°, Pitch vel: {pitchvel:.2f}°, Roll vel: {rollvel:.2f}°")
        print(f"Yaw: {yaw:.2f}°, Pitch: {pitch:.2f}°, Roll: {roll:.2f}°")

    imu.update()