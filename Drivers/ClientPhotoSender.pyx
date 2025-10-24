import socket
import struct
import cv2
import numpy as np
import time
import sys
from types import SimpleNamespace
sys.path.append("build")
from RaspGSCamera import RaspGSCamera

class ClientPhotoSender():
    def __init__(self):
        self.camera = RaspGSCamera()
        self.HEADER_FMT = "!I"
        focal_x , focal_y, cx, cy = self.camera.getIntrinsics()
        self.intrinsics = np.array([focal_x, focal_y, cx, cy], dtype=np.float32)
        self.result = []

    def __pack_message(self,data_bytes: bytes) -> bytes:
        return struct.pack(self.HEADER_FMT, len(data_bytes)) + data_bytes

    def __recv_message(self,sock: socket.socket) -> bytes:
        hdr = b""
        while len(hdr) < 4:
            chunk = sock.recv(4 - len(hdr))
            if not chunk:
                raise ConnectionError("Connection closed while reading header")
            hdr += chunk
        (length,) = struct.unpack(self.HEADER_FMT, hdr)
        data = b""
        while len(data) < length:
            chunk = sock.recv(length - len(data))
            if not chunk:
                raise ConnectionError("Connection closed while reading payload")
            data += chunk
        return data

    def start_sending_packets(self):
        args = SimpleNamespace(
            host="192.168.110.191",#to do: wireless connection
            port=5001,
        )

        # Example intrinsics values
        focal_x , focal_y, cx, cy = self.camera.getIntrinsics()
        intrinsics = np.array([focal_x, focal_y, cx, cy], dtype=np.float32)

        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    print(f"Connecting to server {args.host}:{args.port}...")
                    s.connect((args.host, args.port))
                    print("Connected. Sending intrinsics...")

                    # send intrinsics first
                    s.sendall(self.__pack_message(intrinsics.tobytes()))

                    print("Sent intrinsics. Starting to send images...")
                    if True:
                        image = self.camera.capture_mat()
                        success, jpg = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                        if not success:
                            print("Failed to encode image, skipping...")
                            continue
                        img_bytes = jpg.tobytes()
                        s.sendall(self.__pack_message(img_bytes))
                        #print(f"Sent image ({len(img_bytes)} bytes)")
                        data_bytes = self.__recv_message(s)
                        arr = np.frombuffer(data_bytes, dtype=np.float32)
                        self.result = arr.reshape(-1, 2).tolist()
                        break

            except (ConnectionRefusedError, OSError):
                print("Server not available. Retrying in 3 seconds...")
                time.sleep(3)
            except Exception as e:
                print("Error:", e)
                time.sleep(3)