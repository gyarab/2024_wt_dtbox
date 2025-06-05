from dtbox.display.shortcuts import display
from time import time_ns, sleep_ms
from dtbox.buzzer.shortcuts import buzzer
from dtbox.ultrasonic.shortcuts import ultrasonic

maxRange = 100
minRange = 20
someonePresent = False
entered = False
totalLefts = 0

def checkLegitDistance():
    dists = 0
    for i in range(30):
        dists += round(ultrasonic.distance_cm())
    avgDists = dists/30
    if avgDists < maxRange and avgDists > minRange:
        return True
    else:
        return False

while True:
    distance = round(ultrasonic.distance_cm())
    display.show(distance)
    print(someonePresent)
    if distance < maxRange and distance > minRange:
        if checkLegitDistance:
            someonePresent = True
            entered = True
            continue
    someonePresent = False
    if someonePresent == False and entered == True:
        totalLefts += 1
        if totalLefts > 15:
            break

entered = False
someonePresent = False
timeStart = time_ns()
totalLefts = 0

while True:
    time = str((time_ns() - timeStart) / 1000000000)
    display.show(time[:5])
    distance = round(ultrasonic.distance_cm())
    print(someonePresent)
    if distance < maxRange and distance > minRange:
        if checkLegitDistance:
            someonePresent = True
            entered = True
            continue
    someonePresent = False
    if someonePresent == False and entered == True:
        totalLefts+=1
        if totalLefts > 15:
            break
