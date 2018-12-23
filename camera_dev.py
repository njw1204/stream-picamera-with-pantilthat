from threading import Thread, Lock
import cv2, time

class CameraDevice:
    CAMERA_INDEX = 0
    WIDTH = 480
    HEIGHT = 320

    device = None
    thread = None
    threadOn = False
    lock = Lock()
    readVal, readData = False, None
    frameCnt = 0

    @classmethod
    def start(cls):
        with cls.lock:
            if cls.device is None or not cls.device.isOpened():
                cls.readVal, cls.readData = False, None
                cls.device = cv2.VideoCapture(cls.CAMERA_INDEX)
                if cls.device is not None and cls.device.isOpened():
                    cls.device.set(cv2.CAP_PROP_FRAME_WIDTH, cls.WIDTH)
                    cls.device.set(cv2.CAP_PROP_FRAME_HEIGHT, cls.HEIGHT)
                    # cls.thread = Thread(target=cls.update)
                    # cls.threadOn = True
                    # cls.frameCnt = 0
                    # cls.thread.start()

    @classmethod
    def stop(cls):
        with cls.lock:
            try:
                cls.readVal, cls.readData = False, None
                cls.threadOn = False
                cls.device.release()
            except:
                pass
            finally:
                cls.thread = None
                cls.device = None

    @classmethod
    def state(cls):
        with cls.lock:
            if cls.device is not None and cls.device.isOpened():
                return True
            else:
                return False

    @classmethod
    def update_thread_loop(cls):
        # currently not used
        while cls.threadOn:
            try:
                cls.readVal, cls.readData = cls.device.read()
            except:
                cls.readVal, cls.readData = False, None
            finally:
                cls.frameCnt += 1

    @classmethod
    def read_from_thread_loop(cls):
        # currently not used
        tempFrameCnt = cls.frameCnt
        while tempFrameCnt == cls.frameCnt:
            time.sleep(0)
        return cls.readVal, cls.readData