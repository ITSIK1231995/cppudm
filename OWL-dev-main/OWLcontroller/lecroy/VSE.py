import os
import win32api
import win32com
from win32com.client import DispatchWithEvents, WithEvents
from copy import deepcopy


# ----
from win32com.client import Dispatch
from win32com.client import gencache
from win32com.client import getevents
from win32com.client import EventsProxy
import pythoncom

def _event_setattr_(self, attr, val):
    try:
        # Does the COM object have an attribute of this name?
        self.__class__.__bases__[0].__setattr__(self, attr, val)
    except AttributeError:
        # Otherwise just stash it away in the instance.
        self.__dict__[attr] = val

def DispatchWithEventsNew(clsid, user_event_class, arguments):
    # Create/Get the object.
    disp = Dispatch(clsid)
    if not disp.__class__.__dict__.get("CLSID"): # Eeek - no makepy support - try and build it.
        try:
            ti = disp._oleobj_.GetTypeInfo()
            disp_clsid = ti.GetTypeAttr()[0]
            tlb, index = ti.GetContainingTypeLib()
            tla = tlb.GetLibAttr()
            gencache.EnsureModule(tla[0], tla[1], tla[3], tla[4], bValidateFile=0)
            # Get the class from the module.
            disp_class = gencache.GetClassForProgID(str(disp_clsid))
        except pythoncom.com_error:
            raise TypeError("This COM object can not automate the makepy process - please run makepy manually for this object")
    else:
        disp_class = disp.__class__
    # If the clsid was an object, get the clsid
    clsid = disp_class.CLSID
    # Create a new class that derives from 3 classes - the dispatch class, the event sink class and the user class.
    # XXX - we are still "classic style" classes in py2x, so we need can't yet
    # use 'type()' everywhere - revisit soon, as py2x will move to new-style too...
    try:
        from types import ClassType as new_type
    except ImportError:
        new_type = type # py3k
    events_class = getevents(clsid)
    if events_class is None:
        raise ValueError("This COM object does not support events.")
    result_class = new_type("COMEventClass", (disp_class, events_class, user_event_class), {"__setattr__" : _event_setattr_})
    instance = result_class(disp._oleobj_) # This only calls the first base class __init__.
    events_class.__init__(instance, instance)
    args = [instance] + arguments
    if hasattr(user_event_class, "__init__"):
        user_event_class.__init__(*args)
    return EventsProxy(instance)

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

class VSE():
    def startVerificationScriptEngine(self, traceFullPathAndName, vScriptFullPathAndName,hostPc, testLog, controller):
        Analyzer = DispatchWithEventsNew("CATC.PETracer", PEEvent,[hostPc,testLog,controller])  # using dispatch with events
        Trace = Analyzer.OpenFile(traceFullPathAndName)
        VSEngine = Trace.GetVScriptEngine(vScriptFullPathAndName)
        handler = DispatchWithEventsNew(VSEngine, VSEventHandler,[hostPc,testLog,controller])
        VSEngine.Tag = 12
        Result = VSEngine.RunVScript()  # run VSE script and get result
        if Result == 1:
            print ("VSE's results: PASSED !!! ")
            controller.updateRunTimeStateInTerminal(hostPc, testLog,"\nVSE's results: PASSED !!! ")
        else:
            print ("VSE's results: FAILED !!!")
            controller.updateRunTimeStateInTerminal(hostPc, testLog,"\nVSE's results: FAILED !!!")
        os.system("TASKKILL /F /IM PETracer.exe")
        # del self.CopyOfPEEvent
        print("VSE script execution has finished")
        controller.updateRunTimeStateInTerminal(hostPc, testLog,"\nVSE script execution has finished")
        return Result
