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

#Read determinated Register
def RegisterRead(Register_H, Register_L):
    h = SMBus(1).read_byte_data(adress, Register_H)
    l = SMBus(1).read_byte_data(adress, Register_L)
    value = (h << 8) + l
    return value

#Calculate Offset X
def Offset_X():
    bus = SMBus(1)
    gyro_x_5sek = []
    for i in range(0,1000):
            value = RegisterRead(GYRO_XOUT_H,GYRO_XOUT_L)
            
            if (value >= 32768):
                int_x = -((65535 - value) + 1)
            else:
                int_x = value

            gyro_x_5sek.append(int_x)
            time.sleep(0.001)
    bus.close()
    return print("Mittelwert von X-Achse", np.mean(gyro_x_5sek))


def Rotation_x():
    value = Offset_X()
    rotation -= value
    return


#MAIN
try:
    #WakeUp()
    Offset_X()
    print("try")

except OSError:
    print("Kabel ausa zogen")
    time.sleep(2)
    