from flask import Response, request, abort
from _thread import get_ident
from .setting import serverConfig, streamConfig
from .tokenManager import Auth
from camera_dev import CameraDevice
import cv2, threading, time

class LiveVideo:
    placeholder = cv2.imencode('.jpg',
                               cv2.resize(cv2.imread(streamConfig.PLACEHOLDER),
                                          (CameraDevice.WIDTH, CameraDevice.HEIGHT),
                                          interpolation=cv2.INTER_AREA))[1].tobytes()
    thread = None
    frame = None
    frameId = 0
    lastTime = 0
    lock = threading.Lock()
    signal = dict()

    @classmethod
    def StartThread(cls):
        with cls.lock:
            if cls.thread is None:
                cls.lastTime = time.time()
                cls.thread = threading.Thread(target=cls.CaptureTask)
                cls.thread.start()
                cls.EventWait()
                cls.EventClear()

    @classmethod
    def GetFrame(cls):
        cls.lastTime = time.time()
        cls.EventWait()
        cls.EventClear()
        if cls.frameId == -1:
            return cls.placeholder
        else:
            return cls.frame

    @classmethod
    def CaptureTask(cls):
        while True:
            try:
                ret, img = CameraDevice.device.read()
                img = cv2.flip(img, 0)
                cls.frame = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, streamConfig.QUALITY])[1].tobytes()
                cls.frameId = 1
            except:
                cls.frameId = -1
            finally:
                cls.EventSet()
                time.sleep(0.04)
                if streamConfig.TIMEOUT > 0 and time.time() - cls.lastTime > streamConfig.TIMEOUT:
                    cls.frame = None
                    cls.frameId = 0
                    cls.thread = None
                    break

    @classmethod
    def EventSet(cls):
        nowTime = time.time()
        rm = None
        for id, ev in cls.signal.items():
            if not ev[0].isSet():
                ev[0].set()
                ev[1] = nowTime
            elif nowTime - ev[1] > streamConfig.THREAD_TIMEOUT:
                rm = id
        if rm:
            del cls.signal[rm]

    @classmethod
    def EventWait(cls):
        ident = get_ident()
        if ident not in cls.signal:
            cls.signal[ident] = [threading.Event(), time.time()]
        cls.signal[ident][0].wait()

    @classmethod
    def EventClear(cls):
        cls.signal[get_ident()][0].clear()


def GenVideo():
    for _ in range(2):
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + LiveVideo.placeholder + b'\r\n'

    if LiveVideo.thread is None:
        LiveVideo.StartThread()

    while True:
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + LiveVideo.GetFrame() + b'\r\n'


def Stream():
    streamHeaders = [i for i in serverConfig.DEFAULT_RESPONSE_HEADER.items()]
    if Auth([serverConfig.ADMIN_ID]):
        return Response(GenVideo(), mimetype='multipart/x-mixed-replace;boundary=frame',
                        headers=streamHeaders)
    else:
        abort(403)