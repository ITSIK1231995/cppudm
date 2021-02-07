import os
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


    #todo: if expacting pc to turnOff - test conection untill pc is off or threashhold exceded then return true
    #todo: if expacting pc to turnOn - test conection untill pc is ON or threashhold exceded then return true
    def waitForPcToTurnOn(self,controllerPc,hostPc,testLog): # when PC is ON output is True
        controllerPc.updateRunTimeState(hostPc,testLog, " \n Pinging Host until it's On  \n ")
        clientSocket = socket.socket()
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        attempsToConnectSocket = controllerPc.configs.defaultConfContent['attempsToCreateSocket']
        for i in range(attempsToConnectSocket):
            try:
                clientSocket.connect((hostPc["IP"], port))  # connect to the server
                clientSocket.send("Test".encode())
                clientSocket.close()
                controllerPc.updateRunTimeState(hostPc,testLog,"\nwaitForPcToTurnOn - PC is ON")
                return True
            except socket.error as e:
                controllerPc.updateRunTimeState(hostPc,testLog,"\nwaitForPcToTurnOn - PC is OFF atempt "+ str(i))
                pass
        return False

    # def waitForPcToTurnOff(self,controllerPc,hostPc): # when PC is off output is True
    #     controllerPc.updateRunTimeState(hostPc, " \n Pinging Host until it's off  \n ")
    #     clientSocket = socket.socket()
    #     port = controllerPc.configs.defaultConfContent['hostPcServerPort']
    #     attempsToConnectSocket = controllerPc.configs.defaultConfContent['attempsToCreateSocket']
    #     for i in range(attempsToConnectSocket):
    #         try:
    #             clientSocket.connect((hostPc["IP"], port))  # connect to the server
    #             clientSocket.send("Test".encode())
    #             clientSocket.close()
    #             controllerPc.updateRunTimeState(hostPc, "\nwaitForPcToTurnOff - PC is ON atempt "+ str(i))
    #         except socket.error as e:
    #             controllerPc.updateRunTimeState(hostPc, "\nwaitForPcToTurnOff - PC is OFF")
    #             return True
    #     return False

    def waitForPcToTurnOff(self,controllerPc,hostPc,testLog):
        attempsToConnectSocket = controllerPc.configs.defaultConfContent['attempsToCreateSocket']
        for i in range(attempsToConnectSocket):
            # response = os.system("ping -n 4 " + hostPc["IP"])
            response = subprocess.run(["ping","-n","4",hostPc["IP"]], stdout=subprocess.PIPE).stdout.decode('utf-8')
            # and then check the response...
            print(">>>>> ping response = " + str(response))
            if len(re.findall("unreachable", response)) == 4 or \
                    len(re.findall("timed out", response)) == 4:
            # if "unreachable" in response or "timed out" in response:
                if 'postPingWaitingTime' in hostPc:
                    controllerPc.updateRunTimeState(hostPc, testLog,"\n Awaiting for " + str(hostPc['postPingWaitingTime']) + "seconds")
                    time.sleep(hostPc['postPingWaitingTime'])
                controllerPc.updateRunTimeState(hostPc,testLog, "\nwaitForPcToTurnOff - PC is OFF")
                return True
            controllerPc.updateRunTimeState(hostPc,testLog, "\nwaitForPcToTurnOff - PC is ON atempt "+ str(i))
        return False


    def checkIfPcisOn(self,controllerPc,hostPc):
        clientSocket = socket.socket()  # instantiate
        port = controllerPc.configs.defaultConfContent['hostPcServerPort']
        attempsToConnectSocket = controllerPc.configs.defaultConfContent['attempsToCreateSocket']
        i = 0
        while True:
            try:
                clientSocket.connect((hostPc["IP"], port))  # connect to the server
                clientSocket.send("Test".encode())
            except socket.error as e:
                if i < attempsToConnectSocket:
                    i += 1
                    continue
                else:
                    return False
            break
        clientSocket.close()
        return True

        # try:
        #     clientSocket.connect((hostPc["IP"], port))  # connect to the server
        # except socket.error as e:
        #     return False
        # clientSocket.close()
        # return True



#todo : make a calss (in a diffrent folder) opration with socket that inherents from opration and includes all functions that manage sockets
#todo : make all oprations use hostPC as the data provider
#todo : use sockets in order to test if computer is on
#todo : make all oprations inherent from opration or oprationWithSucket