import os
from win32com.client import DispatchWithEvents, WithEvents
from copy import deepcopy

class PEEvent(object):
    def OnTraceCreated(self, trace):
        try:
            print("PEEvent::OnTraceCreated - %s" % trace)
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog,"\nPEEvent::OnTraceCreated - %s" % trace)
        except Exception as e:
            print("PEEvent::OnTraceCreated failed with exception: %s" % e)
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog,"\nPEEvent::OnTraceCreated failed with exception: %s" % e)

    def OnStatusReport(self, subsystem, state, percent_done):
        try:
            print("PEEvent::OnStatusReport - subsystem:{0}, state:{1}, progress:{2}".format(subsystem, state,percent_done))
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog, "PEEvent::OnStatusReport - subsystem:{0}, state:{1}, progress:{2}".format(subsystem, state,percent_done))
        except Exception as e:
            print("PEEvent::OnStatusReport failed with exception: %s" % e)
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog,"PEEvent::OnStatusReport failed with exception: %s" % e)

# class for for handling VSE events
class VSEventHandler(object):
    def OnVScriptReportUpdated(self, new_line, tag):
        try:
            print("VSEventHandler::OnVScriptReportUpdated - %s tag:%s" % (new_line, tag))
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog,"VSEventHandler::OnVScriptReportUpdated - %s tag:%s" % (new_line, tag))
        except Exception as e:
            print("VSEventHandler::OnVScriptReportUpdated - failed with exception: %s" % e)
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog,"VSEventHandler::OnVScriptReportUpdated - failed with exception: %s" % e)

    def OnVScriptFinished(self, script_name, result, tag):
        try:
            print("VSEventHandler::OnVScriptFinished - {script_name}, {result}, {tag}".format(script_name=script_name,result=result,tag=tag))
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog,"VSEventHandler::OnVScriptFinished - {script_name}, {result}, {tag}".format(script_name=script_name,result=result,tag=tag))
        except Exception as e:
            print("VSEventHandler::OnVScriptFinished - failed with exception: %s" % e)
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog,"VSEventHandler::OnVScriptFinished - failed with exception: %s" % e)

    def OnNotifyClient(self, eventId, eventBody, tag):
        try:
            print("VSEventHandler::OnNotifyClient - eventId: %s, eventBody: %s, tag: %s" % (eventId, eventBody, tag))
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog,"VSEventHandler::OnNotifyClient - eventId: %s, eventBody: %s, tag: %s" % (eventId, eventBody, tag))
        except Exception as e:
            print("VSEventHandler::OnNotifyClient - failed with exception: %s" % e)
            self.__class__.controller.updateRunTimeStateInTerminal(self.__class__.hostPc, self.__class__.testLog,"VSEventHandler::OnNotifyClient - failed with exception: %s" % e)

class VSE():
    def startVerificationScriptEngine(self, traceFullPathAndName, vScriptFullPathAndName,hostPc, testLog, controller):
        self.CopyOfPEEvent = deepcopy(PEEvent)
        self.CopyOfPEEvent.hostPc = hostPc
        self.CopyOfPEEvent.testLog = testLog
        self.CopyOfPEEvent.controller = controller
        Analyzer = DispatchWithEvents("CATC.PETracer",  self.CopyOfPEEvent)  # using dispatch with events
        Trace = Analyzer.OpenFile(traceFullPathAndName)
        VSEngine = Trace.GetVScriptEngine(vScriptFullPathAndName)
        self.copyOfVSEventHandler = type('VSEventHandler', VSEventHandler.__bases__, dict(VSEventHandler.__dict__))
        self.copyOfVSEventHandler.hostPc = hostPc
        self.copyOfVSEventHandler.testLog = testLog
        self.copyOfVSEventHandler.controller = controller
        handler = WithEvents(VSEngine, self.copyOfVSEventHandler)
        VSEngine.Tag = 12
        Result = VSEngine.RunVScript()  # run VSE script and get result
        if Result == 1:
            print ("VSE's results: PASSED !!! ")
            controller.updateRunTimeStateInTerminal(hostPc, testLog,"\nVSE's results: PASSED !!! ")
        else:
            print ("VSE's results: FAILED !!!")
            controller.updateRunTimeStateInTerminal(hostPc, testLog,"\nVSE's results: FAILED !!!")
        os.system("TASKKILL /F /IM PETracer.exe")
        del self.CopyOfPEEvent
        print("VSE script execution has finished")
        controller.updateRunTimeStateInTerminal(hostPc, testLog,"\nVSE script execution has finished")
        return Result
