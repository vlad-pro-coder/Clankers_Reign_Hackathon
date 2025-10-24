# TestCamera.py
import sys
import time
import numpy as np

# Add build folder if needed
sys.path.append("../build")  # adjust if your compiled module is in build/

from RaspGSCamera import RaspGSCamera  # import the compiled class
from SmoothBno085 import SmoothedBNO08x

def main():
    cam = RaspGSCamera(width=1456, height=1088, calib_file=b"../camera_calibration.npz")
    try:
        # Initialize camera
        print("Camera started successfully")

        # Print camera intrinsics
        fx, fy, cx, cy = cam.getIntrinsics()
        print(f"Camera intrinsics: fx={fx}, fy={fy}, cx={cx}, cy={cy}")

        # Capture 10 frames and display their shapes
        for i in range(1):
            img = cam.capture_mat()
            print(f"Frame {i+1}: shape={img.shape}, dtype={img.dtype}")
            time.sleep(0.1)

        # Capture a JPEG
        jpeg_bytes = cam.capture_jpeg(quality=90)
        if jpeg_bytes:
            print(f"JPEG captured, size={len(jpeg_bytes)} bytes")
            # Optionally save to file
            with open("frame.jpg", "wb") as f:
                f.write(jpeg_bytes)
            print("Saved frame.jpg")

    except Exception as e:
        print("Error:", e)

    finally:
        # Stop camera
        cam.stop()
        print("Camera stopped")

if __name__ == "__main__":
    main()