from UI.GUI.teststate import testState
PASS_COLOR = "background-color: rgb(0, 255, 0);"
FAIL_COLOR = "background-color: rgb(255, 153, 153);"
RUN_COLOR = "background-color: rgb(255, 178, 102);"
NOT_STARTED_COLOR = "background-color: rgb(192, 192, 192);"
COLOR_CONVERTER = {testState.RUNNING :RUN_COLOR ,
                   testState.PASSED : PASS_COLOR,
                   testState.FAILED : FAIL_COLOR,
                   testState.NOTSTARTED : NOT_STARTED_COLOR}








