from UI.GUI.teststate import testState
PASS_COLOR = "background-color: rgb(0, 255, 0);"
FAIL_COLOR = "background-color: rgb(255, 153, 153);"
RUN_COLOR = "background-color: rgb(255, 178, 102);"
NOT_STARTED_COLOR = "background-color: rgb(192, 192, 192);"
COLOR_CONVERTER = {testState.RUNNING :RUN_COLOR ,
                   testState.PASSED : PASS_COLOR,
                   testState.FAILED : FAIL_COLOR,
                   testState.NOTSTARTED : NOT_STARTED_COLOR}


#TODO need to use the above dict instead of the below class in all the places we are using convertor


class convertor():
    def __init__(self):
        self.states = testState

    def getColorForState(self, currState):
         if currState == self.states.RUNNING:
             return RUN_COLOR
         if currState == self.states.PASSED:
             return PASS_COLOR
         if currState == self.states.FAILED:
             return FAIL_COLOR
         if currState == self.states.NOTSTARTED:
             return NOT_STARTED_COLOR



