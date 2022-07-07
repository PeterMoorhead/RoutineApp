from mimetypes import init
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


    print("appBegun: ", appBegun)
    if (appBegun == False):
        print("starting app")
        appBegun = True
        #startup sequence
        splitTaskTime()

    print("on return: ", currentTask)
    time.sleep(1)
    return getStatus()

@app.route('/pause')
def pauseTasks():
    global paused    
    global initTasks
    global timeAtPause
    global baseTasks

    cT = newBrowser()

    timeAtPause = totalTimeTillFinish('21:45:00')

    taskAtPause = list(cT.keys())[0]
    timeLeftOfTaskAtPause = list(cT.values())[0] 
    print("timeLeftOfTaskAtPause:", timeLeftOfTaskAtPause) #7087
    print("initTasks.get(taskAtPause):", initTasks.get(taskAtPause)) #{'startTime': 35454, 'endTime': 28364}

    fullTimeAllocated = initTasks.get(taskAtPause)['startTime'] - initTasks.get(taskAtPause)['endTime']
    print("fullTimeAllocated: ", fullTimeAllocated) #7090

    timePassed = initTasks.get(taskAtPause)['startTime'] - (initTasks.get(taskAtPause)['endTime'] + timeLeftOfTaskAtPause) # 3104 - (time left) = time passed
    print("time passed: ", timePassed) #3.0

    taskTimeAlreadyDonePercentage = timePassed / fullTimeAllocated # 0.0004231311706629055 (percentage)
    print("taskTimeAlreadyDonePercentage: ", taskTimeAlreadyDonePercentage)

    percentageLeftToDo = 1 - taskTimeAlreadyDonePercentage # new allocation for when you start again or 13.5% in example

    index = 0
    for i in baseTasks:
        percentToAdd = (i.percent * (i.percent * taskTimeAlreadyDonePercentage))/100
        print("i.percent", i.percent)
        print("(i.percent * taskTimeAlreadyDonePercentage)", (i.percent * taskTimeAlreadyDonePercentage))
        print("percentToAdd", percentToAdd)
        print("percentageLeftToDo", percentageLeftToDo)
        if (index == 0):
          newPercentAllocation = percentToAdd + (i.percent * percentageLeftToDo)
        else:
          newPercentAllocation = percentToAdd + i.percent

        print("newPercentAllocation", newPercentAllocation)
        
        baseTasks[index].percent = newPercentAllocation
        index = index + 1

    for x in baseTasks:
        print("Task: ", x.task)
        print("Start Time: ", x.startTime)
        print("End Time: ", x.endTime)
        print("Percentage: ", x.percent)


    paused = True
    return {'paused': 0}

@app.route('/start')
def startTasks():
    global totalTimeLeft
    global paused

    paused = False
    
    splitTaskTime()
    return getStatus()

def getStatus():
    global paused
    
    task = newBrowser()
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

    index = 0
    y = totalTimeTillFinish('21:45:00') #time in seconds till 9:45pm
    l = 0 #time that gets added up to add to end time etc during loop
    for i in baseTasks:
        if (index == 0):
            x = i.percent * int(totalTimeTillFinish('21:45:00'))
            l = round(l + x)
            initTasks[i.task] = {"endTime": 0, "startTime": round(x)-1}
            print(initTasks[i.task])
        else:
            x = i.percent * int(totalTimeTillFinish('21:45:00'))
            initTasks[i.task] = {"endTime": l, "startTime": round(x + l)-1}
            l = round(l + x)
            print(initTasks[i.task])

        index = index + 1
    

def newBrowser(): # for when apps already running and you open it on your phone or somewhere afterwards
    #needs to calc how far you are through current task list and at what time you are and then calc the remaining time to 9:45pm
    global totalTimeLeft
    global currentTask
    global initTasks #object of format: {'russian': {'endTime': 619, 'startTime': 310}, 'programming': {'endTime': 309, 'startTime': 0}} etc
    global paused

    currentTimeLeft = totalTimeTillFinish('21:45:00')
    print("currentTimeLeft: ", currentTimeLeft)
    for task in initTasks.copy():        
        if (currentTimeLeft < initTasks[task]["endTime"]):
            initTasks.pop(task)

    for task in initTasks:
        if (currentTimeLeft >= initTasks[task]["endTime"] and currentTimeLeft <= initTasks[task]["startTime"]):
            x = currentTimeLeft - initTasks[task]["endTime"]
            print("x: ", x)
            return {task: x} #returns {'russian': 200} where 200 is time left

    return {'nothing': 0}

appBegun = False

rng = random.randint(1, 5)

baseTasks = [Task("programming",0.2,0,0), Task("russian",0.2,0,0), Task("self help",0.2,0,0), Task("finance",0.2,0,0), Task("exercise",0.2,0,0)] #task,percentage
paused = False
totalTimeLeft = totalTimeTillFinish('21:45:00') #returns seconds left
initTasks = {}
currentTask = 0
timeAtPause = 0