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
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog, "PE-Event:: On Trace Created")
            trace_obj = Dispatch(trace)  # Dispatch trace object
            trace_obj.Save(self.saveTraceFullPath)  # Save trace file
            trace_obj.Close()  # close trace file
            del trace_obj  # delete trace dispatch instance
            isTraceCreatedPerAnalyzer[self.traceReady] = True
        except Exception as e:
            print("PEEvent::OnTraceCreated failed with exception: %s" % e)
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog,"PEEvent::OnTraceCreated failed with exception: %s" % e)

    def OnStatusReport(self, subsystem, state, percent_done):
        try:
            print("PEEvent::OnStatusReport - subsystem:{0}, state:{1}, progress:{2}".format(subsystem, state,percent_done))
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog,"PEEvent::OnStatusReport - subsystem:{0}, state:{1}, progress:{2}".format(subsystem, state,percent_done))
            if state == 400:
                global resetExerciserGenerationScriptState
                resetExerciserGenerationScriptState = 1
        except Exception as e:
            print("PEEvent::OnStatusReport failed with exception: %s" % e)
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog,"PEEvent::OnStatusReport failed with exception: %s" % e)

class lecroyHandler():
    def __init__(self,controller):
        self.traceFileName = "data.pex"  # default trace file name used in recording options
        self.controller = controller

    def startRecordingWithAnalyzer(self,recOptionsFullPath,SavedTraceFullPathAndName,hostPc,testLog): #TODO change to lecroyHandler
        global resetExerciserGenerationScriptState
        resetExerciserGenerationScriptState = 0
        traceReady = 0 #TODO need to change the name of it to  analzyer index
        isTraceCreatedPerAnalyzer.insert(traceReady, False) # the "0" indicates a place in the traceCreatedPerAnalyzer list, each item in this list will represent analyzer
        self.lecroyObj = dispatchComObj.DispatchWithEventsAndParams("CATC.PETracer", PEEvent, [SavedTraceFullPathAndName, traceReady, hostPc, testLog, self.controller])
        time.sleep(5) # TODO need to replace with getdiscoveredDevice() to make sure that the app worked
        self.rec_options = self.lecroyObj.GetRecordingOptions()
        self.rec_options.SetTraceFileName(self.traceFileName)
        print("Start Analyzer record")
        self.controller.updateRunTimeStateInTerminal(self.lecroyObj.hostPc, self.lecroyObj.testLog, "\n Start Analyzer record")  # TODO need to change the name of updateRunTimeStateInTerminal to updateTernimalAndLog
        try:
            self.lecroyObj.StartRecording(recOptionsFullPath)
            time.sleep(5) #Start recording requires few seconds of waiting by spec
        except com_error as e:
            print(str(e))
            self.controller.updateRunTimeStateInTerminal(self.lecroyObj.hostPc, self.lecroyObj.testLog,"\n While trying to start the Analzyer record, the following exception occured: " + str(e))
        return self.lecroyObj

    def stopAnalyzerRecording(self): #TODO need to do two  functions one of them stopRecording that checking if its exerciser Test Generation eneded and one of them doesnt check it if the function that checks if generation ended need to add time out for it
            self.lecroyObj.StopRecording(False)
            print("Stop Analyzer record")
            self.controller.updateRunTimeStateInTerminal(self.lecroyObj.hostPc, self.lecroyObj.testLog, "\n Stop Analyzer record")
            del self.rec_options  # delete recording options instance
            while (isTraceCreatedPerAnalyzer[self.lecroyObj.traceReady] == False):
                sleep(0.2)
                pythoncom.PumpWaitingMessages()
                print("PumpWaitingMessages")
            del self.lecroyObj

    def loadGenerationOptionToExerciser(self, lecroyObj,generationOptionFullPath):
        lecroyObj.GetGenerationOptions().Load(generationOptionFullPath)

    def startGenerationScriptOnExerciser(self,lecroyObj,generationScriptFullPathAndName):
        lecroyObj.StartGeneration(generationScriptFullPathAndName, 0, 0)

    def verifyExerciserGenerationScriptFinished(self):
        while resetExerciserGenerationScriptState != 1:
            sleep(0.2)
            pythoncom.PumpWaitingMessages()
            print("PumpWaitingMessages")
        self.resetExerciserGenerationScriptState()
        return True

    def resetExerciserGenerationScriptState(self):
        global resetExerciserGenerationScriptState
        resetExerciserGenerationScriptState = 0
    def getGenerationState(self):
        global resetExerciserGenerationScriptState
        return resetExerciserGenerationScriptState