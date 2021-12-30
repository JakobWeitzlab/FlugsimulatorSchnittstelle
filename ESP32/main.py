from machine import Pin, I2C
import socket
import network
import time

#Wifi Settings
host='192.168.4.1'
port = 1234
SSID="flugsimulator"
PASSWORD="123456789"
wlan=None
s=None

#Sensor Settings
MPUAddress = 0x68
I2CFast = 400000
I2CSlow = 100000

#Register
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
POWER_MANAGEMENT_1 = 0x6B

class MPU():
  def __init__(self):
    self.i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=I2CSlow)
    #self._WakeUp()
    self._running = True
    print("Device found on Address " + str(self.i2c.scan()))
    print("Init MPU complete")
  
  def _WakeUp(self):
    self.i2c.writeto_mem(0x68, 0x6B, bytes([0]))
    print("WakeUp complete")
    time.sleep(0.5)
    
  def _RegisterRead(self):
    high = self.i2c.readfrom_mem(MPUAddress, ACCEL_XOUT_H, 1)
    low = self.i2c.readfrom_mem(MPUAddress, ACCEL_XOUT_L, 1) 
    value = (high[0] << 8) + low[0] #shifting high 8 Bits and adding low
    #print(bin(value))
    return(bin(value))
    
    
class Wifi():
  def __init__(self):
    self.ConnectWifi(SSID, PASSWORD)
    self.CreateSocket()
    print("Wifi init successfull")
    
  def ConnectWifi(self, ssid,passwd):
    global wlan
    self.wlan=network.WLAN(network.STA_IF)                 #create a wlan object
    self.wlan.active(True)                                 #Activate the network interface
    self.wlan.disconnect()                                 #Disconnect the last connected WiFi
    self.wlan.connect(ssid,passwd)                         #connect wifi
    while(self.wlan.ifconfig()[0]=='0.0.0.0'):             #Wait for IP assignment
      print("Trying to Connect to Wifi")
      time.sleep(1)
    return True
    
  def CreateSocket(self):
    #Catch exceptions,stop program if interrupted accidentally in the 'try'
    try:
      if(self.ConnectWifi(SSID,PASSWORD) == True):              #judge whether to connect WiFi
        self.s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      #create socket
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)   #Set the value of the given socket option
        #ip=wlan.ifconfig()[0]                                  #get ip addr
    except:
      if (self.s):
        self.s.close()
      self.wlan.disconnect()
      self.wlan.active(False)
    
  def SendData(self):
    self.s.sendto(self.mpu._RegisterRead(),(host,port))            #send data
    print("Data Send")
    #time.sleep(0.5)
      
  def loop(self):
    self.mpu = MPU()
    self.mpu._WakeUp()
    
    for y in range(0,10):
      self.SendData()
    
    
#Execut the Main function    
def main():
  wifi = Wifi()
  wifi.loop()
  
if __name__ == "__main__":
  main()
