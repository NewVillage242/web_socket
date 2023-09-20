
import socket
import threading

SERVER, PORT= "0.0.0.0", 9999
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_read(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while True:
        msg = conn.recv(1024).decode(FORMAT)
        print(msg)
        if "bye" in msg:
            break
    conn.close()

# server -> client
# [#num] string_to_send
def handle_write():
    while True:
        msg = input("Server > ")
        num, *_ = msg.split(" ")
        num = int(num)
        if num is 0:
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
    while True:
        conn, addr = server.accept()
        count += 1
        dic[count] = conn
        thread_read = threading.Thread(target=handle_read, args=(conn, addr))
        thread_read.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()