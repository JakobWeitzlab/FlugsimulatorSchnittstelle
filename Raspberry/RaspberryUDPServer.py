import socket
import time
import math
# from functools import partial
from smbus2 import SMBus


class Server:
    def __init__(self):

        UDP_IP = "192.168.4.1"
        UDP_PORT = 1234

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self.sock.bind((UDP_IP, UDP_PORT))
        
    def Receive(self):
        data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
        return data, addr

    def convertTuple(self, tup):
        st = ''.join(map(str, tup))
        return int(st[10:12])
        
    def _distance(self, value1, valueZ):
        distance = math.sqrt(math.pow(value1, 2) + math.pow(valueZ, 2))
        return distance

    def höhenruder(self, x, y, z):
        foo = math.atan2(y, self._distance(x, z))
        # print(str(time.time()) + " höhenruder" + str(x)+ str(y)+ str(z))
        self.yaw = math.degrees(foo)
        return 

    def querruder(self, x, y, z):
        foo = math.atan2(y, self._distance(x, z))
        # print(str(time.time()) + " höhenruder" + str(x)+ str(y)+ str(z))
        self.roll = math.degrees(foo)
        return

    def seitenruder(self, x, y, z):
        return

    def Select(self):
        switcher = {
            10: self.höhenruder,
            11: self.querruder,
            12: self.seitenruder
        } 

        switcher[self.convertTuple(self.addr)](self.ConvertReading(0),self.ConvertReading(1), self.ConvertReading(2))# (int(self.values[0]), int(self.values[1]), int(self.values[2]))

    def ProMicro(self):
        # yaw = self.yaw * 2.84
        with SMBus(1) as bus:
            # print(time.time())
            bus.write_byte_data(0x03,0, int(self.yaw))
            # bus.write_byte_data(0x03,1, self.roll)
            # bus.write_byte_data(0x03,2, self.roll)
        return

    def ConvertReading(self, i):
        # for i in range(0,2):
        # Positiv or negative number?
        if (int(self.values[i]) >= 0x8000):
            self.values[i] = -((65535 - int(self.values[i])) + 1)
            return int(self.values[i])
        else:
            return int(self.values[i])
        # return self.values

    def loop(self):
        # count = 0
        # oldTime = time.time()
        # arr = [] 
        while True:
            self.data, self.addr = self.Receive()
            self.values = self.data.decode('UTF-8').split(" ")
            # self.ConvertReading()
            self.Select()
            # print(time.time())
            self.ProMicro()

            # switcher[self.convertTuple(addr)](str(values[0]), str(values[1]), str(values[2]))
            '''arr.append(data)
            if time.time() >= oldTime + 1:
                print(str(len(arr)) + " messages/s")
                oldTime = time.time()
                arr.clear()'''

def main():
    server = Server()
    server.loop()


if __name__ == "__main__":
    main()
