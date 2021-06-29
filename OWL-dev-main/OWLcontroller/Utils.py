import datetime
from collections import namedtuple
from operations.allOperations import allOperations

def getHostsDictFromDefaultConfigurationForCurrentExecutionMode(controller):
    if controller.isCurrentExecutionModeIsHostPcMode():
        return controller.configs.defaultConfContent['hostPCs']
    else:
        return controller.configs.defaultConfContent['Exercisers']

def getTestsByGroupDictForCurrentSystemExecutionMode(controller):
    if controller.isCurrentExecutionModeIsHostPcMode():
        return controller.configs.legacyMode.legacyFlowOperationsTestsByGroups
    else:
        return controller.configs.legacyMode.legacyTestsByGroup

def getOperationObject(operation):
    opraion = namedtuple('opraion', ['name', 'opraionObj'])
    mappedOperations = allOperations()
    if isinstance(operation, dict):
        return opraion(operation['name'], mappedOperations.operationsImplementation[operation['name']])
    if isinstance(operation, str):
        return opraion(operation, mappedOperations.operationsImplementation[operation])

def getCurrentTime():
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))