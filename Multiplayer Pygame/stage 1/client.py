import socket

def connect_to_server():
    ip = "192.168.0.104"
    port = int(input("Server port number: "))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip,port))

    return s

s = connect_to_server()

while True:
    messageFromServer = str(s.recv(2048))[2:-1]
    print(messageFromServer)
    messageToServer = input()
    s.sendall(str.encode(messageToServer))
    if messageToServer == "quit":
        break