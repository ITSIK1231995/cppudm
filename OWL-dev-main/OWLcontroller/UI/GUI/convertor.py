from UI.GUI.state import state
PASS_COLOR = "background-color: rgb(0, 255, 0);"
FAIL_COLOR = "background-color: rgb(255, 153, 153);"
RUN_COLOR = "background-color: rgb(255, 178, 102);"
NOT_STARTED_COLOR = "background-color: rgb(192, 192, 192);"
class convertor():
    def __init__(self):
        self.states = state
    def getAppropriateColorForState(self, currState):
         if currState == self.states.RUNNING:
             return RUN_COLOR
         if currState == self.states.PASSED:
             return PASS_COLOR
         if currState == self.states.FAILED:
             return FAIL_COLOR
         if currState == self.states.NOTSTARTED:
             return NOT_STARTED_COLOR



