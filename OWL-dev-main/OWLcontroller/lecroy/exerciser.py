import os
import win32com.client
class exerciser():
    def __init__(self,PETracer = None):
        if PETracer is None:
            self.PETracer = win32com.client.Dispatch("CATC.PETracer")
        else:
            self.PETracer = PETracer

    def loadGenerationOptions(self,generationOptionFilePath):
        self.PETracer.GetGenerationOptions().Load(generationOptionFilePath)

    def startGenerationScript(self,generationScriptPathAndName):
        self.PETracer.StartGeneration(generationScriptPathAndName, 0, 0 )