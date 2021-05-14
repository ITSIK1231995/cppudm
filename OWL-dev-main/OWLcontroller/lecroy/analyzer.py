from win32com.client import DispatchWithEvents, Dispatch
from time import sleep, time
import pythoncom
import os
traceCreatedPerAnalyzer = []

class PEEvent(object):
    saveTraceFullPath = ""
    trace_ready = False
    def OnTraceCreated(self, trace):
        try:
            print("PEEvent::OnTraceCreated - %s" % trace)
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog, "PE-Event:: On Trace Created")
            trace_obj = Dispatch(trace)  # Dispatch trace object
            trace_obj.Save(self.__class__.saveTraceFullPath)  # Save trace file
            trace_obj.Close()  # close trace file
            del trace_obj  # delete trace dispatch instance
            # self.__class__.trace_ready = True  # set global flag to True
            traceCreatedPerAnalyzer[self.__class__.trace_ready] = True
        except Exception as e:
            print("PEEvent::OnTraceCreated failed with exception: %s" % e)
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog,
                                                                   "PEEvent::OnTraceCreated failed with exception: %s" % e)

    @staticmethod
    def getTraceReadinessState(self):
        return self.__class__.trace_ready

    def OnStatusReport(self, subsystem, state, percent_done):
        try:
            print("PEEvent::OnStatusReport - subsystem:{0}, state:{1}, progress:{2}".format(subsystem, state,percent_done))
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog,
                                                                   "PEEvent::OnStatusReport - subsystem:{0}, state:{1}, progress:{2}".format(subsystem, state,percent_done))
        except Exception as e:
            print("PEEvent::OnStatusReport failed with exception: %s" % e)
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog,
                                                                   "PEEvent::OnStatusReport failed with exception: %s" % e)
class analyzerHandler():
    def __init__(self,controller):
        self.traceFileName = "data.pex"  # default trace file name used in recording options
        self.controller = controller

    def startRecordingWithAnalyzer(self,recOptionsFullPath,saveTraceFullPath,savedTraceName,hostPc,testLog):
        os.system("TASKKILL /F /IM PETracer.exe")
        traceCreatedPerAnalyzer.append(False)
        self.CopyOfPEEvent = type('copyOfPEevent', PEEvent.__bases__, dict(PEEvent.__dict__)) # Lecroy's implement for events limitng us from sending data into the PEevent class, therfore instead of using workarounds or not using the events wre creating a new class and not a new instance each time which will be released at the end of each run
        self.CopyOfPEEvent.saveTraceFullPath = saveTraceFullPath + "\\" + savedTraceName + ".pex"
        self.CopyOfPEEvent.trace_ready = 0
        self.CopyOfPEEvent.hostPc = hostPc
        self.CopyOfPEEvent.testLog = testLog
        self.CopyOfPEEvent.controller = self.controller
        self.analyzerObj = DispatchWithEvents("CATC.PETracer", self.CopyOfPEEvent)
        self.rec_options = self.analyzerObj.GetRecordingOptions()
        self.rec_options.SetTraceFileName(self.traceFileName)
        self.analyzerObj.StartRecording(recOptionsFullPath)  # here you need to pass rec options file path or empty string
        print("Start Analyzer record")
        self.controller.updateRunTimeStateInTerminal(self.CopyOfPEEvent.hostPc, self.CopyOfPEEvent.testLog,"\n Start Analyzer record")

    def stopRecording(self):
        self.analyzerObj.StopRecording(False)
        print("Stop Analyzer record")
        self.controller.updateRunTimeStateInTerminal(self.CopyOfPEEvent.hostPc, self.CopyOfPEEvent.testLog, "\n Stop Analyzer record")
        # You can use this to get default file path for recording
        print(self.rec_options.GetFileName())
        del self.rec_options  # delete recording options instance
        while (traceCreatedPerAnalyzer[self.CopyOfPEEvent.trace_ready] == False):
            sleep(0.2)
            pythoncom.PumpWaitingMessages()
            print("PumpWaitingMessages")
        del self.analyzerObj  # delete analyzer dispatch instance