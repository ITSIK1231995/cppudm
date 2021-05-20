from win32com.client import Dispatch
from time import sleep
import pythoncom
import os

from win32com.universal import com_error

from lecroy.dispatchComObj import dispatchComObj

isTraceCreatedPerAnalyzer = []

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
        except Exception as e:
            print("PEEvent::OnStatusReport failed with exception: %s" % e)
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog,"PEEvent::OnStatusReport failed with exception: %s" % e)

class analyzerHandler():
    def __init__(self,controller):
        self.traceFileName = "data.pex"  # default trace file name used in recording options
        self.controller = controller

    def startRecordingWithAnalyzer(self,recOptionsFullPath,SavedTraceFullPathAndName,hostPc,testLog):
        os.system("TASKKILL /F /IM PETracer.exe")
        traceReady = 0 #TODO need to change the name of it to  analzyer index
        isTraceCreatedPerAnalyzer.insert(traceReady, False) # the "0" indicates a place in the traceCreatedPerAnalyzer list, each item in this list will represent analyzer
        self.analyzerObj = dispatchComObj.DispatchWithEventsAndParams("CATC.PETracer", PEEvent, [SavedTraceFullPathAndName, traceReady, hostPc, testLog, self.controller])
        self.rec_options = self.analyzerObj.GetRecordingOptions()
        self.rec_options.SetTraceFileName(self.traceFileName)
        print("Start Analyzer record")
        self.controller.updateRunTimeStateInTerminal(self.analyzerObj.hostPc, self.analyzerObj.testLog,"\n Start Analyzer record")  # TODO need to change the name of updateRunTimeStateInTerminal to updateTernimalAndLog
        try:
            self.analyzerObj.StartRecording(recOptionsFullPath)  # here you need to pass rec options file path or empty string
        except com_error as e:
            print(str(e))
            self.controller.updateRunTimeStateInTerminal(self.analyzerObj.hostPc, self.analyzerObj.testLog,
                                                         "\n While trying to start the Analzyer record, the following exception occured: " + str(e))

    def stopRecording(self):
        self.analyzerObj.StopRecording(False)
        print("Stop Analyzer record")
        self.controller.updateRunTimeStateInTerminal(self.analyzerObj.hostPc, self.analyzerObj.testLog, "\n Stop Analyzer record")
        del self.rec_options  # delete recording options instance
        while (isTraceCreatedPerAnalyzer[self.analyzerObj.traceReady] == False):
            sleep(0.2)
            pythoncom.PumpWaitingMessages()
            print("PumpWaitingMessages")
        del self.analyzerObj  # delete analyzer dispatch instance
        os.system("TASKKILL /F /IM PETracer.exe")