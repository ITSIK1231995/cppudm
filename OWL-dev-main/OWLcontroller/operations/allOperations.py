from operations.operation import operation
from operations.operationsTypes.powerOnWithClicker import powerOnWithClicker
# from operations.operationsTypes.runDm import runDM
from operations.operationsTypes.runDm import runDM
from operations.operationsTypes.turnOnWithLan import turnOnWithLan
from operations.operationsTypes.wait import wait
from operations.operationsTypes.hibernate import hibernate
from operations.operationsTypes.sleep import sleep
from operations.operationsTypes.shutdown import shutdown
from operations.operationsTypes.runCommandViaCmd import runCommandViaCmd


class allOperations():
    operationsImplementation = {str : operation}
    operationsImplementation['runCommandViaCmd'] = runCommandViaCmd
    operationsImplementation['shutdown'] = shutdown
    operationsImplementation['sleep'] = sleep
    operationsImplementation['hibernate'] = hibernate
    operationsImplementation['wait'] = wait
    operationsImplementation['powerOnWithClicker'] = powerOnWithClicker
    operationsImplementation['turnOnWithLan'] = turnOnWithLan
    operationsImplementation['runDM'] = runDM

#
# print (allOperations.operationsImplement)