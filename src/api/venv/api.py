import time
import random
import datetime

from flask import Flask
from flask_cors import CORS
from AppService import TaskManager, TimeKeeper
from Task import Task
from datetime import timedelta

app = Flask(__name__)
CORS(app)

@app.route('/getRoutine')
def appStartTime():
    global appBegun
    global totalTimeLeft
    global paused
    global currentTask
    global initTasks

    if (appBegun == False):
        appBegun = True
        #startup sequence
        splitTaskTime()

    print("on return: ", currentTask)
    # newBrowser()
    return getStatus()

@app.route('/pause')
def pauseTasks():
    global paused
    paused = True
    return getStatus()

@app.route('/start')
def startTasks():
    global totalTimeLeft
    global paused 
    paused = False
    return getStatus()

def getStatus():
    global paused
    global currentTask
    print("paused: ", paused)
    print("currentTask: ", currentTask["name"])
    print("time: ", initTasks[currentTask["name"]])
    task = {"task": currentTask["name"], "time": initTasks[currentTask["name"]]}
    return {"paused": paused, "currentTask": task}

def totalTimeTillFinish(endTime):
    currentTime = time.strftime("%H:%M:%S", time.localtime())
    d1 = datetime.datetime.strptime(endTime,'%H:%M:%S')
    d2 = datetime.datetime.strptime(currentTime,'%H:%M:%S')
    return (d1 - d2).total_seconds() # returns time left in seconds

def splitTaskTime(): #not called often, just on start, pause/start
    global totalTimeLeft
    global currentTask
    global baseTasks
    global initTasks

    # cachedTime is time left to go
    # need to divide that by each tasks %
    
    for i in baseTasks:
        print("i:", i.task)
        y = totalTimeTillFinish('21:45:00')
        print("y", y)
        initTasks[i.task] = i.time * int(totalTimeTillFinish('21:45:00'))
        print("init task: ", initTasks[i.task])

    timeTillDoneInSeconds = initTasks[list(initTasks.keys())[0]] ## till hereish?
    startTime = time.strftime("%H:%M:%S", time.localtime())
    d2 = datetime.datetime.strptime(startTime,'%H:%M:%S')
    d3 = d2 + datetime.timedelta(seconds=timeTillDoneInSeconds)
    print("d333 in split: ", d3) #1900-01-01 19:53:46.400000

    x = str(d3)
    s_x = x.split(".", 1)
    y = s_x[0]
    d5 = datetime.datetime.strptime(y, '%Y-%d-%m %H:%M:%S')
    print(d5)
    currentTask = {"name": list(initTasks.keys())[0], "startTime": startTime, "endTime": d3} 
    print("name in split: ", currentTask["name"])
    print("startTime in split: ", currentTask["startTime"])
    print("d3 in split: ", currentTask["endTime"])
    # initTasks = {"programming",1960, "russian",1960, "self help",1960, "finance",1960, "exercise",1960} (task, time in seconds allocated for task)

def newBrowser():
    global totalTimeLeft
    global currentTask
    global baseTasks
    global initTasks


    startTime = time.strftime("%H:%M:%S", time.localtime())
    d2 = datetime.datetime.strptime(startTime,'%H:%M:%S')
    print("d2: ", d2)
    print("endTime: ",currentTask["endTime"])
    d2 = d2.strftime('%H:%M:%S')
    d4 = currentTask["endTime"]
    d2 = datetime.datetime.strptime(d2, '%H:%M:%S')
    x = str(d4)
    s_x = x.split(".", 1)
    y = s_x[0]
    d4 = datetime.datetime.strptime(y, '%Y-%d-%m %H:%M:%S')
    d3 = d4 - d2
    print("newBrowser: ", d3)

    currentTask = {"name": list(initTasks.keys())[0], "startTime": startTime, "endTime": d3}
    return

appBegun = False

rng = random.randint(1, 5)

baseTasks = [Task("programming",0.2), Task("russian",0.2), Task("self help",0.2), Task("finance",0.2), Task("exercise",0.2)] #task,percentage
paused = False
totalTimeLeft = totalTimeTillFinish('21:45:00') #returns seconds left
initTasks = {}
currentTask = 0