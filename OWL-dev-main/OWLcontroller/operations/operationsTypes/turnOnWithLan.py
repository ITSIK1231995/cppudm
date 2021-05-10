import platform
from operations.operation import operation
import subprocess
from wakeonlan import send_magic_packet
from getmac import get_mac_address

class turnOnWithLan(operation):

    def getKey(self):
        ''' Returns operation's name '''
        return (type(self).__name__)

    @staticmethod
    def PCOnAfterTest():#well the pc be on after test finishes
        return True

    @staticmethod
    def asumesPcOnBeforeTest():#does the test asumes the pc well be on before runing
        return False

    @staticmethod
    def pingIP(ipAddress):
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
            ) == "windows" else 'c', ipAddress), shell=True, universal_newlines=True)
            if 'unreachable' in output:
                return False
            return True
        except Exception:
            return False


    @staticmethod
    def fetchMacAddress(hostIP):
        hostPcMacAdress = get_mac_address(ip=hostIP)
        return hostPcMacAdress


    def runOp(self,controllerPc,hostPc,testLog,opParams):
        controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\n turn on with lan command has started \n ")

        controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\n wake on lun magic packet has been sent ")
        macAdress = turnOnWithLan.fetchMacAddress(hostPc["IP"])
                # wake on lan
        send_magic_packet(macAdress,ip_address=hostPc["IP"],port= controllerPc.configs.defaultConfContent['hostPcServerPort'])
        controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\n Wake on lan has been sent, pinging the host for checking if it's on")
        hostPcIsOn = operation.waitForPcToTurnOn(self,controllerPc,hostPc,testLog)
        if hostPcIsOn:
            controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\nWake on lun succeed and the PC is ON")
        else:
            controllerPc.updateRunTimeStateInTerminal(hostPc, testLog, "\nWake on lun Failed and the PC is still off")
        return hostPcIsOn







