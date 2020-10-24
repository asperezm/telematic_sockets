import socket
import threading
import os
import constant
import shutil


HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        comm = msg_length.split()
        command = comm[0]

        print(command)
        print(f'Received from { addr }')

        if command == constant.LIST_ALL:
            strfiles = ""
            for x in os.listdir(constant.PATH):
                strfiles += x+"\n"
            conn.send(bytes('[500] LIST OBTAINED', FORMAT))
            conn.send(strfiles[:-1].encode(FORMAT))

        elif command == constant.CREATE_BUCKET:
            new_bucket = constant.PATH + f'/{ comm[1] }'
            try:
                os.mkdir(new_bucket)
            except OSError:
                conn.send(bytes('[307] BUCKET ALREADY EXISTS', FORMAT))
            else:
                conn.send(bytes('[100] BUCKET CREATED', FORMAT))

        elif command == constant.DELETE_BUCKET:
            bucket = constant.PATH + f'/{ comm[1] }'
            try:
                os.rmdir(bucket)
            except OSError:
                conn.send(bytes('[304] BUCKET NOT FOUND', FORMAT))
            else:
                conn.send(bytes('[200] BUCKET DELETED', FORMAT))

        elif command == constant.LIST_BUCKETS:
            bucket1 = os.listdir(constant.PATH)
            bucketname = ""
            for buck in bucket1:
                if os.path.isdir(os.path.join(buck)):
                    bucketname += buck+"\n"
            conn.send(bytes('[500] LIST OBTAINED', FORMAT))
            conn.send(bucketname[:-1].encode(FORMAT))

        elif command == constant.LIST_FILES:
            files = os.listdir(constant.PATH)
            filesname = ""
            for file in files:
                if os.path.isfile(os.path.join(file)):
                    filesname += file+"\n"
            conn.send(bytes('[500] LIST OBTAINED', FORMAT))
            conn.send(filesname[:-1].encode(FORMAT))
        
        elif command == constant.UPLOAD_FILE:
            filename = comm[1]
            try:
               shutil.copy(filename,constant.PATH)
               conn.send("[400] FILE UPLOADED".encode(FORMAT))
            except:
                conn.send("[401] FAILED TO UPLOAD".encode(FORMAT))
                
        elif command == constant.DOWNLOAD_FILE:
            pass
        elif command == constant.DELETE_FILE:
            pass
        elif command == constant.DISCONNECT_COMMAND:
            print(f'[CLIENT DISCONNECTED] { addr } disconnected')
            conn.send(bytes('[600] DISCONNECTED', FORMAT))
            connected = False
        else:
            conn.send(bytes('[300] UNKNOWN COMMAND', FORMAT))

    conn.close()


def start():
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    server.listen(10)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print(f"[STARTING] server is starting...")
start()
