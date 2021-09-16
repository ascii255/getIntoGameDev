import socket
import _thread

class clientNode:
    def __init__(self, connection):
        self.connection = connection
        self.next = None

def open_connection(ip="",port=0):
    #create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #AF_INET: ipv4
    #SOCK_STREAM: tcp
    ip = "192.168.0.104"
    s.bind((ip,port))
    connectedIP = s.getsockname()[0]
    connectedPort = s.getsockname()[1]
    print(f"Server connected on ip: {connectedIP}, port:{connectedPort}")
    return s

def client_thread(client,firstClient):
    client.connection.send(str.encode("Welcome to the server!"))
    messageFromClient = ""
    while True:
        try:
            #recieve up to 2048 bytes of data from client
            messageFromClient = str(client.connection.recv(2048))[2:-1]

            if messageFromClient=="quit":
                print("Disconnected")
                break
            else:
                print(f"Client says \"{messageFromClient}\"")
                messageToClient = str.upper(messageFromClient)
                #send to all clients
                thisClient = firstClient
                while thisClient is not None:
                    thisClient.connection.sendall(str.encode(messageToClient))
                    thisClient = thisClient.next
                messageFromClient = ""
        except:
            break
    print("close connection")
    connection.close()

s = open_connection()
firstClient = None
#start listening on socket
s.listen()
while True:
    connection, address = s.accept()
    print(f"Connected to {address}")
    newClient = clientNode(connection)
    if firstClient is None:
        firstClient = newClient
    else:
        thisNode = firstClient
        while thisNode.next is not None:
            thisNode = thisNode.next
        thisNode.next = newClient
    _thread.start_new_thread(client_thread, (newClient,firstClient))