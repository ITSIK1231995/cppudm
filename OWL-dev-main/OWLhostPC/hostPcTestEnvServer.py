import socket
from operations.allOperations import allOperations
from operations.operationsTypes.runCommandViaCmd import runCommandViaCMD
import json


class hostPcTestEnvServer():




    @staticmethod
    def bindServer():
        # get the hostname
        host = socket.gethostname()
        port = 5000  # initiate port no above 1024

        server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together
        # configure how many client the server can listen simultaneously
        server_socket.listen(1)

        return server_socket
    @staticmethod
    def server(server_socket):
        while True:
            conn, address = server_socket.accept()  # accept new connection
            print("Connection from: " + str(address))

            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024)
            if data and data.decode('utf-8') != "Test":

                data = json.loads(data.decode('utf-8'))
                if isinstance(data, dict):
                    mappedOperations = allOperations()
                    mappedOperations.operationsImplement[data['operation']].runOp(data['param'],conn)

                elif isinstance(data, str):
                    mappedOperations = allOperations()
                    mappedOperations.operationsImplement[data].runOp()


            #print("from connected user: " + str(data))
            #data = input(' -> ')
            # conn.send(data.encode())  # send data to the client

        #conn.close()  # close the connection






if __name__ == '__main__':
    while True:
        try:
            hostPcTestEnvServer.server(hostPcTestEnvServer.bindServer())
        except Exception as e:
            print(e)
            continue




