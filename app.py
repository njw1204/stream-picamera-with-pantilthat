from server import main as server
from camera_dev import CameraDevice
import threading

if __name__ == '__main__':
    try:
        CameraDevice.start()
        if CameraDevice.state():
            t = threading.Thread(target=server.run)
            t.start()
        else:
            print("Can't open camera.")
    finally:
        CameraDevice.stop()