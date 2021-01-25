import socket
import subprocess
import platform
from operations.operation import operation

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
            else:
                return True
        except Exception:
            return False
    # @staticmethod
    # def getMacAdress():
    #     import subprocess
    #     import sys
    #
    #     ip = '10.100.102.22'
    #
    #     # ping ip
    #     p = subprocess.Popen(['ping', ip, '-c1'], stdout=subprocess.PIPE,
    #                          stderr=subprocess.PIPE)
    #
    #     out, err = p.communicate()
    #
    #     # arp list
    #     p = subprocess.Popen(['arp', '-n'], stdout=subprocess.PIPE,
    #                          stderr=subprocess.PIPE)
    #
    #     out, err = p.communicate()
    #
    #     try:
    #
    #         arp = [x for x in out.split('\n') if ip in x][0]
    #     except IndexError:
    #         sys.exit(1)  # no arp entry found
    #     else:
    #         # get the mac address from arp list
    #         # bug: when the IP does not exists on the local network
    #         # this will print out the interface name
    #         print(
    #         ' '.join(arp.split()).split()[2])


    @staticmethod
    def runOp(hostPc,opParams):
        opParams.macAdress = b'\x10\x65\x30\x2B\xE5\x87'
        # pinging the host for checking if its on
        currentIpAdress = [opParams.hostIP]
        for each in currentIpAdress:
            if turnOnWithLan.pingIP(each):
                print("Host Pc is available")
            else:
                print(" HOST Pc is not available")
                # wake on lan
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(b'\xff' * 6 + opParams.macAdress * 16,  #Host Pc MAC adress
                         (opParams.hostIP, 80)) # Host Pc IP
                # Wake on lan Working


# turnOnWithLan.runOp()






