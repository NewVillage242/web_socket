
import socket
import threading

HEADER = 64
PORT = 9999
# SERVER = ""
# Another way to get the local IP address automatically
SERVER = "0.0.0.0"
print(SERVER)
print(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr, count):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while dic[count]:
        msg = conn.recv(1024).decode(FORMAT)
        print(msg)
        if "bye" in msg:
            dic[count] = False

    conn.close()


def handle_write(conn, addr, count):
    #conn.send(bytes(count, FORMAT))
    while dic[count]:
        msg = input("Server > ")
        conn.send(bytes(msg, FORMAT))
    conn.cloes()
dic = {}
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    count = 0
    while True:
        conn, addr = server.accept()
        count += 1
        dic[count] = True
        thread_read = threading.Thread(target=handle_client, args=(conn, addr, count))
        thread_write= threading.Thread(target=handle_write, args=(conn,addr, count))
        thread_read.start()
        thread_write.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()