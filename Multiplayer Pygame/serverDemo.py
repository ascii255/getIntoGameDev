import socket
import _thread

def open_connection(ip="",port=0):
    #create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #AF_INET: ipv4
    #SOCK_STREAM: tcp
    s.bind((ip,port))
    connectedIP = s.getsockname()[0]
    connectedPort = s.getsockname()[1]
    print(f"Server connected on ip: {connectedIP}, port:{connectedPort}")
    return s

def client_thread(connection):
    connection.send(str.encode("Welcome to the server!"))
    reply = ""
    while True:
        try:
            #recieve up to 2048 bytes of data from client
            reply = str.decode(connection.recv(2048))

            if len(reply)==0:
                print("Disconnected")
                break
            else:
                reply = str.upper(reply)
                connection.sendall(str.encode(reply))
                reply = ""
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