import os
import subprocess
import psutil
CMD_COMMAND = 'cmd /k '
DM_SCRIPT_NAME = 'L1.2_Entry_Exit_PS4_Calypso.srt'
DM_SCRIPT_PATH = 'C:\OWL\OWL-dev\OWLhostPC\DM_scripts\\'
EXECUTE_DM = r'DriveMaster.exe /s:'
LOG_PATH = ' /1:log.txt /e'
RUN_DM = EXECUTE_DM + DM_SCRIPT_PATH + DM_SCRIPT_NAME + LOG_PATH

class runDM():

    @staticmethod
    def runOp(userPath):
        #os.system(CMD_COMMAND + RUN_DM)
        runDM = EXECUTE_DM + userPath + LOG_PATH
        command = RUN_DM
        run = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=None, stderr=subprocess.PIPE,
                               env=os.environ, universal_newlines=True)
        returncode = run.communicate()  ## HANGS HERE ##

        if runDM().checkIfProcessRunning('DriveMaster'):
            print('A DriveMaster process is running')
        else:
            print('A DriveMaster process is not running')

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


# runDM.runOp()

