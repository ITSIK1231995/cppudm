import socket
from operations.allOperations import allOperations
import json
import sys
import logging
import traceback
import os

class hostPcTestEnvServer():
    def __init__(self):
        self.bindServer()
        self.server()

    def bindServer(self):
        # get the hostname
        host = socket.gethostname()
        port = 5000  # initiate port no above 1024
        self.server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        self.server_socket.bind((host, port))  # bind host address and port together
        # configure how many client the server can listen simultaneously
        self.server_socket.listen(1)

    def reliseServerScoket(self):
        logging.info("server_socket closed")
        self.server_socket.close()

    def server(self):
        logging.info("server started, waiting for connections")
        print("server started, waiting for connections")
        while True:
            scoket, address = self.server_socket.accept()  # accept new connection
            # print("Connection from: " + str(address))
            logging.info("Connection from: " + str(address))
            print("Connection from: " + str(address))
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = scoket.recv(1024)
            logging.info("data received")
            print("data received")
            if data and data.decode('utf-8') != "Test":
                data = json.loads(data.decode('utf-8'))
                mappedOperations = allOperations()
                if 'param' in data.keys():
                    logging.info("executing operation = " + data['operation']+", param = " + data['param'])
                    print("executing operation = " + data['operation']+", param = " + data['param'])
                    mappedOperations.operationsImplement[data['operation']].runOp(self,scoket,data['param'])
                else:
                    logging.info("executing operation = " + data['operation'])
                    print("executing operation = " + data['operation'])
                    mappedOperations.operationsImplement[data['operation']].runOp(self,scoket,[])

if __name__ == '__main__':
    if not os.path.exists("C:\\owlLog"):
        os.makedirs("C:\\owlLog")
    logging.basicConfig(filename='C:\\owlLog\\appLog.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        hostPcServer = hostPcTestEnvServer()
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logging.exception("exception on main")
        logging.exception("server shouting down")
        logging.shutdown()
        sys.exit()






