import socket
import queue
import threading
# import
import time

from settings import PORT, WIKI_LINKS_FILE, NUM_CLIENT_THREAD


SOCKET_ADDR = ("localhost", PORT)


def fill_queue(que):
    que.put('start')
    for val in ['one', 'two', 'three', 'stop']:
        que.put(val)


def fetch_socket(url: str):
    sock = socket.socket()
    sock.connect(SOCKET_ADDR)
    sock.send(url.encode())
    response = sock.recv(1024)
    return response.decode()


def fetch_socket_thread_loop(que: queue.Queue):
    while not que.empty():
        try:
            url = que.get(timeout=0.3)
        except queue.Empty:
            print('-- Queue is empty')
            continue
        time.sleep(0.1)
        try:
            fetch_result = fetch_socket(url)
        except ConnectionRefusedError:
            print(f'Connection refused to {SOCKET_ADDR}')
            break
        except Exception as e:
            print(f'! Exception in socket request = {url}')
            print(type(e).__name__)
            continue
        print(f'{threading.current_thread().name} | {url} | {fetch_result}')


if __name__ == '__main__':
    queue_links = queue.Queue()

    fill_queue(queue_links)

    threads = [
        threading.Thread(
            target=fetch_socket_thread_loop,
            args=(queue_links,),
            name=f'client_socket_{num}') for num in range(NUM_CLIENT_THREAD)]

    print('-- Start thread')
    for th in threads:
        th.start()

    for th in threads:
        th.join()

    print('-- Stopped threads')
