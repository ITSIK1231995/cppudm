import time

from win32com.client import Dispatch
from time import sleep
import pythoncom
import os
from win32com.universal import com_error
from lecroy.dispatchComObj import dispatchComObj

isTraceCreatedPerAnalyzer = []
resetExerciserGenerationScriptState = 0
class PEEvent(object):
    def __init__(self,SavedTraceFullPathAndName,traceReady,hostPc,testLog,controller):
        self.saveTraceFullPath = SavedTraceFullPathAndName
        self.traceReady = traceReady
        self.hostPc = hostPc
        self.testLog = testLog
        self.controller = controller

    def OnTraceCreated(self, trace):
        try:
            print("PEEvent::OnTraceCreated - %s" % trace)
            self.controller.updateTerminalAndLog(self.hostPc, self.testLog, "PE-Event:: On Trace Created")
            trace_obj = Dispatch(trace)
            trace_obj.Save(self.saveTraceFullPath)
            trace_obj.Close()
            del trace_obj
            isTraceCreatedPerAnalyzer[self.traceReady] = True
        except Exception as e:
            print("PEEvent::OnTraceCreated failed with exception: %s" % e)
            self.controller.updateTerminalAndLog(self.hostPc, self.testLog, "PEEvent::OnTraceCreated failed with exception: %s" % e)

    def OnStatusReport(self, subsystem, state, percent_done):
        try:
            print("PEEvent::OnStatusReport - subsystem:{0}, state:{1}, progress:{2}".format(subsystem, state,percent_done))
            self.controller.updateTerminalAndLog(self.hostPc, self.testLog, "PEEvent::OnStatusReport - subsystem:{0}, state:{1}, progress:{2}".format(subsystem, state, percent_done))
            if state == 400:
                global resetExerciserGenerationScriptState
                resetExerciserGenerationScriptState = 1
        except Exception as e:
            print("PEEvent::OnStatusReport failed with exception: %s" % e)
            self.controller.updateTerminalAndLog(self.hostPc, self.testLog, "PEEvent::OnStatusReport failed with exception: %s" % e)

class lecroyHandler():
    def __init__(self,controller):
        self.traceFileName = "data.pex"  # default trace file name used in recording options
        self.controller = controller
        os.system("TASKKILL /F /IM PETracer.exe")

    def startRecordingWithAnalyzer(self,recOptionsFullPath,SavedTraceFullPathAndName,hostPc,testLog):
        global resetExerciserGenerationScriptState
        resetExerciserGenerationScriptState = 0
        traceReady = 0 #TODO need to change the name of it to  analzyer index
        isTraceCreatedPerAnalyzer.insert(traceReady, False) # the "0" indicates a place in the traceCreatedPerAnalyzer list, each item in this list will represent analyzer
        self.lecroyObj = dispatchComObj.DispatchWithEventsAndParams("CATC.PETracer", PEEvent, [SavedTraceFullPathAndName, traceReady, hostPc, testLog, self.controller])
        time.sleep(5) # TODO need to replace with getdiscoveredDevice() to make sure that the app worked
        self.rec_options = self.lecroyObj.GetRecordingOptions()
        self.rec_options.SetTraceFileName(self.traceFileName)
        print("Analyzer Record Started")
        self.controller.updateTerminalAndLog(self.lecroyObj.hostPc, self.lecroyObj.testLog, "\n Analyzer Record Started")
        try:
            self.lecroyObj.StartRecording(recOptionsFullPath)
            time.sleep(5) #Start recording requires few seconds of waiting by spec
        except com_error as e:
            print(str(e))
            self.controller.updateTerminalAndLog(self.lecroyObj.hostPc, self.lecroyObj.testLog, "\n Start Recording failed with the following exception:  " + str(e))
        return self.lecroyObj

    def stopAnalyzerRecording(self):
            self.lecroyObj.StopRecording(False)
            print("Analyzer Record Stopped")
            self.controller.updateTerminalAndLog(self.lecroyObj.hostPc, self.lecroyObj.testLog, "\n Analyzer Record Stopped")
            del self.rec_options  # delete recording options instance
            while (isTraceCreatedPerAnalyzer[self.lecroyObj.traceReady] == False):
                sleep(0.2)
                pythoncom.PumpWaitingMessages()
                print("PumpWaitingMessages")
            del self.lecroyObj

    def loadGenerationOptionToExerciser(self, lecroyObj,generationOptionFullPath):
        lecroyObj.GetGenerationOptions().Load(generationOptionFullPath)

    def startGenerationScriptOnExerciser(self,lecroyObj,generationScriptFullPathAndName,host,testLog,controllerPc):
        try:
            lecroyObj.StartGeneration(generationScriptFullPathAndName, 0, 0)
        except com_error as e:
            print(str(e))
            self.controller.updateTerminalAndLog(self.lecroyObj.hostPc, self.lecroyObj.testLog,"\n Start Generation failed with the following exception: " + str(e))

    def verifyExerciserGenerationScriptFinished(self): #TODO need to add time out
        while resetExerciserGenerationScriptState != 1:
            sleep(0.2)
            pythoncom.PumpWaitingMessages()
            print("PumpWaitingMessages")
        self.resetExerciserGenerationScriptState()
        return True

    def resetExerciserGenerationScriptState(self):
        global resetExerciserGenerationScriptState
        resetExerciserGenerationScriptState = 0
