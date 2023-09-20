import socket
import sys
import threading

HOST, PORT = "0.0.0.0", 9999
data = " ".join(sys.argv[1:])

def handle_ui(sock):
    while True:
        received = str(sock.recv(1024), "utf-8")
        print(received)
# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    #sock.sendall(bytes(data + "\n", "utf-8"))
    #name = str(sock.recv(1024), "utf-8")
    name = "1"
    thread = threading.Thread(target=handle_ui, args=(sock,))
    thread.start()
    while True:
        # Receive data from the server and shut down
        data = input(">")
        sock.sendall(bytes(name+" "+data, "utf-8"))
        print(f"Client {name}")
        print("Sent:     {}".format(data))
        if "bye" in data:
            break
    socket.close()
