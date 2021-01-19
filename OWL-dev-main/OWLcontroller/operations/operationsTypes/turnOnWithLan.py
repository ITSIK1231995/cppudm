# import os
# import time
# import socket
# import subprocess
#
# hostname = "10.100.102.29"
#
# while 1:
#     sp = subprocess.Popen(["ping.exe", hostname], stdout = subprocess.PIPE)
#
#     sp.wait() # Wait for ping.exe to terminate.
#
#     return_code = sp.returncode # Get the return code
#
#     if return_code != 0:
#         print (hostname, 'is down.')
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         #I'm not that familiar with this part.assuming yours is correct.
#         s.sendto(b'\xff'*6 + b'\x00\x21\x6A\xC7\x1A\x42'*16, ('10.100.102.29', 80))
#     else:
#         print (hostname, 'is up.')
#
#


import socket
import subprocess
import platform

HOST_NAME = '10.100.102.14'
MAC_ADRESS = b'\x10\x65\x30\x2B\xE5\x87'
def ping_ip(current_ip_address):
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
        ) == "windows" else 'c', current_ip_address), shell=True, universal_newlines=True)
        if 'unreachable' in output:
            return False
        else:
            return True
    except Exception:
        return False


if __name__ == '__main__':
    # pinging the host for checking if its on
    current_ip_address = [HOST_NAME]
    for each in current_ip_address:
        if ping_ip(each):
            print(f"{each} Host Pc is available")
        else:
            print(f"{each}  HOST Pc is not available")
            #  Working wake on lan!!!
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b'\xff' * 6 + MAC_ADRESS * 16,  #Host Pc MAC adress
                     (HOST_NAME, 80)) # Host Pc IP
            # Wake on lan Working


