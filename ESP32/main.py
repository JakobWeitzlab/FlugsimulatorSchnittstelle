from machine import Pin, I2C
import socket
import network
import time
import machine



# Wifi Settings
host = '192.168.4.1'
port = 1234
SSID = "flugsimulator"
PASSWORD = "123456789"
wlan = None
s = None

# Sensor Settings
MPUAddress = 0x68
I2CFast = 400000
I2CSlow = 100000

# Register
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
POWER_MANAGEMENT_1 = 0x6B


class Config:
  def __init__(self):
    self._running = False
    return


class MPU:
  def __init__(self, config):
    self._running = config._running
    self._handshakeSuccess = False

    self.i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=I2CFast)
    self._WakeUp()
    self._Handshake()

  def _Handshake(self):
    while self._handshakeSuccess == False:
      print("Attempt to Handshake")
      time.sleep(1)
      if str(self.i2c.scan()) == "[104]":
        self._handshakeSuccess = True
        self._running = True
        print("Handshake Successfull")

  def _WakeUp(self):
    self.i2c.writeto_mem(0x68, 0x6B, bytes([0]))
    print("WakeUp complete")
    time.sleep(0.5)
    print("Init MPU complete")
    
  def _RegisterRead(self, Register_H, Register_L):
    high = self.i2c.readfrom_mem(MPUAddress, Register_H, 1)
    low = self.i2c.readfrom_mem(MPUAddress, Register_L, 1)
    value = (high[0] << 8) + low[0] #shifting high 8 Bits and adding low
    return value

  def _Acc(self):
    valueX = self._RegisterRead(ACCEL_XOUT_H, ACCEL_XOUT_L)
    valueY = self._RegisterRead(ACCEL_YOUT_H, ACCEL_YOUT_L)
    valueZ = self._RegisterRead(ACCEL_ZOUT_H, ACCEL_ZOUT_L)
    data = str(valueX) + " " + str(valueY) + " " + str(valueZ)
    return data
    
    
class Wifi:
  def __init__(self):
    config = Config()
    # Create mpu Object
    self.mpu = MPU(config)
    self._running = self.mpu._running
    
    self.ConnectWifi(SSID, PASSWORD)
    self.CreateSocket()
    print("Wifi init successfull")
    
  def ConnectWifi(self, ssid,passwd):
    global wlan
    self.wlan=network.WLAN(network.STA_IF)                 # create a wlan object
    self.wlan.active(True)                                 # Activate the network interface
    self.wlan.disconnect()                                 # Disconnect the last connected WiFi
    self.wlan.ifconfig(('192.168.4.xx', '255.255.255.0', '192.168.4.1', '8.8.8.8')) # IP for Client 1
    self.wlan.connect(ssid, passwd)                         # connect wifi
    while (self.wlan.isconnected() != True):
        print("trying to connect to Wifi")
        time.sleep(1)
    return True
    
  def CreateSocket(self):
    #Catch exceptions,stop program if interrupted accidentally in the 'try'
    try:
      if(self.ConnectWifi(SSID,PASSWORD) == True):              # judge whether to connect WiFi
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      # create socket
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # Set the value of the given socket option
        #ip=wlan.ifconfig()[0]                                  # get ip addr
    except:
      if (self.s):
        self.s.close()
      self.wlan.disconnect()
      self.wlan.active(False)
    
  def SendData(self):
    self.s.sendto(self.mpu._Acc(), (host, port))            # send data
    
  def loop(self):
    # mpu._WakeUp()
    while self._running:
      self.SendData()
      

#Execut the Main function
def main():
  # machine.freq(160000000)
  # print(machine.freq())
  wifi = Wifi()
  wifi.loop()
  
if __name__ == "__main__":
  main()
