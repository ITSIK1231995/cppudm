from enum import Enum


class state(Enum): #TODO need to move it to a seperate file
    PASSED = 1
    FAILED = 2
    RUNNING = 3
    FINISHED = 4
    NOTSTARTED = 5
