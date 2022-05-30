import time

class TimeKeeper:
    paused = False
    time = time.strftime("%H:%M:%S", time.localtime())

class TaskManager:

    def getTime(self):
        return time.strftime("%H:%M:%S", time.localtime())

    def pause(self, cachedTime):
        cachedTime.paused = True
        cachedTime.time = time.strftime("%H:%M:%S", time.localtime())
        return cachedTime

    def start(self, cachedTime):
        cachedTime.paused = False
        cachedTime.time = time.strftime("%H:%M:%S", time.localtime())
        return cachedTime
