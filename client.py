import socket
import sys
import threading
import signal 

HOST, PORT = "0.0.0.0", 9999
data = " ".join(sys.argv[1:])
def sigint_handler(signal, frame):
    print("End")
    # _sock.sendall(bytes("bye", "utf-8"))
    _sock.close()
    sys.exit(0)
def handle_ui():
    try:
        while True:
            received = str(_sock.recv(1024), "utf-8")
            print(received)
    except OSError:
        pass
    finally:
        pass
# Create a socket (SOCK_STREAM means a TCP socket)
_sock = None
signal.signal(signal.SIGINT, sigint_handler)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    #sock.sendall(bytes(data + "\n", "utf-8"))
    #name = str(sock.recv(1024), "utf-8")
    name = "1"
    _sock = sock
    thread = threading.Thread(target=handle_ui)
    thread.start()
    while True:
        # Receive data from the server and shut down
        data = input(">")
        _sock.sendall(bytes(name+" "+data, "utf-8"))
        print(f"Client {name}")
        print("Sent:     {}".format(data))
        if "bye" in data:
            break
    sock.close()
