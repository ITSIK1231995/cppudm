from configparser import ConfigParser
import configControl.confFile
from collections import namedtuple
from collections import OrderedDict
from pathlib import Path
import os
# Errinj Mode
from configControl.confParserLM import findDir
from configControl.fileOperationFuncs import convertToString, cleanUpErrinjModeConfFile
ERRINJ_CONFIG_FILE_SUFFIX = ".cts"
TEST_PARAM = "="
# Parser
class confParserErrinjMode():
    def __init__(self,defaultConfContent):

        # Errinj mode configs paths
        self.errinjConfFilesPath = findDir(defaultConfContent['errinjModePath'])
        self.errinjConfFile = ConfigParser()
        self.errinjConfFile.read(self.errinjConfFilesPath)

    def getFilesNames(self, path):
        return os.listdir(path)

    def addParamAndValueToErrinjConfFile(self, testConf, Param, ParamValue):
        setattr(testConf, Param, ParamValue)
        return testConf

    def storeTestConfurationIntoDicts(self, testConf, testsByGroupErrinj, ):
        if testConf.testgroup not in testsByGroupErrinj:
            testsByGroupErrinj[testConf.testgroup] = []
        else:
            testsByGroupErrinj[testConf.testgroup].append(testConf)
        return (testsByGroupErrinj)

    def parseErrinjConfFiles(self):
        ''' Returns namedTuple which contains testsByGroupErrinj and testStatusErrinj '''
        testsByGroupErrinj = OrderedDict()
        parsingResults = namedtuple('parsingResult', ['testsByGroupErrinj'])
        allConfFilesPaths = Path(self.errinjConfFilesPath).rglob('*.cts')
        for pathOFConfigFile in allConfFilesPaths:
            confFilePAth = convertToString(pathOFConfigFile)  # because pathOFConfigFile is object not string
            with open(confFilePAth) as config:
                testConf = configControl.confFile.testConfErrinj()
                for line in config.readlines():
                    if TEST_PARAM in line:
                        paramName, paramValue = cleanUpErrinjModeConfFile(line)
                        testConf = self.addParamAndValueToErrinjConfFile(testConf, paramName,
                                                                                  paramValue)
            testsByGroupErrinj = self.storeTestConfurationIntoDicts(testConf, testsByGroupErrinj)
        return parsingResults(testsByGroupErrinj)  # return the namedTuple contains both results dicts

if __name__ == '__main__':

    # Tester for parsing errinj config
    print ('dirnames')
    dirnames = confParserErrinjMode(0).parseErrinjConfFiles()
    for item in dirnames.testsByGroupErrinj.values():
        print(item)


