from smbus2 import SMBus
import time
import logging
import math
import numpy
import smbus2


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

    '''def __init__(self):
        # logging Library init
        logging.basicConfig(level=logging.INFO)  # Configure Logging Level
        self._WakeUp()
        return logging.info("init abgeschlossen.")'''

    def _WakeUp(self):
        with SMBus(1) as bus:
            data = 0x00
            bus.write_byte_data(adress, POWER_MANAGEMENT_1, data)
            bus.close()
        return logging.info("MPU Wake up call")

    def _RegisterRead(self, Register_H, Register_L):
        with SMBus(1) as bus:
            high = bus.read_byte_data(adress, Register_H)
            low = bus.read_byte_data(adress, Register_L)
            value = (high << 8) + low
            bus.close()

        # Positiv or negative number?
        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
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

    def _Offset(self):
        gyro_x_5sek = []
        for i in range(0,10):
            int_x = self._Rotation_x()
            gyro_x_5sek.append(int_x)
            time.sleep(1)
        print("Mittelwert von X-Achse", numpy.mean(gyro_x_5sek))
        return numpy.mean(gyro_x_5sek)


    def loop(self):
        '''Execute the Main loop'''

        self._running = True
    
        meanRotationX = []
        while self._running:
            sampleAmount = 0
            while sampleAmount <= 10:
                meanRotationX.append(self._Rotation_x())
                sampleAmount+=1
                #time.sleep(0.001)
            print(time.time(), numpy.mean(meanRotationX))
            meanRotationX.clear()
            #print(time.time(), " X rotation ", self._Rotation_x())
            #print(time.time(), " Y rotation ", self._Rotation_y())
            #time.sleep(0.001)


def main():
    '''Execute the Main Method'''
    mpu = MPU()
    mpu.loop()


if __name__ == "__main__":
    main()
