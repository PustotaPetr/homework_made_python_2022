import socket
from queue import Queue
import threading

PORT = 50033

connect_queue = Queue()

def echo_socket(conn: socket.socket):
    conn.recv(1000)
    conn.sendall(b'hello')

if __name__ == "__main__":

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", PORT))
        sock.listen(5)
        while True:
            conn, addr = sock.accept()
            print(f"{type(conn)} || {conn=} {addr=}")
            echo_socket(conn)

