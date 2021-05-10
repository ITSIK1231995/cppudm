import time
from collections import namedtuple

import win32com


class lecroy():
    def startAnalyzerRecord(self,recOptionsFullPath,saveTraceFullPath,savedTraceName):
        analyzerInfo = namedtuple('analyzerInfo' , ['AnalyzerObj' , 'Trace', 'SavedTracePathAndName'])
        # Initialize the Analyzer object
        Analyzer = win32com.client.Dispatch("CATC.PETracer")
        #
        # In the piece of code below we perform 4 sequential recordings and
        # save the traces recorded in the current folder
        #
        RecOptions = recOptionsFullPath # Example: getcwd() + r"\Input\test_ro.rec"
        SavedTraceLocation = saveTraceFullPath # Example: getcwd() + "\Output\\"
        SavedTrace = SavedTraceLocation + savedTraceName + ".pex"	 # Example for savedTraceName: "PCIe_seqrec_data"
        # Tell the PCIe analyzer to start recording...
        Trace = Analyzer.MakeRecording(RecOptions)
        # Imitation of some activity - just sleep for 3 seconds.
        time.sleep(3)
        analyzerInfo.AnalyzerObj = Analyzer
        analyzerInfo.Trace = Trace
        analyzerInfo.SavedTracePathAndName = SavedTrace
        return analyzerInfo

    def stopAnalyzerRecording(self, analyzerInfo):
        # Tell the analyzer to stop recording and give the trace acquired.
        analyzerInfo.AnalyzerObj.StopRecording(False)

        # Save the trace in the current folder
        # Trace.Save(SavedTrace,0,10)
        analyzerInfo.Trace.Save(analyzerInfo.SavedTracePathAndName)

        # Release the analyzer ...
        Analyzer = None