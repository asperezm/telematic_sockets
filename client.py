import socket
#import constant
import os

HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
    
def start():
    print("Connected to the server, 'HELP' to see the available commands")
    while True:
        command = input()
        comm = command.split()
        if command == "":
            print("Invalid command")
        elif command == "HELP":
            
            print('ALL, CBUCKET, DBUCKET, LBUCKET, LBUCKET, LFILE, UPFILE, DWFILE, DWFILE, DFILE, EXIT, CD, BK')
        elif command == "EXIT":
            client.send(bytes( command, FORMAT))
            break
        elif comm[0] == "DWFILE":
            client.send(bytes( command + " " + os.getcwd(), FORMAT))
        else:
            client.send(bytes( command, FORMAT))
        print(client.recv(HEADER).decode(FORMAT))
    print(client.recv(HEADER).decode(FORMAT))
            
start()
        
            
        
        