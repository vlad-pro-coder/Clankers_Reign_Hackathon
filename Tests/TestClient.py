import sys

sys.path.append("../build")

from ClientPhotoSender import ClientPhotoSender

if __name__ == "__main__":
    print("📸 Starting ClientPhotoSender test...")
    sender = ClientPhotoSender()

    try:
        sender.start_sending_packets()
    except KeyboardInterrupt:
        print("\n🛑 Stopping client gracefully...")
