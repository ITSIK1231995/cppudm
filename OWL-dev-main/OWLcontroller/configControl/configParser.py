from configparser import ConfigParser
from configControl.confFile import * # TODO: need ot change this to regualr import because we want to use the name of the class and than the name of the operation , for example : controlPC.function , that way we can see it very natural the functiom and who does them
from collections import namedtuple
from collections import OrderedDict
from configControl.configControlUtils import *
from pathlib import Path
import json
import os

# Errinj Mode
ERRINJ_CONFIG_FILE_SUFFIX = ".cts"
TEST_PARAM = "="

# Legacy mode
LEGACY_MODE_CONF_SUFFIX = 'ini'


def cleanUpErrinjModeConfFile(line):
    return line.rstrip("\n").replace(";", "").replace('"', "").strip().split("=")

def convertToString(line):
    return str(line)

def getFilePath(legacyModeConfigFilesDirectory, filename):
    return os.path.join(legacyModeConfigFilesDirectory, filename)

def getRootDirectory(relativePath):
    return r'..\\' + relativePath



def findFile(fileNameFromUser ="../"):
    path = "../" + fileNameFromUser
    return path if os.path.isfile(path) else ''

# def searchFromRoot(dirNameFromUser):
#     start = "../"
#     for dirpath, dirnames, filenames in os.walk(start):
#         for filename in filenames:
#             if filename == dirNameFromUser:
#                 filename = os.path.join(dirpath, filename)
#                 # print(filename)
#                 # print(dirpath)
#                 # print(dirnames)
#                 #print(dirpath)
#                 return filename


def findDir(dirNameFromUser):
    path = "../" + dirNameFromUser
    return path if os.path.isdir(path) else ''



# Parser
class configParser():
    def __init__(self):

        # Legacy Mode configs paths
        defaultConfContent = self.parseDefaultConf()
        # self.legacyModeConfigFilesDirectory = getRootDirectory(defaultConfContent['legacyModePath'])
        self.lMConfFilesDirectory = findDir(defaultConfContent['legacyModePath']) # LM - Legacy Mode config files directory
        # Errinj mode configs paths
        self.errinjConfFilesPath = findDir(defaultConfContent['errinjModePath'])
        self.errinjConfFile = ConfigParser()
        self.errinjConfFile.read(self.errinjConfFilesPath)


    # Common methods for parsing

    def getFilesNames(self, path):
        return os.listdir(path)


    # Legacy mode
    def getGroupOfSection(self, sectionName):
        return (sectionName.split('/')[1])

    def getParamsFromSection(self, sectionName):
        return list(self.lMConfFile[sectionName])

    def getparamValue(self, sectionName, param):
        return self.lMConfFile[sectionName][param]

    def insertGroupTotestsByGroup(self, groupName, testsByGroupLM):
        if groupName not in testsByGroupLM: testsByGroupLM[groupName] = []
        return testsByGroupLM

    def addValueToLegacyConfiguration(self, testConf, Param, sectionName):
        setattr(testConf, Param, self.getparamValue(sectionName, Param))
        return testConf

    def parseSequanceFile(self, sectionName):
        flowOperationsName = open((findFile(self.getparamValue(sectionName, 'sequancefile'))), encoding="utf8")
        FlowOperations = json.load(flowOperationsName)
        flowOperationsName.close()
        return FlowOperations

    def createSequanceFileConf(self, sectionName):
        testConfiguration = testConfLegacySequenceFlow()
        sequenceFile = self.parseSequanceFile(sectionName)
        for operation in sequenceFile['operationsList']:
            testConfiguration.flowoperations.append(operation)
        print(testConfiguration.flowoperations)
        return testConfiguration

    def addParamsToConf(self, sectionParams, testConf, sectionName):
        for Param in sectionParams:
            testConf = self.addValueToLegacyConfiguration(testConf, Param, sectionName)
        return testConf

    def saveConfIntoDicts(self, sectionName, legacyFlowOperationsTestsByGroups, testConf):
        groupName = self.getGroupOfSection(sectionName)
        legacyFlowOperationsTestsByGroups = self.insertGroupTotestsByGroup(groupName, legacyFlowOperationsTestsByGroups)
        legacyFlowOperationsTestsByGroups[groupName].append(testConf)
        # legacyFlowOperationTestsByStatus[testConf.testname] = testConf
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!got into seuance stracture')



    def parseLMConf(self):
        ''' parsing Legacy mode config files '''
        legacyTestsByGroup = OrderedDict()
        legacyFlowOperationsTestsByGroups = OrderedDict()
        parseResults = namedtuple('parsingResult', ['legacyTestsByGroup',  'legacyFlowOperationsTestsByGroups' ])

        # Legacy mode config file (contains sections , each section is a summary for one test)
        for filename in self.getFilesNames(self.lMConfFilesDirectory):
            if filename.endswith(LEGACY_MODE_CONF_SUFFIX): # TODO: need to move the SUFFIX to a file of constatns stuff but bot utilss , because utils its for for genearal tools
                self.lMConfFile = ConfigParser() # TODO: legacyConfigFile is attribute that we need only for this function andd not for all the class , so need to change this to be local to the function and if oter functions usess it ned to send it to them
                self.lMConfFile.read(getFilePath(self.lMConfFilesDirectory, filename))  # (os.path.join(self.legacyModeConfigFilesDirectory, filename))
                # create configuration file
                for sectionName in self.lMConfFile.sections():
                    sectionParams = self.getParamsFromSection(sectionName)
                    if 'sequancefile' in sectionParams: #TODO: "sequanceFile" should be constant , we need create a class of CONSTANTS , that way each const will be reached by const.legacy.something
                        #TODO: change all the places of the word configuration into conf
                        testConf = self.createSequanceFileConf(sectionName)
                        self.addParamsToConf(sectionParams, testConf, sectionName)
                        self.saveConfIntoDicts(sectionName, legacyFlowOperationsTestsByGroups, testConf)
                    else:
                        testConf = testConfLegacy()  # Creates Legacy config file container
                        self.addParamsToConf(sectionParams, testConf, sectionName)
                        self.saveConfIntoDicts(sectionName, legacyTestsByGroup, testConf)
        return parseResults(legacyTestsByGroup, legacyFlowOperationsTestsByGroups)  # return the namedTuple contains both results dicts

        # Errinj Mode


    def addParamAndValueToErrinjConfFile(self, testConf, Param, ParamValue):
        setattr(testConf, Param, ParamValue)
        return testConf

    def storeTestConfurationIntoDicts(self, testConf, testsByGroupErrinj, testStatusErrinj):
        if testConf.testgroup not in testsByGroupErrinj:
            testsByGroupErrinj[testConf.testgroup] = []
        else:
            testsByGroupErrinj[testConf.testgroup].append(testConf)
        testStatusErrinj[testConf.testname] = testConf
        return (testsByGroupErrinj, testStatusErrinj)

    def parseErrinjConfFiles(self):
        ''' Returns namedTuple which contains testsByGroupErrinj and testStatusErrinj '''
        testsByGroupErrinj = OrderedDict()
        testStatusErrinj = OrderedDict()
        parsingResults = namedtuple('parsingResult', ['testsByGroupErrinj', 'testStatusErrinj'])
        allConfFilesPaths = Path(self.errinjConfFilesPath).rglob('*.cts')
        for pathOFConfigFile in allConfFilesPaths:
            confFilePAth = convertToString(pathOFConfigFile)  # because pathOFConfigFile is object not string
            with open(confFilePAth) as config:
                testConf = testConfErrinj()
                for line in config.readlines():
                    if TEST_PARAM in line:
                        paramName, paramValue = cleanUpErrinjModeConfFile(line)
                        testConf = self.addParamAndValueToErrinjConfFile(testConf, paramName,
                                                                                  paramValue)
            testsByGroupErrinj, testStatusErrinj = self.storeTestConfurationIntoDicts(testConf, testsByGroupErrinj, testStatusErrinj)
        return parsingResults(testsByGroupErrinj, testStatusErrinj)  # return the namedTuple contains both results dicts


    def parseDefaultConf(self, defaultConfig='..\defaultConfiguration.json'):
        # Opening JSON file
        # TODO: change the string for the defaultconfiguration.json to a CONSTANT in the begining of the file
        defaultConf = open('..\defaultConfiguration.json', encoding="utf8")
        defaultConfContent = json.load(defaultConf)
        defaultConf.close()
        return defaultConfContent

    # def parseAll(self):
    #     defaultConfigurationContent = self.parsingDefaultConfig()
    #     pass


# Tester for pharsing Legacy Config

dictsfromparsing = configParser().parseLMConf()

print ('test')
print('testsByGroupLegacyFlowOperations', dictsfromparsing.legacyFlowOperationsTestsByGroups)
# print('testStatusLegacyFlowOperations', dictsfromparsing.legacyFlowOperationTestsByStatus)
print('testsByGroupLegacy', dictsfromparsing.legacyTestsByGroup)
# print('testStatusLegacy', dictsfromparsing.legacyTestsByStatus)



# Tester for parsing errinj config
print ('dirnames')
dirnames = configParser().parseErrinjConfFiles()
for item in dirnames.testsByGroupErrinj.values():
    print(item)


# # Tester for default config parsing
configParser().parseDefaultConf()


#deep search of folder
path ="../"
#we shall store all the file names in this list
filelist = []

for root, dirs, files in os.walk(path):

    for file in files:
        #append the file name to the list
        filelist.append(os.path.join(root,file))

#print all the file names
for name in filelist:
    print(name)



# # Tester for reading json files
#     for filename in os.listdir(r'C:\Projects\autoLatencyApp\defaultConfiguration.json'):
#         if filename.endswith('json'):
#             print (filename)
#             with open(filename) as f:
#                 d = json.load(f)
#                 print(d)


# #Opening JSON file
# f = open('defaultConfiguration.json', encoding="utf8"  )
#
# # returns JSON object as
# # a dictionary
# data = json.load(f)
#
# # Iterating through the json
# # list
# for i in data['hostPCs']:
#     print(i)
#
# # Closing file
# f.close()


# Read files tester
import os
directory = r'C:\Projects\autoLatencyApp\legacyModeConfigFiles'
for filename in os.listdir(directory):
    if filename.endswith(".ini"):
        print(os.path.join(directory, filename))
        continue
    else:
        continue
