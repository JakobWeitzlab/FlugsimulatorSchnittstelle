from smbus2 import SMBus
import time
import logging
import math

# import numpy as np

# Adressbereiche
adress = 0x68
POWER_MANAGEMENT_1 = 0x6B
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40


class MPU():

    def __init__(self):
        # logging Library init
        logging.basicConfig(level=logging.INFO)  # Configure Logging Level
        self._WakeUp()
        return logging.info("init abgeschlossen.")

    def _WakeUp(self):
        with SMBus(1) as bus:
            data = 0x00
            bus.write_byte_data(adress, POWER_MANAGEMENT_1, data)
        return logging.info("MPU Wake up call")

    def _RegisterRead(self, Register_H, Register_L):
        high = SMBus(1).read_byte_data(adress, Register_H)
        low = SMBus(1).read_byte_data(adress, Register_L)
        value = (high << 8) + low
        
        return value

    def _RegisterWrite(self, Register, Data):
        SMBus.write_byte_data(adress, Register, Data)
        return logging.info("Data writte")

    def _Acc(self):
        valueX = self._RegisterRead(ACCEL_XOUT_H, ACCEL_XOUT_L)
        valueY = self._RegisterRead(ACCEL_YOUT_H, ACCEL_YOUT_L)
        valueZ = self._RegisterRead(ACCEL_ZOUT_H, ACCEL_ZOUT_L)
        return valueX, valueY, valueZ

    def _distance(self, value1, valueZ):
        distance = math.sqrt(math.pow(value1, 2) + math.pow(valueZ, 2))
        return distance

    def _Rotation_x(self):
        valueX, valueY, valueZ = self._Acc()
        
        yaw = math.atan2(valueY, self._distance(valueX, valueZ))
        return math.degrees(yaw)

    def _Rotation_y(self):
        valueX, valueY, valueZ = self._Acc()

        roll = math.atan2(valueX, self._distance(valueY, valueZ))
        return -math.degrees(roll)

    def loop(self):
        '''Execute the Main loop'''

        self._running = True
        while self._running:
            print("x rotation ", self._Rotation_x())
            # print("Y rotation ", self._Rotation_y())
            time.sleep(0.1)


def main():
    '''Execute the Main Method'''
    mpu = MPU()
    mpu.loop()


if __name__ == "__main__":
    main()
