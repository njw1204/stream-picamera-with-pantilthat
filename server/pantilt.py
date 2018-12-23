from statistics import median
from .setting import motorConfig
import pantilthat, threading, time

class VAR:
    thread = None
    threadOn = False
    lock, lock2 = threading.Lock(), threading.Lock()


def moveRelative(dir, angle):
    with VAR.lock:
        if dir == 'left' or dir == 'down':
            angle = -angle

        if dir == 'left' or dir == 'right':
            angle += pantilthat.get_pan()
            pantilthat.pan(median([-90, angle, 90]))
        elif dir == 'up' or dir == 'down':
            angle += pantilthat.get_tilt()
            pantilthat.tilt(median([-90, angle, 90]))


def startTask(dir, duration, force):
    if force:
        stopTask()

    with VAR.lock2:
        if VAR.threadOn:
            return False
        VAR.threadOn = True
        VAR.thread = threading.Thread(target=moveRelativeThread, args=(dir, duration))
        return True


def stopTask():
    with VAR.lock2:
        VAR.threadOn = False
        try: VAR.thread.join()
        except: pass
        VAR.thread = None


def moveRelativeThread(dir, duration):
    startTime = time.time()
    while VAR.threadOn and time.time() - startTime < duration:
        moveRelative(dir, motorConfig.UNIT_OF_TASK)
        time.sleep(motorConfig.TICK_OF_TASK)
    VAR.thread = None
    VAR.threadOn = False