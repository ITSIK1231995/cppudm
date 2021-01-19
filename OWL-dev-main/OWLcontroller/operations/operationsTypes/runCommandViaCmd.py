from operations.operation import operation
import json


class runCommandViaCmd(object):
    def getKey(self):
        ''' Returns operation's name '''
        return (type(self).__name__)

    # @staticmethod
    # def runOp(client_socket, cmdCommand = 'ipconfig'):
    #
    #     # trying here to send a json
    #     # data = {}
    #     # data['runCommandViaCmd'] = cmdCommand
    #     # json_data = json.dumps(data)
    #
    #     # sending just the cmd command
    #     message = cmdCommand
    #     client_socket.send(message.encode())  # send message
    #     data = client_socket.recv(1024).decode()  # receive response from the server
    #
    #     return ('Received from server: ' + data)  # show the response in terminal

    @staticmethod
    def runOp(client_socket, cmdCommand='ipconfig'):

        df1 = {"operation": "runCommandViaCmd", "param": cmdCommand}
        client_socket.sendall(json.dumps(df1).encode('utf-8'))  # encode the dict to JSON
        data = client_socket.recv(1024).decode()  # receive response from the server

        return ('Received from server: ' + data)  # show the response in terminal

        #message = input(" -> ")  # again send a messege to the server

