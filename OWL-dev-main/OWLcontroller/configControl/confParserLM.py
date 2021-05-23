# config parser for the Legacy Mode
from configparser import ConfigParser
import configControl.confFile
from collections import namedtuple
from collections import OrderedDict
import json
import os
from configControl.configTypes.constans import constans
import re

def convertToString(line):
    return str(line)

def getFilePath(legacyModeConfigFilesDirectory, filename):
    return os.path.join(legacyModeConfigFilesDirectory, filename)

def getRootDirectory(relativePath):
    return r'..\\' + relativePath

def findFile(fileNameFromUser ="../"):
    path = constans.LEGACY_ROOT_FOLDER + fileNameFromUser
    return path if os.path.isfile(path) else ''

def findDir(dirNameFromUser):
    path = constans.LEGACY_ROOT_FOLDER + dirNameFromUser
    return path if os.path.isdir(path) else ''

# Parser
class confParserLM():
    def __init__(self,defaultConfContent):
        # Legacy Mode configs paths
        self.lMConfFilesDirectory = findDir(defaultConfContent['legacyModePath']) # LM - Legacy Mode config files directory

    # Legacy mode
    def getFilesNames(self, path):
        return os.listdir(path)

    def getGroupOfSection(self, sectionName):
        return (sectionName.split('/')[1])

    def getParamsFromSection(self, sectionName,lMConfFile):
        return list(lMConfFile[sectionName])

    def getparamValue(self, sectionName, param,lMConfFile):
        return lMConfFile[sectionName][param]

    def insertGroupTotestsByGroup(self, groupName, testsByGroupLM):
        if groupName not in testsByGroupLM: testsByGroupLM[groupName] = []
        return testsByGroupLM

    def addValueToLegacyConfiguration(self, testConf, Param, sectionName,lMConfFile):
        setattr(testConf, Param, self.getparamValue(sectionName, Param,lMConfFile))
        return testConf

    def getCurrPath(self):
        return os.getcwd().strip()

    def parseSequanceFile(self,sectionName,controlPc,lMConfFile ):
        operationsList = []
        with open (findFile(self.getparamValue(sectionName, 'sequancefile',lMConfFile))) as owlTestFile:
            for operationLine in owlTestFile:
                opName = self.getOperationName(operationLine)
                opParam = self.getOperationParam(operationLine)
                if opParam is None:
                    operationsList.append(opName)
                else:
                    operationsList.append({"name" : opName, "params" : opParam})
        return operationsList

#TODO need to check if its work because at home i didnt have host pc
    def getOperationParam(self, operationFromOwlTestFile):
        ''' will return whatever is between the brackets ([]) in ths string it gets '''
        regex = r"(?<=\[)([^]]+)(?=\])"
        matches = re.finditer(regex, operationFromOwlTestFile, re.MULTILINE)
        for matchNum, match in enumerate(matches):
            matchNum = matchNum + 1
            return "{match}".format(match=match.group())

    def getOperationName(self,operationFromOwlTestFile):
        """ Will return everything between quotes """
        return re.findall('"([^"]*)"', operationFromOwlTestFile)[0]

    def createSequanceFileConf(self, sectionName,controlPc,lMConfFile):
        testConfiguration = configControl.confFile.testConfLegacySequenceFlow()
        sequenceFile = self.parseSequanceFile(sectionName,controlPc,lMConfFile)
        if sequenceFile == None:
            return None
        testConfiguration.flowoperations = sequenceFile
        return testConfiguration

    def addingParamsToConf(self, sectionParams,testConf,sectionName,lMConfFile):
        for Param in sectionParams:
            testConf = self.addValueToLegacyConfiguration(testConf, Param, sectionName,lMConfFile)
        return testConf

    def saveConfIntoDicts(self, sectionName, legacyFlowOperationsTestsByGroups, testConf):
        groupName = self.getGroupOfSection(sectionName)
        legacyFlowOperationsTestsByGroups = self.insertGroupTotestsByGroup(groupName, legacyFlowOperationsTestsByGroups)
        legacyFlowOperationsTestsByGroups[groupName].append(testConf)

    def parseLMConf(self, controlPc):
        ''' parsing Legacy mode config files '''
        legacyTestsByGroup = OrderedDict()
        legacyFlowOperationsTestsByGroups = OrderedDict()
        parseResults = namedtuple('parsingResult', ['legacyTestsByGroup',  'legacyFlowOperationsTestsByGroups' ])
        # Legacy mode config file (contains sections , each section is a summary for one test)
        for filename in self.getFilesNames(self.lMConfFilesDirectory):
            if filename.endswith(constans.LEGACY_MODE_CONF_SUFFIX):
                lMConfFile = ConfigParser()
                lMConfFile.read(getFilePath(self.lMConfFilesDirectory, filename))  # (os.path.join(self.legacyModeConfigFilesDirectory, filename))
                # create configuration file
                for sectionName in lMConfFile.sections():
                    sectionParams = self.getParamsFromSection(sectionName,lMConfFile)
                    if constans.LEGACY_SEQUENCE_FILE in sectionParams:
                        testConf = self.createSequanceFileConf(sectionName,controlPc,lMConfFile)
                        if testConf == None:
                            continue # If the user provided an invalid Json file (sequence file) , the system won't take it.
                        self.addingParamsToConf(sectionParams,testConf, sectionName,lMConfFile)
                        self.saveConfIntoDicts(sectionName, legacyFlowOperationsTestsByGroups, testConf)
                    else:
                        testConf = configControl.confFile.testConfLegacy()  # Creates Legacy config file container
                        self.addingParamsToConf(sectionParams, testConf, sectionName,lMConfFile)
                        self.saveConfIntoDicts(sectionName, legacyTestsByGroup, testConf)
        return parseResults(legacyTestsByGroup, legacyFlowOperationsTestsByGroups)  # return the namedTuple contains both results dicts




