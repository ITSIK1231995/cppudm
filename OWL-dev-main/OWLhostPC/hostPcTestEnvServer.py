import socket
from operations.allOperations import allOperations
from operations.operationsTypes.runCommandViaCmd import runCommandViaCMD
import json

import sys
import logging
import traceback
import os


class hostPcTestEnvServer():




    @staticmethod
    def bindServer():
        # get the hostname
        host = "127.0.0.1"
        port = 5000  # initiate port no above 1024

        server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together
        # configure how many client the server can listen simultaneously
        server_socket.listen(1)

        return server_socket
    @staticmethod
    def server(server_socket):
        logging.info("server started, waiting for connections")
        print("server started, waiting for connections")
        #print("server started, waiting for connections")


        while True:

            scoket, address = server_socket.accept()  # accept new connection
            # print("Connection from: " + str(address))
            logging.info("Connection from: " + str(address))
            print("Connection from: " + str(address))

            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = scoket.recv(1024)
            logging.info("data received")
            print("data received")
            if data and data.decode('utf-8') != "Test":
                data = json.loads(data.decode('utf-8'))
                # if isinstance(data, dict):
                mappedOperations = allOperations()
                if 'param' in data.keys():
                    logging.info("executing operation = " + data['operation']+", param = " + data['param'])
                    print("executing operation = " + data['operation']+", param = " + data['param'])
                    mappedOperations.operationsImplement[data['operation']].runOp(scoket,data['param'])
                else:
                    logging.info("executing operation = " + data['operation'])
                    print("executing operation = " + data['operation'])
                    mappedOperations.operationsImplement[data['operation']].runOp(scoket,[])


                # elif isinstance(data, str):
                #     mappedOperations = allOperations()
                #     mappedOperations.operationsImplement[data].runOp()


            #print("from connected user: " + str(data))
            #data = input(' -> ')
            # conn.send(data.encode())  # send data to the client

        #conn.close()  # close the connection






if __name__ == '__main__':
    #hostPcTestEnvServer.server(hostPcTestEnvServer.bindServer())

    if not os.path.exists("C:\\owlLog"):
        os.makedirs("C:\\owlLog")

    logging.basicConfig(filename='C:\\owlLog\\appLog.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        hostPcTestEnvServer.server(hostPcTestEnvServer.bindServer())
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logging.exception("exception on main")
        logging.shutdown()





