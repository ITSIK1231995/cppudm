import os
from win32com.client import DispatchWithEvents, WithEvents

class PEEvent(object):
    def OnTraceCreated(self, trace):
        try:
            print("PEEvent::OnTraceCreated - %s" % trace)
        except Exception as e:
            print("PEEvent::OnTraceCreated failed with exception: %s" % e)

    def OnStatusReport(self, subsystem, state, percent_done):
        try:
            print("PEEvent::OnStatusReport - subsystem:{0}, state:{1}, progress:{2}".format(subsystem, state,
                                                                                            percent_done))
        except Exception as e:
            print("PEEvent::OnStatusReport failed with exception: %s" % e)
# class for for handling VSE events
class VSEventHandler(object):
    def OnVScriptReportUpdated(self, new_line, tag):
        try:
            print("VSEventHandler::OnVScriptReportUpdated - %s tag:%s" % (new_line, tag))
        except Exception as e:
            print("VSEventHandler::OnVScriptReportUpdated - failed with exception: %s" % e)

    def OnVScriptFinished(self, script_name, result, tag):
        try:
            print("VSEventHandler::OnVScriptFinished - {script_name}, {result}, {tag}".format(script_name=script_name,
                                                                                              result=result,
                                                                                              tag=tag))
        except Exception as e:
            print("VSEventHandler::OnVScriptFinished - failed with exception: %s" % e)

    def OnNotifyClient(self, eventId, eventBody, tag):
        try:
            print("VSEventHandler::OnNotifyClient - eventId: %s, eventBody: %s, tag: %s" % (eventId, eventBody, tag))
        except Exception as e:
            print("VSEventHandler::OnNotifyClient - failed with exception: %s" % e)

class VSE():
    def startVerificationScriptEngine(self, traceFullPathAndName, vScriptFullPathAndName):
        # TraceName = "C:\\Users\\Public\\Documents\\LeCroy\\PCIe Protocol Suite\\Sample Files\\Training_x8.pex"
        # VScriptName = "C:\\Users\\Public\\Documents\\LeCroy\\PCIe Protocol Suite\\Scripts\\VFScripts\\Examples\\" \
        #               "examp_nvme_errors.pevs"
        Analyzer = DispatchWithEvents("CATC.PETracer", PEEvent)  # using dispatch with events
        Trace = Analyzer.OpenFile(traceFullPathAndName)
        VSEngine = Trace.GetVScriptEngine(vScriptFullPathAndName)
        handler = WithEvents(VSEngine, VSEventHandler)
        VSEngine.Tag = 12
        Result = VSEngine.RunVScript()  # run VSE script and get result
        if Result == 1:
            print ("VSE's results: PASSED !!! ")
        else:
            print ("VSE's results: FAILED !!!")
        os.system("TASKKILL /F /IM PETracer.exe")
        print("VSE script execution has finished")
