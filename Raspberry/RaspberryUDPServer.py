import socket
import time
from functools import partial


class Server:
    def __init__(self):

        UDP_IP = "192.168.4.1"
        UDP_PORT = 1234

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self.sock.bind((UDP_IP, UDP_PORT))
        
    def Receive(self):
        data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
        return data, addr


def convertTuple(tup):
    st = ''.join(map(str, tup))
    return int(st[10:12])
    

def höhenruder(x, y, z):
    #print(str(time.time()) + " höhenruder" + str(x)+ str(y)+ str(z))
    return

def querruder(x, y, z):
    #print("querruder" + str(x)+ str(y)+ str(z))
    return

def seitenruder(x, y, z):
    return

def default():
    return

switcher = {
    10: höhenruder,
    11: querruder,
    12: seitenruder
} 

def loop():
    server = Server()
    count = 0
    oldTime = time.time()
    arr = [] 
    while True:
        data, addr = server.Receive()
        values = data.decode('UTF-8').split(" ")
        switcher[convertTuple(addr)](str(values[0]), str(values[1]), str(values[2]))
        arr.append(data)
        if time.time() >= oldTime + 1:
            print(str(len(arr)) + " messages/s")
            oldTime = time.time()
            arr.clear()

def main():
    loop()


if __name__ == "__main__":
    main()
