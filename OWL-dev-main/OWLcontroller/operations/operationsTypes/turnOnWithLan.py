import socket
import subprocess
import platform
import time

from operations.operation import operation
import os
import subprocess # CMD commands and outputs


PING = 'ping '
class turnOnWithLan(operation):


    def getKey(self):
        ''' Returns operation's name '''
        return (type(self).__name__)

    @staticmethod
    def pingIP(current_ip_address):
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
            ) == "windows" else 'c', current_ip_address), shell=True, universal_newlines=True)
            if 'unreachable' in output:
                return False
            return True
        except Exception:
            return False


    @staticmethod
    def getMacAdress(hostPc):
        def getMac():
            return subprocess.run("arp -a 10.100.102.22", stdout=subprocess.PIPE).stdout.decode('utf-8')

        from subprocess import Popen, PIPE
        import re
        IP = hostPc["IP"]
    # do_ping(IP)
        pingCommand = "arp -a" + hostPc["IP"]
        print(getMac())
        subprocess.run(["arp -a 10.100.102.22"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        os.system(pingCommand)
        # The time between ping and arp check must be small, as ARP may not cache long

        pid = Popen(["arp", "-n", IP], stdout=PIPE)
        s = pid.communicate()[0]
        mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", str(s)).groups()[0]
        print(mac)



    def runOp(self,controllerPc,hostPc,opParams):
        controllerPc.updateRunTimeState(hostPc, "\n turn on with lan command has started \n ")
        #macAdress = turnOnWithLan.getMacAdress(hostPc)
        controllerPc.updateRunTimeState(hostPc, "\n Verifies the Host is off before sending a wake on lan")
        hostPcIsOFf = operation.waitForPcToTurnOff(self,controllerPc,hostPc)
        if hostPcIsOFf:
            controllerPc.updateRunTimeState(hostPc, "\n Host is off - > Sends wake on lun ")
            macAdress = b'\x10\x65\x30\x2b\xe5\x87'
            # wake on lan
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b'\xff' * 6 + macAdress * 16,  #Host Pc MAC adress
                             (hostPc["IP"], 80)) # Host Pc IP
            controllerPc.updateRunTimeState(hostPc, "\n Wake on lan has been sent, pinging the host for checking if it's on... ")
            hostPcIsOn = operation.waitForPcToTurnOn(self,controllerPc,hostPc)

            if hostPcIsOn:
                controllerPc.updateRunTimeState(hostPc,"\nWake on lun succeed and the PC is ON")
            else:
                controllerPc.updateRunTimeState(hostPc,"\nWake on lun Failed and the PC is off")

            controllerPc.updateRunTimeState(hostPc,"\n turn on with lan command has ended \n ")
            return hostPcIsOn







