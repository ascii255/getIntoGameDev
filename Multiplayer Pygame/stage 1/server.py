import socket
import _thread

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

def client_thread(connection):
    connection.send(str.encode("Welcome to the server!"))
    messageFromClient = ""
    while True:
        try:
            #recieve up to 2048 bytes of data from client
            messageFromClient = str(connection.recv(2048))[2:-1]

            if messageFromClient=="quit":
                print("Disconnected")
                break
            else:
                messageToClient = str.upper(messageFromClient)
                connection.sendall(str.encode(messageToClient))
                messageFromClient = ""
        except:
            break
    print("close connection")
    connection.close()

s = open_connection()

#start listening on socket
s.listen()
while True:
    connection, address = s.accept()
    print(f"Connected to {address}")
    _thread.start_new_thread(client_thread, (connection,))