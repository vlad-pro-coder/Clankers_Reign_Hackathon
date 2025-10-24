import sys
sys.path.append("../Components")

from DriveTrain import DriveTrain

dt = DriveTrain()

print("Enter x y rot values between -1 and 1 (Ctrl+C to exit)")

try:
    while True:
        user_input = input("x y rot: ").strip()
        if not user_input:
            continue

        try:
            x_str, y_str, rot_str = user_input.split()
            x = float(x_str)
            y = float(y_str)
            rot = float(rot_str)
        except ValueError:
            print("❌ Invalid input. Format: x y rot (example: 0.5 -0.2 0)")
            continue

        dt.drive(x, y, rot)
        print(f"→ Driving with x={x}, y={y}, rot={rot}")

except KeyboardInterrupt:
    print("\n🛑 Stopping motors...")
    dt.drive(0, 0, 0)
    print("✅ Motors stopped.")
