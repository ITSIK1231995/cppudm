import psutil
class runDM():

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


# Check if any chrome process was running or not.

if runDM().checkIfProcessRunning('chrome'):
    print('Yes a chrome process was running')
else:
    print('No chrome process is not running')



