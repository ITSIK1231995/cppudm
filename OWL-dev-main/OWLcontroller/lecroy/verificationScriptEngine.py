import os
from lecroy.dispatchComObj import dispatchComObj

class PEEvent(object):
    def __init__(self,hostPc,testLog,controller):
        self.hostPc = hostPc
        self.testLog = testLog
        self.controller = controller

    def OnTraceCreated(self, trace):
        try:
            print("PEEvent::OnTraceCreated - %s" % trace)
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog,"\nPEEvent::OnTraceCreated - %s" % trace)
        except Exception as e:
            print("PEEvent::OnTraceCreated failed with exception: %s" % e)
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog,"\nPEEvent::OnTraceCreated failed with exception: %s" % e)

    def OnStatusReport(self, subsystem, state, percent_done):
        try:
            print("PEEvent::OnStatusReport - subsystem:{0}, state:{1}, progress:{2}".format(subsystem, state,percent_done))
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog, "PEEvent::OnStatusReport - subsystem:{0}, state:{1}, progress:{2}".format(subsystem, state,percent_done))
        except Exception as e:
            print("PEEvent::OnStatusReport failed with exception: %s" % e)
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog,"PEEvent::OnStatusReport failed with exception: %s" % e)

# class for for handling VSE events
class VSEventHandler(object):
    def __init__(self,hostPc,testLog,controller):
        self.hostPc = hostPc
        self.testLog = testLog
        self.controller = controller

    def OnVScriptReportUpdated(self, new_line, tag):
        try:
            print("VSEventHandler::OnVScriptReportUpdated - %s tag:%s" % (new_line, tag))
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog,"VSEventHandler::OnVScriptReportUpdated - %s tag:%s" % (new_line, tag))
        except Exception as e:
            print("VSEventHandler::OnVScriptReportUpdated - failed with exception: %s" % e)
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog,"VSEventHandler::OnVScriptReportUpdated - failed with exception: %s" % e)

    def OnVScriptFinished(self, script_name, result, tag):
        try:
            print("VSEventHandler::OnVScriptFinished - {script_name}, {result}, {tag}".format(script_name=script_name,result=result,tag=tag))
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog,"VSEventHandler::OnVScriptFinished - {script_name}, {result}, {tag}".format(script_name=script_name,result=result,tag=tag))
        except Exception as e:
            print("VSEventHandler::OnVScriptFinished - failed with exception: %s" % e)
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog,"VSEventHandler::OnVScriptFinished - failed with exception: %s" % e)

    def OnNotifyClient(self, eventId, eventBody, tag):
        try:
            print("VSEventHandler::OnNotifyClient - eventId: %s, eventBody: %s, tag: %s" % (eventId, eventBody, tag))
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog,"VSEventHandler::OnNotifyClient - eventId: %s, eventBody: %s, tag: %s" % (eventId, eventBody, tag))
        except Exception as e:
            print("VSEventHandler::OnNotifyClient - failed with exception: %s" % e)
            self.controller.updateRunTimeStateInTerminal(self.hostPc, self.testLog,"VSEventHandler::OnNotifyClient - failed with exception: %s" % e)

class verificationScriptEngine():
    def startVerificationScript(self, traceFullPathAndName, vScriptFullPathAndName, hostPc, testLog, controller):
        print("\nVerification Script Engine procedure has started")
        os.system("TASKKILL /F /IM PETracer.exe")
        controller.updateRunTimeStateInTerminal(hostPc, testLog,"\nVerification Script Engine procedure has started")
        Analyzer = dispatchComObj.DispatchWithEventsAndParams("CATC.PETracer", PEEvent, [hostPc, testLog, controller])  # using dispatch with events
        Trace = Analyzer.OpenFile(traceFullPathAndName)
        VSEngine = Trace.GetVScriptEngine(vScriptFullPathAndName)
        handler = dispatchComObj.DispatchWithEventsAndParams(VSEngine, VSEventHandler, [hostPc, testLog, controller])
        VSEngine.Tag = 12
        Result = VSEngine.RunVScript()  # run VSE script and get result
        if Result == 1:
            print ("\nVerification Script Engine final result: PASSED !!! ")
            controller.updateRunTimeStateInTerminal(hostPc, testLog,"\nVerification Script Engine final result: PASSED !!! ")
        else:
            print ("\nVerification Script Engine final result: FAILED !!!")
            controller.updateRunTimeStateInTerminal(hostPc, testLog,"\nVerification Script Engine final result: FAILED !!!")
        os.system("TASKKILL /F /IM PETracer.exe")
        print("Verification Script Engine procedure has finished")
        controller.updateRunTimeStateInTerminal(hostPc, testLog,"\nVerification Script Engine procedure has finished")
        return Result
