import os
import subprocess
import psutil
import logging


CMD_COMMAND = 'cmd /k '
DM_SCRIPT_NAME = 'L1.2_Entry_Exit_PS4_Calypso.srt'
DM_SCRIPT_PATH = 'C:\OWL\OWL-dev\OWLhostPC'
EXECUTE_DM = r'DriveMaster.exe /s:'
LOG_PATH = 'C:\Dmtests\OWLdmLastLog.txt'
LOG_PATH_DM_SYNTAX = ' /l:C:\Dmtests\OWLdmLastLog.txt /e'
RUN_DM_CMD = EXECUTE_DM + DM_SCRIPT_PATH + DM_SCRIPT_NAME + LOG_PATH_DM_SYNTAX

class runDM():

    @staticmethod
    def runOp(hostPcServerRef,socket,userPath):
        path = os.getcwd()
        runDMCmd = EXECUTE_DM + path + userPath + LOG_PATH_DM_SYNTAX
        command = runDMCmd
        run = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=None, stderr=subprocess.PIPE,
                               env=os.environ, universal_newlines=True)
        returncode = run.communicate()  ## HANGS HERE ##
        if runDM.checkIfProcessRunning("DriveMaster"):
            logging.info("DriveMaster process is running")
        else:
            logging.info("DriveMaster process is not running")
        with open(LOG_PATH, 'r') as file:
            data = file.read()
        socket.send(data.encode())  # send data to the client


    @staticmethod
    def checkIfProcessRunning(processName):
        '''
        Check if there is any running process that contains the given name processName.
        '''
        #Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if processName.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
