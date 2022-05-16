#!/bin/python3.7
# ======import librarys======#
import sys
import socket
import time
import math
from traceback import print_list
# import threading
# from functools import partial

# ======import external librarys====== #
import schedule
from smbus2 import SMBus
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

        self.offsetSeiten = 0
        self.offsetHoehen = 0
        self.offsetQuer = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self.sock.bind((UDP_IP, UDP_PORT))
        
        self.messageCountHoehen = 0
        self.messageCountSeiten = 0
        self.messageCountQuer = 0

        self.BatteryStatusHoehen = 0
        self.BatteryStatusSeiten = 0
        self.BatteryStatusQuer = 0

        self.handshakeCount = 0

        self.statusJoystick = False

        self.HandleSchedule()
        self.Handshake()
        
        # self.ClientStatus()
        # self.ClientHandshake()
        
    def HandleSchedule(self):
        # ======Handle schedule====== #
        schedule.every(2).seconds.do(self.CountInputPackage)  # Count input packages
        schedule.every(10).seconds.do(self.ClientStatus)  # Handle Client Status
        # schedule.every(2).seconds.do(self.ClientStatus)

    def SensorCalibration(self):
        print("attempt to calibrate")
        mutex.lock()
        oldTime = time.time()
        arrHoehen = []
        arrSeiten = []
        arrQuer = []

        self.offsetSeiten = 0
        self.offsetHoehen = 0
        self.offsetQuer = 0

        while oldTime > time.time() - 3:
            data, self.addr = self.Receive()
            self.values = data.decode('UTF-8').split(" ")
            self.Select()
            arrHoehen.append(self.WinkelHoehen)
            arrSeiten.append(self.WinkelSeit)
            arrQuer.append(self.WinkelQuer)
        # print(arrSeiten)
        self.offsetHoehen = numpy.mean(arrHoehen)
        self.offsetSeiten = numpy.mean(arrSeiten)
        self.offsetQuer = numpy.mean(arrQuer)
        # print(self.offsetSeiten)
        self.signals.finishedOffset.emit()
        time.sleep(0.01)
        mutex.unlock()
        print("Kalibrierung erfolgreich")
        # print(str(self.offsetSeiten) + " " + str(90-self.offsetHoehen) + " " + str(self.offsetQuer))

    def ClientStatus(self):
        mutex.lock()
        if self.messageCountHoehen > 0:
            self.statusHoehen = True
        else:
            self.statusHoehen = False

        if self.messageCountSeiten > 0:
            self.statusSeiten = True
        else:
            self.statusSeiten = False

        if self.messageCountQuer > 0:
            self.statusQuer = True
        else:
            self.statusQuer = False
        time.sleep(0.1)
        self.signals.statusClient.emit()
        mutex.unlock()

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
        self.signals.statusJoystick.emit()
        self.statusJoystick = True
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
        self.WinkelHoehen = math.degrees(foo)

        if (self.WinkelHoehen - self.offsetHoehen < 0):
            self.posNegHoehen = 0x5C
            self.WinkelHoehen = numpy.abs(self.WinkelHoehen - self.offsetHoehen)
        else:
            self.WinkelHoehen = numpy.abs(self.WinkelHoehen - self.offsetHoehen)
        self.messageCountHoehen += 1
        return  

    def Querruder(self, x, y, z):
        self.posNegQuer = 0x5D
        foo = math.atan2(y, self.Distance(x, z))
        self.WinkelQuer = math.degrees(foo)

        if (self.WinkelQuer - self.offsetQuer < 0):
            self.posNegQuer = 0x5E
            self.WinkelQuer = numpy.abs(self.WinkelQuer - self.offsetQuer)
        else:
            self.WinkelQuer = numpy.abs(self.WinkelQuer - self.offsetQuer)
        self.messageCountQuer += 1
        return

    def Seitenruder(self, x, y, z):
        self.posNegSeit = 0x5F
        foo = math.atan2(x, self.Distance(y, z))
        self.WinkelSeit = math.degrees(foo)

        if (self.WinkelSeit - self.offsetSeiten < 0):
            self.posNegSeit = 0x60
            self.WinkelSeit = numpy.abs(self.WinkelSeit - self.offsetSeiten)
        else:
            self.WinkelSeit = numpy.abs(self.WinkelSeit - self.offsetSeiten)
        self.messageCountSeiten += 1
        
        # print("Winkel " + str(math.degrees(foo)))
        # print("offset " + str(self.offsetSeiten))
        # print("richtiger Winkel " + str(self.WinkelSeit))
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
        # print(str(self.messageCountHoehen) + " Hoehenruder messages/s")
        # print(str(self.messageCountSeiten) + " Seitenruder messages/s")
        # print(str(self.messageCountQuer) + " Querruder messages/s")
        self.messageCountHoehen
        self.messageCountSeiten
        self.messageCountQuer
        self.signals.finishedMessageCount.emit()
        time.sleep(0.01)
        mutex.unlock()

        
        self.messageCountHoehen = 0
        self.messageCountSeiten = 0
        self.messageCountQuer = 0
        return

    def BatteryStatusConversion(self, v):
        # foo = (float(v) * 4095) / 3.3
        foo = float(v)
        print(foo)
        if foo > 2400:
            return "Batterie: 100"
        if foo > 2326:
            return "Batterie: >50"
        if foo > 2210:
            return "Batterie: 25"
        if foo < 2093:
            return "Batterie: <25"
    
    @pyqtSlot()   
    def run(self):
        # Battery
        arr = [10,11,12]
        print("receiving")
        while len(arr) != 0:
            data, self.addr = self.Receive()
            add = self.ConvertTuple(self.addr)
            self.values = data.decode('UTF-8').split(" ")
            
            if add == 10 and len(self.values) <= 2:
                self.BatteryStatusHoehen = self.BatteryStatusConversion(self.values[0])
                arr.pop(arr.index(10))
                self.signals.statusBattery.emit()
                print("received 10")
            if add == 11 and len(self.values) <= 2:
                # self.BatteryStatusSeiten = self.values[0]
                self.BatteryStatusQuer = self.BatteryStatusConversion(self.values[0])
                arr.pop(arr.index(11))
                self.signals.statusBattery.emit()
                print("received 11")
            if add == 12 and len(self.values) <= 2:
                self.BatteryStatusSeiten = self.BatteryStatusConversion(self.values[0])
                arr.pop(arr.index(12))
                self.signals.statusBattery.emit()
                print("received 12")
        self.SensorCalibration()
        
        # Main loop
        while self._running:
            try:
                # print("looping")
                schedule.run_pending()
                
                data, self.addr = self.Receive()
                self.values = data.decode('UTF-8').split(" ")
                self.Select()
                               
                self.ProMicro()
                # time.sleep(0.2)

            except KeyboardInterrupt:
                # quit
                sys.exit()
            except:
                pass
            

class ServerSignals(QObject):
    finishedMessageCount = pyqtSignal()
    finishedOffset = pyqtSignal()
    statusClient  = pyqtSignal()
    statusBattery = pyqtSignal()
    statusJoystick = pyqtSignal()

def main():
    server = Server()
    # threading.Thread(target=server.loop())
    server.run()

if __name__ == "__main__":
    main()
