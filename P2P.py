import socket as sk
from threading import Thread

ip = "0.0.0.0"
port = 4444 # listening port, change

target = "192.168.1.10" # target ip, change
target_port = 4444 # target port, change

server = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

def recv():
    server = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

    server.bind((ip, port))

    while True:
        data, addr = server.recvfrom(1024)
        print(f"received: {data.decode()}")

def send():
    while True:
        data = input()
        server.sendto(data.encode(), (target, target_port))
        print("you: {data}")

r = Thread(target=recv, daemon=True)
s = Thread(target=send, daemon=True)

r.start()
s.start()
r.join()
s.join()

server.close()
