import socket
import argparse
import time
import hashlib

GET_TIME=b"1"
MINE_BITCOIN=b"2"

def main():
    parser = argparse.ArgumentParser(description="A worker")
    parser.add_argument('--lb', help='load balancer ip:port', required=True)
    args = parser.parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    sock.connect((args.lb.split(":")[0], int(args.lb.split(":")[1])))
    # sock.sendall(b"The Worker Is Running!")
    
    print("Connected")

    working_loop(sock)

    print("The socket is closing!")

def working_loop(sock):
    while True:
        num=sock.recv(1)
        if len(num) == 0:
            break
        
        secs=time.time()# in str

        to_send=b""
        if num==GET_TIME:
            to_send = time.ctime(secs).encode("utf-8")
        elif num==MINE_BITCOIN:
            h = str(secs).encode("utf-8")
            for i in range(255):
                m = hashlib.sha256()
                m.update(h)
                h = m.digest()
            
            m = hashlib.sha256()
            m.update(h)
            to_send=m.hexdigest().encode("utf-8")

        sock.send(to_send)

main()