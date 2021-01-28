# import uuid
# uuid.getnode()
#
# print (hex(uuid.getnode()))
#
# address = 1234567890
# h = iter(hex(address)[2:].zfill(12))
# print(":".join(i + next(h) for i in h))
# import subprocess, re
#
# ipconfig_all = subprocess.check_output('ipconfig /all').decode()
# mac_addr_pattern = re.compile(r'(?:[0-9a-fA-F]-?){12}')
# mac_addr_list = re.findall(mac_addr_pattern, ipconfig_all)
#
# print(mac_addr_list)

from getmac import get_mac_address

