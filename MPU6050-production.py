from smbus2 import SMBus
import time
import logging
# import numpy as np

# Adressbereiche
adress = 0x68
POWER_MANAGEMENT_1 = 0x6B
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44


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

    # Read determinated Register
    def _RegisterRead(self, Register_H, Register_L):
        high = SMBus(1).read_byte_data(adress, Register_H)
        low = SMBus(1).read_byte_data(adress, Register_L)
        value = (high << 8) + low
        return value

    def _Rotation_x(self):
        return

    def loop(self):
        '''Execute the Main loop'''

        self._running = True
        while self._running:
            time.sleep(1)


def main():
    '''Execute the Main Method'''
    mpu = MPU()
    mpu.loop()


if __name__ == "__main__":
    main()
