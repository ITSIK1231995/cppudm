from operations.operation import operation
from operations.operationsTypes import runCommandViaCmd, shutdown, sleep, hibernate


class allOperations():
    operationsImplement = {str : operation}
    operationsImplement['runCommandViaCmd'] = runCommandViaCmd.runCommandViaCMD
    operationsImplement['shutdown'] = shutdown.shutdown
    operationsImplement['sleep'] = sleep.sleep
    operationsImplement['hibernate'] = hibernate.hibernate
