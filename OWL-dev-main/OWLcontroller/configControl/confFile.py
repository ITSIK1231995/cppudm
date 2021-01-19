class confFile(object):
    #confFile information
    testname = ''
    recordingoptions = ''
    generationoptions = ''
    verificationscript = ''

    def __setattr__(self, key, value):
        super.__setattr__(self,key.lower().strip(),value.lower().strip()) if hasattr(self, key.lower().strip()) else ''


    def __repr__(self):
        output = ''
        for var in vars(self):
            output +='\n'+ var + ' : ' + (str(getattr(self, var))) + '\n'
        return output


class testConfLegacy(confFile):
    trainerinitscript = ''
    trainerscript = ''

class testConfErrinj(confFile):
    testanalyzer = ''
    testgroup =''
    testcode = ''
    testdescription = ''
    trainerscript = ''


class testConfLegacySequenceFlow(confFile):
    def __setattr__(self, key, value):
        if isinstance(value, str):
            super.__setattr__(self,key.lower().strip(),value.lower().strip()) if hasattr(self, key.lower().strip()) else ''
        else:
            super.__setattr__(self, key, value)

    sequancefile = ''
    flowoperations = []



