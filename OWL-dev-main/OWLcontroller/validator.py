from operations.allOperations import allOperations
from collections import namedtuple
import logging

class Validator:
    def __init__(self,controller):
        self.controller = controller
        self.validateflowOps()
        self.validateAndFixHostPcSavedTestData()


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
            logging.info("Validator detected issues in flow operations")
            self.controller.preRunValidationErorrs.append("system detected issues with the flowing the flow operations\n\n" + outputText+
                                                          "\n it is recomanded to go over the test flows and fix the issues, otherwise this might result in unexpected behaviour")

    def doesTestExsistInConf(self,testName,groupName):
        for testFromConf in self.controller.configs.legacyMode.legacyFlowOperationsTestsByGroups[groupName]:
            if testName == testFromConf.testname:
                return True
        return False
    def validateAndFixHostPcSavedTestData(self):
        itemToRemove = namedtuple('opraion', ['name', 'sourceDict'])
        itemsToRemove = []
        outputText = ""
        for hostPc in self.controller.configs.defaultConfContent["hostPCs"]:
            for savedTestName,savedTestObj in hostPc["tests"].items():
                if not self.doesTestExsistInConf(savedTestName,hostPc['groupName']):
                    outputText += "saved test name "+savedTestName+", for host "+hostPc["IP"]+\
                                  " was not found in the configuration files\n"
                    itemsToRemove.append(itemToRemove(savedTestName,hostPc["tests"]))


        if outputText != "":
            logging.info("Validator detected issues in saved hostPc Tests")
            self.controller.preRunValidationErorrs.append("System detected issues with the flowing saved tests\n\n" + outputText+
                                                          "\nSystem had removed this tests in memory in order to prevent unexpected behaviour\n"
                                                          "If you wish to run the system with this tests\n"
                                                          "exit without saving and add the missing tests in the appropriate configuration files before starting the system again")
        for itemToRemove in itemsToRemove:
            del itemToRemove.sourceDict[itemToRemove.name]
