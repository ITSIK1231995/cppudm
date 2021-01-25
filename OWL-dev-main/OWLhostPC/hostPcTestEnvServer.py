import socket
from operations.allOperations import allOperations
from operations.operationsTypes.runCommandViaCmd import runCommandViaCMD
import json


class hostPcTestEnvServer():

    @staticmethod
    def server():
        while True:
            # get the hostname
            host = socket.gethostname()
            port = 5000  # initiate port no above 1024

            server_socket = socket.socket()  # get instance
            # look closely. The bind() function takes tuple as argument
            server_socket.bind((host, port))  # bind host address and port together

            # configure how many client the server can listen simultaneously
            server_socket.listen(2)
            conn, address = server_socket.accept()  # accept new connection
            print("Connection from: " + str(address))

            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024)
            if not data:
                # if data is not received break
                break

            data = json.loads(data.decode('utf-8'))
            if isinstance(data, dict):
                mappedOperations = allOperations()
                data = mappedOperations.operationsImplement[data['operation']].runOp(data['param'])

            elif isinstance(data, str):
                        mappedOperations = allOperations()
                        data = mappedOperations.operationsImplement[data].runOp()

                #data = runCommandViaCMD().runOp(data['param'])
            #     #Temp check:
            # if data == 'ipconfig':
            #     data = runCommandViaCMD().runOp(data)
            #
            #     #Temp check end

            print("from connected user: " + str(data))
            #data = input(' -> ')
            conn.send(data.encode())  # send data to the client

        conn.close()  # close the connection






if __name__ == '__main__':
    while True:
        hostPcTestEnvServer.server()





