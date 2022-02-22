import time
from smbus2 import SMBus

address = 0x68

POWER_MANAGEMENT_1 = 0x6B
SIGNAL_PATH_RESET = 0x68
TEMP_OUT_H = 0x41
TEMP_OUT_L = 0x42

def ResetDevice():
    with SMBus(1) as bus:
        data = 0x80
        bus.write_byte_data(address, POWER_MANAGEMENT_1, data)
    return

def ResetGyro():
    with SMBus(1) as bus:
        data = 0x07
        bus.write_byte_data(address, SIGNAL_PATH_RESET, data)
        time.sleep(.5)
        data = 0x00
        bus.write_byte_data(address, SIGNAL_PATH_RESET, data)
    return

def DisableTemp():
    high = SMBus(1).read_byte_data(address, TEMP_OUT_H)
    low = SMBus(1).read_byte_data(address, TEMP_OUT_L)
    value = (high << 8) + low
    print("before " + str(value))

    with SMBus(1) as bus:
        data = 0x08
        bus.write_byte_data(address, POWER_MANAGEMENT_1, data)
    
    high = SMBus(1).read_byte_data(address, TEMP_OUT_H)
    low = SMBus(1).read_byte_data(address, TEMP_OUT_L)
    value = (high << 8) + low
    print("after " + str(value))
    return

# ResetDevice()
# ResetGyro()
DisableTemp()
time.sleep(.5)
print("Finish")
