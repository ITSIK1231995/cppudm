from operations.operation import operation
import json
PING = 'ping '
SLEEP_COMMAND ="sleep command request from client"
#SLEEP_COMMAND = 'rundll32.exe powrprof.dll,SetSuspendState 0,1,0'

class sleep(operation):
    def getKey(self):
        pass

    @staticmethod
    def runOp(client_socket, host='empty'):

        messegeToServer = {"operation": "sleep", "param": SLEEP_COMMAND}
        client_socket.sendall(json.dumps(messegeToServer).encode('utf-8'))  # encode the dict to JSON
        messegeFromServer = client_socket.recv(1024).decode()  # receive response from the server

        # sending a ping in order to verify the shutdown
        # pingCommand = PING + host
        # if (os.system(pingCommand)) == 0:
        #     print ("alive")

        return ('Received from server: ' + messegeFromServer)  # show the response in terminal