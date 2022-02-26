# ======import librarys======#
import sys
import socket
import time
import math
import threading
# from functools import partial

# ======import external librarys====== #
from smbus2 import SMBus
import schedule
import numpy
from PyQt5.QtCore import *

mutex = QMutex()

class Server(QRunnable):
    def __init__(self):
        super(Server, self).__init__()
        self.signals = ServerSignals()
        self._running = True
        # self._handshakeSuccess = False
        
        UDP_IP = "192.168.4.1"
        UDP_PORT = 1234

        self.posNegHoehen = 0
        self.posNegQuer = 0
        self.posNegSeit = 0

        self.WinkelHoehen = 0
        self.WinkelQuer = 0
        self.WinkelSeit = 0

        self.stautsHoehen = False
        self.stautsSeiten = False
        self.stautsQuer = False

        self.offseteSeiten = 0
        self.offsetHoehen = 0
        self.offsetQuer = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self.sock.bind((UDP_IP, UDP_PORT))
        
        self.messageCountHoehen = 0
        self.messageCountSeiten = 0
        self.messageCountQuer = 0

        self.handshakeCount = 0

        self.HandleSchedule()
        # self.Handshake()
        # self.SensorCalibration()
        # self.ClientStatus()
        # self.ClientHandshake()
        
    def HandleSchedule(self):
        # ======Handle schedule====== #
        schedule.every(2).seconds.do(self.CountInputPackage)  # Count input packages
        # schedule.every(1.1).seconds.do(self.ClearInputPackage)
        schedule.every(10).seconds.do(self.ClientStatus)  # Handle Client Status

    def SensorCalibration(self):
        oldTime = time.time()
        arrHoehen = []
        arrSeiten = []
        arrQuer = []

        self.offseteSeiten = 0
        self.offsetHoehen = 0
        self.offsetQuer = 0

        while oldTime > time.time() - 5:
            data, self.addr = self.Receive()
            self.values = data.decode('UTF-8').split(" ")
            self.Select()
            arrHoehen.append(self.WinkelHoehen)
            arrSeiten.append(self.WinkelSeit)
            arrQuer.append(self.WinkelQuer)

        self.offsetHoehen = numpy.mean(arrHoehen)
        self.offseteSeiten = numpy.mean(arrSeiten)
        self.offsetQuer = numpy.mean(arrQuer)
        print("Kalibrierung erfolgreich")
        print(str(self.offseteSeiten) + " " + str(90-self.offsetHoehen) + " " + str(self.offsetQuer))

    def ClientStatus(self):
        if self.messageCountHoehen > 0:
            self.statusHoehen = True
        else:
            self.statusHoehen = False

        if self.messageCountSeiten > 0:
            self.stautsSeiten = True
        else:
            self.stautsSeiten = False

        if self.messageCountQuer > 0:
            self.stautsQuer = True
        else:
            self.stautsQuer = False

    def Handshake(self):
        while self.JoystickHandshake() != True:
            time.sleep(1)
            print("Trying to Handshake with Joystick")
        self.handshakeCount += 1

        '''while self.ClientHandshake() != True:
            time.sleep(1)
            print("Trying to Handshake with Clients")
        self.handshakeCount += 1'''

        if self.handshakeCount == 1:
            self._running = True

    def ClientHandshake(self):
        arr = ["192.168.4.10", "192.168.4.11", "192.168.4.12"]
        self.sock.listen(1)
        client = self.sock.accept()
        print(client)

    def JoystickHandshake(self):
        foo = ""
        while foo != "03":
            for addr in self.ScanForI2C(force=True):
                foo = '{:02X}'.format(addr)
        return True

        # if self._running == True:
        #    self.loop() # Execute main loop after successful handshake

    def ScanForI2C(self, force=False):
        devices = []
        for addr in range(0x03, 0x77 + 1):
            read = SMBus.read_byte, (addr,), {'force':force}
            write = SMBus.write_byte, (addr, 0), {'force':force}

            for func, args, kwargs in (read, write):
                try:
                    with SMBus(1) as bus:
                        data = func(bus, *args, **kwargs)
                        devices.append(addr)
                        break
                except OSError as expt:
                    if expt.errno == 16:
                        # just busy, maybe permanent by a kernel driver or just temporary by some user code
                        pass

        return devices

    def Receive(self):
        data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
        return data, addr

    def ConvertTuple(self, tup):
        st = ''.join(map(str, tup))
        return int(st[10:12])
        
    def Distance(self, value1, valueZ):
        distance = math.sqrt(math.pow(value1, 2) + math.pow(valueZ, 2))
        return distance

    def Höhenruder(self, x, y, z):
        self.posNegHoehen = 0x5B
        foo = math.atan2(y, self.Distance(x, z))
        self.WinkelHoehen = math.degrees(foo) - self.offsetHoehen
        if (self.WinkelHoehen - self.offsetHoehen < 0):
            self.posNegHoehen = 0x5C
            self.WinkelHoehen = (90-(self.WinkelHoehen * -1)) + self.offsetHoehen
        self.messageCountHoehen += 1
        return 

    def Querruder(self, x, y, z):
        self.posNegQuer = 0x5D
        foo = math.atan2(y, self.Distance(x, z))
        self.WinkelQuer = math.degrees(foo) - self.offsetQuer
        if (self.WinkelQuer - self.offsetQuer< 0):
            self.posNegQuer = 0x5E
            self.WinkelQuer = 90-(self.WinkelQuer * -1) + self.offsetQuer
        self.messageCountQuer += 1
        return

    def Seitenruder(self, x, y, z):
        self.posNegSeit = 0x5F
        foo = math.atan2(y, self.Distance(x, z))
        self.WinkelSeit = math.degrees(foo) - self.offseteSeiten
        if (self.WinkelSeit - self.offseteSeiten < 0):
            self.posNegSeit = 0x60
            self.WinkelSeit = 90-(self.WinkelSeit * -1) + self.offseteSeiten
        self.messageCountSeiten += 1
        return

    def Select(self):
        switcher = {
            10: self.Höhenruder,
            11: self.Querruder,
            12: self.Seitenruder
        } 

        switcher[self.ConvertTuple(self.addr)](self.ConvertReading(0),self.ConvertReading(1), self.ConvertReading(2))

    def ProMicro(self):
        with SMBus(1) as bus:
            bus.write_byte_data(0x03, self.posNegHoehen, int(self.WinkelHoehen))
            bus.write_byte_data(0x03, self.posNegQuer, int(self.WinkelQuer))
            bus.write_byte_data(0x03, self.posNegSeit, int(self.WinkelSeit))
        return

    def ConvertReading(self, i):
        # Positiv or negative number?
        if (int(self.values[i]) >= 0x8000):
            self.values[i] = -((65535 - int(self.values[i])) + 1)
            return int(self.values[i])
        else:
            return int(self.values[i])
        
    def CountInputPackage(self):
        mutex.lock()
        print(str(self.messageCountHoehen) + " Hoehenruder messages/s")
        print(str(self.messageCountSeiten) + " Seitenruder messages/s")
        print(str(self.messageCountQuer) + " Querruder messages/s")
        self.signals.finished.emit()
        mutex.unlock()

        time.sleep(1)
        self.messageCountHoehen = 0
        self.messageCountSeiten = 0
        self.messageCountQuer = 0
        return
    
    @pyqtSlot()   
    def run(self):
        while self._running:
            try:
                # print("looping")
                schedule.run_pending()
                
                data, self.addr = self.Receive()
                self.values = data.decode('UTF-8').split(" ")
                self.Select()
                # self.ProMicro()
                # time.sleep(0.2)

            except KeyboardInterrupt:
                # quit
                sys.exit()
            except:
                pass
            # time.sleep(0.2)

class ServerSignals(QObject):
    finished = pyqtSignal()

def main():
    server = Server()
    # threading.Thread(target=server.loop())
    server.run()

if __name__ == "__main__":
    main()
