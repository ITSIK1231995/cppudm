from configControl.confParserErrinjMode import confParserErrinjMode
from configControl.confParserLM import confParserLM
from collections import namedtuple
import json


# Parser

# DEFAULT_CONF_FILE = '..\defaultConfiguration.json' When running directly from this file
DEFAULT_CONF_FILE = 'defaultConfiguration.json' #when running from the controlPc


class confParser():
    def __init__(self):
        pass

    def parseAll(self,loadConf):
        defaultConfContent = self.parseDefaultConf(loadConf)

        lMparsingResults = confParserLM(defaultConfContent).parseLMConf() # Parsing the legacy mode config files (Flow operations and trainer scripts)
        errinjModeParsingResults = confParserErrinjMode(defaultConfContent).parseErrinjConfFiles() # Parsing the Errinj Mode config files

        parseResults = namedtuple('parsingResult', ['legacyMode', 'ErrinjMode','defaultConfContent'])
        return parseResults(lMparsingResults, errinjModeParsingResults,defaultConfContent)


    def parseDefaultConf(self, defaultConfig):
        defaultConf = open(defaultConfig, encoding="utf8")
        defaultConfContent = json.load(defaultConf)
        defaultConf.close()
        return defaultConfContent
