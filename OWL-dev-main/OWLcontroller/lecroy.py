import _thread
import os
import threading
import time
from collections import namedtuple
import win32com.client
import win32com






class lecroy():

    def __init__(self):
        self.threadLock = threading.Lock()
        self.makeRecordingWasDone = False
        self.AnalyzerHandlingEnded = False

    def startAnalyzerRecord(self,recOptionsFullPath,saveTraceFullPath,savedTraceName):
        return _thread.start_new_thread(self.dispatchAnalyzerRecord, (recOptionsFullPath,saveTraceFullPath,savedTraceName,))


    def dispatchAnalyzerRecord(self,recOptionsFullPath,saveTraceFullPath,savedTraceName):
        self.threadLock.acquire()
        recOptionsFullPath = 'C:\\Users\\Public\\Documents\\LeCroy\\PCIe Protocol Suite\\Automation\\python\\Input\\test_ro.rec'
        #saveTraceFullPath = 'C:\\Users\\Public\\Documents\\LeCroy\\PCIe Protocol Suite\\Automation\\python\\Output\\'
        #savedTraceName = 'PCIe_seqrecc_dataForth1'
        os.system("TASKKILL /F /IM PETracer.exe")
        analyzerInfo = namedtuple('analyzerInfo', ['AnalyzerObj', 'Trace', 'SavedTracePathAndName'])
        # Initialize the Analyzer object
        self.Analyzer = win32com.client.Dispatch("CATC.PETracer")
        #
        # In the piece of code below we perform 4 sequential recordings and
        # save the traces recorded in the current folder
        #
        RecOptions = recOptionsFullPath  # Example: getcwd() + r"\Input\test_ro.rec"
        SavedTraceLocation = saveTraceFullPath  # Example: getcwd() + "\Output\\"

        self.SavedTrace = SavedTraceLocation + "\\" + savedTraceName + ".pex"  # Example for savedTraceName: "PCIe_seqrec_data"
        # Tell the PCIe analyzer to start recording....

        self.Trace = self.Analyzer.MakeRecording(RecOptions)
        print ("!!!!!!!!!!!!!!!!!!!! Thread passed the make recording func !!!!!!!!!!!!!!!!!!!!!!!!!!")

        # Imitation of some activity - just sleep for 3 seconds.
        time.sleep(3)
        self.makeRecordingWasDone = True
        analyzerInfo.AnalyzerObj = self.Analyzer
        analyzerInfo.Trace = self.Trace
        analyzerInfo.SavedTracePathAndName = self.SavedTrace
        self.stopAnalyzerRecord()
        self.threadLock.release()



    def stopAnalyzerRecord(self):
        while self.makeRecordingWasDone == False:
            time.sleep(1)
        # Tell the analyzer to stop recording and give the trace acquired.

        self.Analyzer.StopRecording(False)
        print("!!!!!!!!!!!!!!!!!!!! Thread passed the stop recording func !!!!!!!!!!!!!!!!!!!!!!!!!!")
        # Save the trace in the current folder
        # Trace.Save(SavedTrace,0,10)
        self.Trace.Save(self.SavedTrace)

        # Release the analyzer ...
        # Analyzer = None
        os.system("TASKKILL /F /IM PETracer.exe")
        self.AnalyzerHandlingEnded = True