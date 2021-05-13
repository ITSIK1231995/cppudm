# import _thread
# import os
# import threading
# import time
# from collections import namedtuple
# import win32com.client
# import win32com
#
# class analyzer():
#     def __init__(self):
#         self.threadLock = threading.Lock()
#         self.makeRecordingWasDone = False
#         self.AnalyzerHandlingEnded = False
#
#     def startAnalyzerRecord(self,recOptionsFullPath,saveTraceFullPath,savedTraceName):
#         return _thread.start_new_thread(self.dispatchAnalyzerRecord, (recOptionsFullPath,saveTraceFullPath,savedTraceName,))
#
#     def dispatchAnalyzerRecord(self,recOptionsFullPath,saveTraceFullPath,savedTraceName):
#         self.threadLock.acquire()
#         os.system("TASKKILL /F /IM PETracer.exe")
#         analyzerInfo = namedtuple('analyzerInfo', ['AnalyzerObj', 'Trace', 'SavedTracePathAndName'])
#         # Initialize the Analyzer object
#         self.Analyzer = win32com.client.Dispatch("CATC.PETracer")
#         RecOptions = recOptionsFullPath  # Example: getcwd() + r"\Input\test_ro.rec"
#         SavedTraceLocation = saveTraceFullPath  # Example: getcwd() + "\Output\\"
#         self.SavedTrace = SavedTraceLocation + "\\" + savedTraceName + ".pex"  # Example for savedTraceName: "PCIe_seqrec_data"
#         # Tell the PCIe analyzer to start recording....
#         self.Trace = self.Analyzer.MakeRecording(RecOptions)
#         print ("!!!!!!!!!!!!!!!!!!!! Thread passed the make recording func !!!!!!!!!!!!!!!!!!!!!!!!!!")
#         # Imitation of some activity - just sleep for 3 seconds.
#         time.sleep(3)
#         self.makeRecordingWasDone = True
#         analyzerInfo.AnalyzerObj = self.Analyzer
#         analyzerInfo.Trace = self.Trace
#         analyzerInfo.SavedTracePathAndName = self.SavedTrace
#         self.stopAnalyzerRecord()
#         self.threadLock.release()
#
#     def stopAnalyzerRecord(self):
#         while self.makeRecordingWasDone == False:
#             time.sleep(1)
#         # Tell the analyzer to stop recording and give the trace acquired.
#         self.Analyzer.StopRecording(False)
#         print("!!!!!!!!!!!!!!!!!!!! Thread passed the stop recording func !!!!!!!!!!!!!!!!!!!!!!!!!!")
#         # Save the trace in the current folder
#         # Trace.Save(SavedTrace,0,10)
#         self.Trace.Save(self.SavedTrace)
#         # Release the analyzer ...
#         # Analyzer = None
#         os.system("TASKKILL /F /IM PETracer.exe")
#         self.AnalyzerHandlingEnded = True
import os

from win32com.client import DispatchWithEvents, Dispatch
from sys import exit
from time import sleep, time
import pythoncom
isTraceReady = False  # global flag, indicates that trace is ready

class analyzerHandler(object):
    def __init__(self):
        # User variables
        #self.traceRecordedeSavingPathWithTraceName = "C:/Temp/trace.pex"  # path where to save trace file
        self.traceCreatedInDefaultLocation = "data.pex"  # default trace file name used in recording options
        #self.recordingOptionsFilePath = "DO_NOT_CHANGE_RECORDING_OPTIONS"  # path to recording options used when recording trace,
        # if DO_NOT_CHANGE_RECORDING_OPTIONS - default will be used
        timeout = 1  # time out between start and stop of recording in seconds
        # Global variables

    def OnTraceCreated(self, trace):
        try:
            print("PEEvent::OnTraceCreated - %s" % trace)
            trace_obj = Dispatch(trace)  # Dispatch trace object
            trace_obj.Save(self.traceRecordedeSavingPathWithTraceName)  # Save trace file
            trace_obj.Close()  # close trace file
            del trace_obj  # delete trace dispatch instance
            global isTraceReady
            isTraceReady = True  # set global flag to True
        except Exception as e:
            print("PEEvent::OnTraceCreated failed with exception: %s" % e)

    def OnStatusReport(self, subsystem, state, percent_done):
        try:
            print("PEEvent::OnStatusReport - subsystem:{0}, state:{1}, progress:{2}".format(subsystem, state,
                                                                                            percent_done))
        except Exception as e:
            print("PEEvent::OnStatusReport failed with exception: %s" % e)

    def startRecording(self,recordingOptionsFilePath,SavedTraceFullPath, savedTraceName):
        self.traceRecordedeSavingPathWithTraceName = SavedTraceFullPath + "\\" +savedTraceName
        os.system("TASKKILL /F /IM PETracer.exe")
        self.dispatchedAnalyzerObj = DispatchWithEvents("CATC.PETracer", analyzerHandler)  # using dispatch with events
        # You can use this to set default file name before recording
        self.rec_options = self.dispatchedAnalyzerObj.GetRecordingOptions()
        self.rec_options.SetTraceFileName(self.traceCreatedInDefaultLocation)

        self.dispatchedAnalyzerObj.StartRecording(recordingOptionsFilePath)  # here you need to pass rec options file path or empty string
        print("StartRecording")

        # sleep(timeout)  # put some timeout before stop recording

    def stopRecording(self):
        self.dispatchedAnalyzerObj.StopRecording(False)
        print("StopRecording")

        # You can use this to get default file path for recording
        print(self.rec_options.GetFileName())

        del self.rec_options  # delete recording options instance

        while (isTraceReady == False):
            sleep(0.2)
            pythoncom.PumpWaitingMessages()
            print("Awaiting for event tells us the trace is ready")

        del self.dispatchedAnalyzerObj  # delete analyzer dispatch instance
        os.system("TASKKILL /F /IM PETracer.exe")
# analyzer = analyzerHandler()
# # analyzer.startRecording()
# # sleep(3)
# # analyzer.stopRecording()
# # print("EXIT")
# # exit(0)