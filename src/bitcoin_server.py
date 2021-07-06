import threading
import socketserver
from pathlib import Path

worker_list = []
worker_list_lock = threading.Condition()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


class ClientQueue():
    def __init__(self, client):
        self.client = client
        self.queue = []
        self.next_needed_index = 0
        self.queue_lock = threading.Lock()

    def append_to_queue(self, index, value):
        self.queue_lock.acquire()

        self.queue.append((index, value))
        self.queue.sort(key=lambda x: x[0])
        self._clean_queue()

        self.queue_lock.release()

    def _clean_queue(self):
        while len(self.queue) > 0 and self.queue[0][0] == self.next_needed_index:
            # remove this
            self.client.sendall(self.queue[0][1] + b"\n")
            self.queue = self.queue[1:]
            self.next_needed_index += 1

def send_command_to_worker(command, index, ret_to_client):
    available_worker = None

    worker_list_lock.acquire()
    while available_worker == None:
        for worker in worker_list:
            if worker["next_command"] == None:
                # found available worker!
                available_worker = worker
                break

        if available_worker != None:
            break

        # someone notify me when a worker is available
        worker_list_lock.wait()

    available_worker["notify"].acquire()
    available_worker["notify"].notify()

    available_worker["next_command"] = command
    available_worker["index"] = index
    available_worker["ret_to_client"] = ret_to_client

    available_worker["notify"].release()
    worker_list_lock.release()

class ClientHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print(f"Connected: {self.client_address} on {threading.currentThread().getName()}")
        my_queue = ClientQueue(self.request)
        index = 0
        while True:
            data = self.request.recv(1024)
            for char in data:
                if char == 49:
                    # get time
                    send_command_to_worker(b"1", index, my_queue)
                    index += 1
                elif char == 50:
                    # mine bitcoin
                    send_command_to_worker(b"2", index, my_queue)
                    index += 1
            if len(data) == 0:
                break
        print(f"Closed: {self.client_address} on {threading.currentThread().getName()}")

class WorkerHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print(f"Worker Connected: {self.client_address} on {threading.currentThread().getName()}")
        me = {
            "addr": self.client_address,
            "next_command": None,
            "notify": threading.Condition()
        }
        me["notify"].acquire()

        worker_list_lock.acquire()  # HERE
        worker_list_lock.notify()   # if someone's blocking to get a worker
        worker_list.append(me)
        worker_list_lock.release()  # HERE

        try:
            while True:
                # wait for someone to send me a command
                me["notify"].wait()
                if me["next_command"] == None:
                    continue

                self.request.send(me["next_command"])
                ret_value = self.request.recv(1024)
                me["ret_to_client"].append_to_queue(me["index"], ret_value)  # return to the actual client

                worker_list_lock.acquire()
                worker_list_lock.notify()  # if someone's blocking to get a worker
                me["next_command"] = None
                worker_list_lock.release()
        finally:
            worker_list_lock.acquire()
            worker_list_lock.notify()  # if someone's blocking to get a worker
            worker_list.remove(me)
            worker_list_lock.release()
            print(f"Worker Closed: {self.client_address} on {threading.currentThread().getName()}")


def client_thread():
    with ThreadedTCPServer(('', 13337), ClientHandler) as server:
        print("Server is running!")
        server.serve_forever()

# start the client thread
threading.Thread(target=client_thread, daemon=True).start()

with ThreadedTCPServer(('', 13338), WorkerHandler) as server:
    print("Worker server is running!")
    server.serve_forever()
