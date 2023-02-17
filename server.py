import socket
import threading
import queue
import datetime

def run_server():
    PORT = 5051
    SERVER = ''
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    HEADER = 64

    messages = queue.Queue()
    message_log = []
    clients = []
    usernames = {}

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(ADDR)
    except:
        return()

    def receive(conn, addr):
        connected = True
        while connected:
            message_len = conn.recv(HEADER).decode(FORMAT)
            if message_len:
                message_len = int(message_len)
                message = conn.recv(message_len).decode(FORMAT)
        #print (message)
        #print(addr)
        #print(conn)
        #conn.send("[MESSAGE RECEIVED]".encode(FORMAT))
            #if message == '!LOGS':
                #print(message_log)
            try:
                messages.put((message, addr, conn))
                message_log.append({addr, message})
            except:
                print("failed")

    def broadcast():
        while True:
            while not messages.empty():
                message, addr, conn = messages.get()
                #print(message)
                if conn not in clients:
                    clients.append(conn)
                    usernames.update({conn: message})
                for client in clients:
                #print(client)
                    #print (addr)
                    try:
                        user = usernames[conn]
                        client.send(f"<{str(user)}> {message}".encode(FORMAT))
                    except:
                        clients.pop(client)
                    #print(message)

#def client():
    #exec(open("client.py").read())

    def start():
        server.listen()
        while True:
            conn, addr = server.accept()
            for message in message_log:
                conn.send(str(message).encode(FORMAT))
            conn.send('[CONNECTED]'.encode(FORMAT))
            conn.send('[! THE FIRST MESSAGE YOU SEND WILL BE YOUR USERNAME !]'.encode(FORMAT))
            thread = threading.Thread(target = receive, args = (conn, addr))
            thread.start()
            thread_brdcst = threading.Thread(target = broadcast)
            thread_brdcst.start()
            #thread_client = threading.Thread(target = client)
            #thread_client.start()
    start()