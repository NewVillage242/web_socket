
import socket
import threading
import sys
import signal
import time
SERVER, PORT= "0.0.0.0", 9999
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'

class Event:
    def __init__(self):
        self.status = False
exit_event = Event()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def sigint_handler(signal,frame):
    print("End")
    exit_event.status = True
    sys.exit(0)

def handle_read(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    counter = 0
    while not exit_event.status:
        msg = conn.recv(1024).decode(FORMAT) 
        if counter >= 10:
            break
        if len(msg) == 0:
            counter += 1
            continue
        print(msg)
        import os
        os.system(f"echo {msg} >> tmp.txt")
        counter = 0
        if "bye" in msg:
            break
    print("hanld_read done.")
    conn.close()

# server -> client
# [#num] string_to_send
def handle_write():
    while not exit_event.status:
        msg = input("Server > ")
        num, *_ = msg.split(" ")
        num = int(num)
        if num == 0:
            break
        msg = " ".join(_)
        dic[num].send(bytes(msg, FORMAT))
    server.close()
    print("Server close")
    
dic = {}
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    count = 0
    thread_write = threading.Thread(target=handle_write)
    thread_write.start()
    while not exit_event:
        conn, addr = server.accept()
        count += 1
        dic[count] = conn
        thread_read = threading.Thread(target=handle_read, args=(conn, addr))
        thread_read.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

signal.signal(signal.SIGINT, sigint_handler)
print("[STARTING] server is starting...")
start()