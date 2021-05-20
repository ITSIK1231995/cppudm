import socket
import subprocess
import time
import re

class operation(object):
    def getKey(self):
        pass

    @staticmethod
    def runOp(controllerPc,hostPc,testLog,opParams):
        pass

    @staticmethod
    def PCOnAfterTest():#well the pc be on after test finishes
        pass

    @staticmethod
    def asumesPcOnBeforeTest():#does the test asumes the pc well be on before runing
        pass

    def waitForPcToTurnOn(self,controllerPc,hostPc,testLog): # when PC is ON output is True
        controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, " \n Pinging Host until it's On  \n ")
        clientSocket = socket.socket()
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        attempsToConnectSocket = controllerPc.configs.defaultConfContent['attempsToCreateSocket']
        for i in range(attempsToConnectSocket):
            try:
                clientSocket.connect((hostPc["IP"], port))  # connect to the server
                clientSocket.send("Test".encode())
                clientSocket.close()
                controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\nwaitForPcToTurnOn - PC is ON")
                return True
            except socket.error as e:
                controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\nwaitForPcToTurnOn - PC is OFF atempt " + str(i))
                pass
        return False

#TODO the following two methoods reimplemnetd to be in minutes and not in connection attemps need to check them on a host pc
    def waitForPcToTurnOff(self,controllerPc,hostPc,testLog):
        maxMinutesToCreateSocket = controllerPc.configs.defaultConfContent['attempsToCreateSocket']
        timeToStopTryingCreatingSocket = time.time() + 60 * maxMinutesToCreateSocket
        while time.time() < timeToStopTryingCreatingSocket:
            # response = os.system("ping -n 4 " + hostPc["IP"])
            response = subprocess.run(["ping","-n","4",hostPc["IP"]], stdout=subprocess.PIPE).stdout.decode('utf-8')
            # and then check the response...
            print(">>>>> ping response = " + str(response))
            if len(re.findall("unreachable", response)) == 4 or \
                    len(re.findall("timed out", response)) == 4:
            # if "unreachable" in response or "timed out" in response:
                if 'postPingWaitingTime' in hostPc:
                    controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\n Awaiting for " + str(hostPc['postPingWaitingTime']) + "seconds")
                    time.sleep(hostPc['postPingWaitingTime'])
                controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\nwaitForPcToTurnOff - PC is OFF")
                return True
            controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\nwaitForPcToTurnOff - PC is ON attempt " + str(i))
        return False

    def checkIfPcisOn(self,controllerPc,hostPc):
        clientSocket = socket.socket()  # instantiate
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        maxMinutesToCreateSocket = controllerPc.configs.defaultConfContent['attempsToCreateSocket']
        timeToStopTryingCreatingSocket = time.time() + 60 * maxMinutesToCreateSocket
        while True:
            try:
                clientSocket.connect((hostPc["IP"], port))  # connect to the server
                clientSocket.send("Test".encode())
            except socket.error as e:
                if time.time() < timeToStopTryingCreatingSocket:
                    continue
                else:
                    return False
            break
        clientSocket.close()
        return True




