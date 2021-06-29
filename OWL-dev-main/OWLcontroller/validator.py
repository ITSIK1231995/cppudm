from Utils import getOperationObject
from operations.allOperations import allOperations
from collections import namedtuple
import logging

class Validator:
    def __init__(self,controller):
        self.controller = controller
        self.validateflowOps()
        self.validateAndFixHostPcSavedTestData()

    def validateflowOps(self):
        outputText = ""
        for groupName,groupTests in self.controller.configs.legacyMode.legacyFlowOperationsTestsByGroups.items():
            for test in groupTests:
                for x in range(len(test.flowoperations)-1):
                    leadingOp = getOperationObject(test.flowoperations[x])
                    tralingOp = getOperationObject(test.flowoperations[x + 1])
                    if not leadingOp.opraionObj.PCOnAfterTest() and tralingOp.opraionObj.asumesPcOnBeforeTest():
                        outputText +="At group= "+groupName+",test= "+test.testname+\
                                     "\nThe operation "+leadingOp.name+" can not be followed by "+tralingOp.name+"\n"

        if outputText != "":
            logging.info("Validator detected issues in flow operations")
            if "flowOpsErr" not in self.controller.preRunValidationErorrs.keys():
                self.controller.preRunValidationErorrs["flowOpsErr"] = []
            self.controller.preRunValidationErorrs["flowOpsErr"].append("system detected issues with the following flow operations\n\n" + outputText +
                "\n it is recommended to go over the test flows and fix the issues, otherwise this might result in unexpected behaviour")

    def doesTestExsistInConf(self,testName,groupName):
        if groupName not in self.controller.configs.legacyMode.legacyFlowOperationsTestsByGroups:
            return False
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
                    outputText += "Saved test name "+savedTestName+", for host "+hostPc["IP"]+\
                                  " was not found in the configuration files\n"
                    itemsToRemove.append(itemToRemove(savedTestName,hostPc["tests"]))
        if outputText != "":
            logging.info("Validator detected issues in saved hostPc Tests")

            if "hostPcSavedTestData" not in self.controller.preRunValidationErorrs.keys():
                self.controller.preRunValidationErorrs["hostPcSavedTestData"] = []
            self.controller.preRunValidationErorrs["hostPcSavedTestData"].append("System detected issues with the following saved tests\n\n" + outputText+
                                                          "\nSystem had removed this tests in memory in order to prevent unexpected behaviour\n"
                                                          "If you wish to run the system with this tests\n"
                                                          "Exit without saving and add the missing tests in the appropriate configuration files before starting the system again")

        for itemToRemove in itemsToRemove:
            del itemToRemove.sourceDict[itemToRemove.name]
