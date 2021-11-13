from smbus2 import SMBus
import time
import logging
import numpy as np

#Adressbereiche
adress = 0x68
POWER_MANAGEMENT_1 = 0x6B
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44

def Initialisierung():
    #logging Library init
    logging.basicConfig(level=logging.INFO) #Configure Logging Level

    return print("init abgeschlossen.")

def WakeUp():
    with SMBus(1) as bus:
            data = 0x00
            bus.write_byte_data(adress, POWER_MANAGEMENT_1, data)
    return logging.info("MPU Wake up call")

def RegisterRead():
    return

def Offset_X():
    return


nullpunkt_X = 0
binary_x = 0

'''
#Wake up
with SMBus(1) as bus:
            data = 0x00
            bus.write_byte_data(adress, POWER_MANAGEMENT_1, data)
            logging.info("MPU Wake up call")
'''

gyro_x_5sek = [49]
y = 0

#Read Gyro data and determen x-offset
while y == 0:
    try:
        WakeUp()
        bus = SMBus(1)

        for i in range(0,10000):
            h = bus.read_byte_data(adress, GYRO_XOUT_H)
            l = bus.read_byte_data(adress, GYRO_XOUT_L)
            value = (h << 8) + l

            if (value >= 32768):
                int_x = -((65535 - value) + 1)
            else:
                int_x = value

            gyro_x_5sek.append(int_x)
        
        print("Mittelwert von X-Achse", np.mean(gyro_x_5sek))
        bus.close()
        time.sleep(0.1)

        y = 1
    except OSError:
        print("Kabel ausa zogen")
        time.sleep(2)