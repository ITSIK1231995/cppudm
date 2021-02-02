from operations.allOperations import allOperations
from collections import namedtuple

class Validator:
    def __init__(self,controller):
        self.controller = controller

    def getOprationObject(self,operation):
        opraion = namedtuple('opraion', ['name', 'opraionObj'])
        mappedOperations = allOperations()
        if isinstance(operation, dict):
            return opraion(operation['name'], mappedOperations.operationsImplementation[operation['name']])
        if isinstance(operation, str):
            return opraion(operation, mappedOperations.operationsImplementation[operation])

    def validateflowOps(self):

        outputText = ""
        for groupName,groupTests in self.controller.configs.legacyMode.legacyFlowOperationsTestsByGroups.items():
            for test in groupTests:
                for x in range(len(test.flowoperations)-1):
                    leadingOp = self.getOprationObject(test.flowoperations[x])
                    tralingOp = self.getOprationObject(test.flowoperations[x+1])
                    if not leadingOp.opraionObj.PCOnAfterTest() and tralingOp.opraionObj.asumesPcOnBeforeTest():
                        outputText +="at group= "+groupName+",test= "+test.testname+\
                                     "\nthe opration "+leadingOp.name+" can not be followed by "+tralingOp.name+"\n"

        if outputText != "":
            self.controller.preRunValidationErorrs.append("system detected issues with the flowing the flow operations\n\n" + outputText+
                                                          "\n it is recomanded to go over the test flows and fix the issues, otherwise this might result in unexpected behaviour")
